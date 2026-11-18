"""Structured logging and Prometheus metrics."""
from __future__ import annotations

import json
import logging
import sys
import time
import uuid
from datetime import UTC, datetime

from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram, generate_latest
from prometheus_client.core import GaugeMetricFamily
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

access_log = logging.getLogger("opsdesk.access")


class JsonFormatter(logging.Formatter):
    """One JSON object per line: ready for Loki, Elasticsearch, journald…"""

    def format(self, record: logging.LogRecord) -> str:
        data = {
            "ts": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": record.levelname.lower(),
            "logger": record.name,
            "msg": record.getMessage(),
        }
        data.update(getattr(record, "extra_fields", {}))
        if record.exc_info:
            data["exc"] = self.formatException(record.exc_info)
        return json.dumps(data, ensure_ascii=False)


def configure_logging(level: str, fmt: str) -> None:
    handler = logging.StreamHandler(sys.stdout)
    if fmt == "json":
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-7s %(name)s %(message)s"))
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level.upper())
    # Uvicorn's own access log is replaced by our structured one.
    logging.getLogger("uvicorn.access").disabled = True


REGISTRY = CollectorRegistry()
HTTP_REQUESTS = Counter(
    "opsdesk_http_requests_total", "HTTP requests handled.", ["method", "route", "status"], registry=REGISTRY
)
HTTP_LATENCY = Histogram(
    "opsdesk_http_request_duration_seconds",
    "HTTP request latency.",
    ["method", "route"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5),
    registry=REGISTRY,
)
HTTP_IN_PROGRESS = Gauge("opsdesk_http_requests_in_progress", "Requests in flight.", registry=REGISTRY)
APP_INFO = Gauge("opsdesk_app_info", "Application build information.", ["version", "revision"], registry=REGISTRY)
TICKETS_CREATED = Counter("opsdesk_tickets_created_total", "Tickets created.", ["priority"], registry=REGISTRY)
TICKET_TRANSITIONS = Counter(
    "opsdesk_ticket_transitions_total", "Ticket status changes.", ["from_status", "to_status"], registry=REGISTRY
)
LOGINS = Counter("opsdesk_logins_total", "Login attempts.", ["result"], registry=REGISTRY)


class BusinessCollector:
    """Business gauges computed from the database at scrape time."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def collect(self):
        from sqlalchemy import func, select

        from .models import Ticket, User

        up = GaugeMetricFamily("opsdesk_database_up", "1 if PostgreSQL answers.")
        tickets = GaugeMetricFamily("opsdesk_tickets", "Tickets by status and priority.", labels=["status", "priority"])
        users = GaugeMetricFamily("opsdesk_users", "Active users by role.", labels=["role"])
        try:
            with self.session_factory() as db:
                rows = db.execute(
                    select(Ticket.status, Ticket.priority, func.count()).group_by(Ticket.status, Ticket.priority)
                ).all()
                for status, priority, count in rows:
                    tickets.add_metric([status, priority], count)
                for role, count in db.execute(
                    select(User.role, func.count()).where(User.is_active.is_(True)).group_by(User.role)
                ).all():
                    users.add_metric([role], count)
            up.add_metric([], 1)
        except Exception:  # noqa: BLE001
            up.add_metric([], 0)
        yield up
        yield tickets
        yield users


def metrics_response() -> Response:
    return Response(generate_latest(REGISTRY), media_type="text/plain; version=0.0.4; charset=utf-8")


class RequestMiddleware(BaseHTTPMiddleware):
    """Request id, security headers, access log and HTTP metrics."""

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id") or uuid.uuid4().hex
        started = time.perf_counter()
        HTTP_IN_PROGRESS.inc()
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
        finally:
            HTTP_IN_PROGRESS.dec()
            elapsed = time.perf_counter() - started
            route = request.scope.get("route")
            route_path = getattr(route, "path", "unmatched")
            if route_path not in ("/metrics",):
                HTTP_REQUESTS.labels(request.method, route_path, str(status_code)).inc()
                HTTP_LATENCY.labels(request.method, route_path).observe(elapsed)
            if not route_path.startswith("/health"):
                access_log.info(
                    "%s %s %s",
                    request.method,
                    request.url.path,
                    status_code,
                    extra={
                        "extra_fields": {
                            "request_id": request_id,
                            "method": request.method,
                            "path": request.url.path,
                            "route": route_path,
                            "status": status_code,
                            "duration_ms": round(elapsed * 1000, 2),
                            "client": request.client.host if request.client else None,
                        }
                    },
                )
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers.setdefault("Cache-Control", "no-store")
        return response
