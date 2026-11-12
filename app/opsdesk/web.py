"""Server-rendered UI, JSON API, probes and modest operational metrics."""
from collections import defaultdict
from datetime import timezone
from pathlib import Path
from threading import Lock
import hmac
import os
import secrets
import time

from flask import Flask, abort, g, jsonify, redirect, render_template, request, session, url_for
import psycopg
from psycopg.rows import dict_row
from werkzeug.exceptions import SecurityError

from .business import InvalidTicket, STATUSES, next_status, ticket_input

COUNTERS = defaultdict(int)
COUNTER_LOCK = Lock()


def secret_file(name):
    path = os.environ.get(name)
    if not path:
        raise RuntimeError(f"Fichier secret requis : {name}.")
    value = Path(path).read_text(encoding="utf8").strip()
    if len(value) < 32:
        raise RuntimeError(f"Secret trop court : {name}.")
    return value


def connect():
    # Parameters remain separate: neither passwords nor DSNs are logged.
    return psycopg.connect(
        host=os.environ.get("DB_HOST", "db"), port=int(os.environ.get("DB_PORT", "5432")),
        dbname=os.environ.get("DB_NAME", "opsdesk"), user=os.environ.get("DB_USER", "opsdesk_app"),
        password=secret_file("DB_PASSWORD_FILE"), connect_timeout=3,
        application_name="opsdesk", row_factory=dict_row,
    )


def serialized(row):
    return {key: (value.astimezone(timezone.utc).isoformat() if hasattr(value, "astimezone") else value) for key, value in row.items()}


def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=secret_file("SESSION_SECRET_FILE"), MAX_CONTENT_LENGTH=16 * 1024,
        SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax",
        TRUSTED_HOSTS=[host.strip() for host in os.environ.get("TRUSTED_HOSTS", "127.0.0.1,localhost").split(",") if host.strip()],
    )
    identity = {"application": "OpsDesk", "version": os.environ.get("APP_VERSION", "0.1.0"), "revision": os.environ.get("APP_REVISION", "uncommitted")}

    @app.before_request
    def start_request():
        g.started = time.monotonic()
        if request.method in {"POST", "PATCH"} and request.path.startswith("/api/") and not request.is_json:
            abort(415)

    @app.after_request
    def finish_request(response):
        response.headers.update({
            "X-Content-Type-Options": "nosniff", "X-Frame-Options": "DENY",
            "Content-Security-Policy": "default-src 'self'; style-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'",
            "Referrer-Policy": "no-referrer", "Cache-Control": "no-store",
        })
        duration = time.monotonic() - g.get("started", time.monotonic())
        endpoint = request.endpoint or "not_found"
        with COUNTER_LOCK:
            COUNTERS[(request.method, endpoint, response.status_code)] += 1
        app.logger.info("method=%s endpoint=%s status=%s duration_ms=%.2f", request.method, endpoint, response.status_code, duration * 1000)
        return response

    def csrf():
        if "csrf" not in session:
            session["csrf"] = secrets.token_hex(24)
        return session["csrf"]

    @app.context_processor
    def context():
        return {"identity": identity, "csrf_token": csrf, "status_labels": {"open": "Ouvert", "in_progress": "En cours", "closed": "Clôturé"}}

    def ensure_csrf():
        supplied = request.form.get("csrf", "")
        if not supplied or not supplied.isascii() or not hmac.compare_digest(session.get("csrf", ""), supplied):
            abort(400, description="Formulaire expiré : rechargez la page.")

    def tickets():
        with connect() as conn:
            return conn.execute("SELECT id,title,description,priority,status,created_at,updated_at FROM tickets ORDER BY id DESC LIMIT 100").fetchall()

    def ticket(ticket_id):
        with connect() as conn:
            row = conn.execute("SELECT id,title,description,priority,status,created_at,updated_at FROM tickets WHERE id=%s", (ticket_id,)).fetchone()
        if not row:
            abort(404)
        return row

    def create(payload):
        value = ticket_input(payload)
        with connect() as conn:
            return conn.execute(
                "INSERT INTO tickets (title,description,priority) VALUES (%s,%s,%s) RETURNING id,title,description,priority,status,created_at,updated_at",
                (value["title"], value["description"], value["priority"]),
            ).fetchone()

    def change(ticket_id, target):
        with connect() as conn:
            row = conn.execute("SELECT status FROM tickets WHERE id=%s FOR UPDATE", (ticket_id,)).fetchone()
            if not row:
                abort(404)
            try:
                checked = next_status(row["status"], target)
            except InvalidTicket as error:
                abort(409, description=str(error))
            return conn.execute(
                "UPDATE tickets SET status=%s,updated_at=now() WHERE id=%s RETURNING id,title,description,priority,status,created_at,updated_at",
                (checked, ticket_id),
            ).fetchone()

    @app.get("/")
    def home():
        return redirect(url_for("list_page"))

    @app.get("/tickets")
    def list_page():
        return render_template("tickets.html", tickets=tickets())

    @app.post("/tickets")
    def new_ticket():
        ensure_csrf()
        try:
            row = create(request.form.to_dict())
        except InvalidTicket as error:
            abort(400, description=str(error))
        return redirect(url_for("detail_page", ticket_id=row["id"]), code=303)

    @app.get("/tickets/<int:ticket_id>")
    def detail_page(ticket_id):
        return render_template("ticket.html", ticket=ticket(ticket_id))

    @app.post("/tickets/<int:ticket_id>/status")
    def change_page(ticket_id):
        ensure_csrf()
        change(ticket_id, request.form.get("status"))
        return redirect(url_for("detail_page", ticket_id=ticket_id), code=303)

    @app.get("/api/tickets")
    def list_api():
        return jsonify([serialized(row) for row in tickets()])

    @app.post("/api/tickets")
    def new_api():
        try:
            row = create(request.get_json())
        except InvalidTicket as error:
            abort(400, description=str(error))
        return jsonify(serialized(row)), 201, {"Location": url_for("detail_api", ticket_id=row["id"])}

    @app.get("/api/tickets/<int:ticket_id>")
    def detail_api(ticket_id):
        return jsonify(serialized(ticket(ticket_id)))

    @app.patch("/api/tickets/<int:ticket_id>")
    def change_api(ticket_id):
        payload = request.get_json()
        if not isinstance(payload, dict) or set(payload) != {"status"}:
            abort(400, description="Le changement attend uniquement le champ status.")
        return jsonify(serialized(change(ticket_id, payload["status"])))

    @app.get("/health/live")
    def live():
        return jsonify(status="alive", **identity)

    @app.get("/health/ready")
    def ready():
        with connect() as conn:
            conn.execute("SELECT id FROM tickets LIMIT 1").fetchone()
        return jsonify(status="ready", database="reachable", **identity)

    @app.get("/version")
    def version():
        return jsonify(**identity)

    @app.get("/metrics")
    def metrics():
        lines = ["# HELP opsdesk_http_requests_total Requests handled by this worker.", "# TYPE opsdesk_http_requests_total counter"]
        with COUNTER_LOCK:
            snapshot = list(COUNTERS.items())
        for (method, endpoint, status), count in sorted(snapshot):
            lines.append(f'opsdesk_http_requests_total{{method="{method}",endpoint="{endpoint}",status="{status}"}} {count}')
        try:
            with connect() as conn:
                counts = conn.execute("SELECT status,count(*) AS total FROM tickets GROUP BY status").fetchall()
            lines.extend(["# TYPE opsdesk_database_up gauge", "opsdesk_database_up 1", "# TYPE opsdesk_tickets gauge"])
            lines += [f'opsdesk_tickets{{status="{row["status"]}"}} {row["total"]}' for row in counts]
        except psycopg.Error:
            lines.extend(["# TYPE opsdesk_database_up gauge", "opsdesk_database_up 0"])
        return "\n".join(lines) + "\n", 200, {"Content-Type": "text/plain; version=0.0.4; charset=utf-8"}

    @app.errorhandler(psycopg.Error)
    def unavailable(_error):
        app.logger.warning("database_unavailable request_endpoint=%s", request.endpoint)
        if request.path.startswith("/api/") or request.path.startswith("/health/"):
            return jsonify(error="PostgreSQL indisponible ; consulter les contrôles du laboratoire."), 503
        return render_template("error.html", message="PostgreSQL est indisponible. Vérifiez la readiness et les journaux du laboratoire."), 503

    @app.errorhandler(400)
    @app.errorhandler(404)
    @app.errorhandler(409)
    @app.errorhandler(413)
    @app.errorhandler(415)
    def expected_error(error):
        # An untrusted Host is rejected before Flask has a URL adapter. Rendering
        # a template with url_for here would turn the intended 400 into a 500.
        if isinstance(error, SecurityError):
            return "Hôte HTTP non autorisé.\n", 400, {"Content-Type": "text/plain; charset=utf-8"}
        message = error.description
        if request.path.startswith("/api/"):
            return jsonify(error=message), error.code
        return render_template("error.html", message=message), error.code

    return app
