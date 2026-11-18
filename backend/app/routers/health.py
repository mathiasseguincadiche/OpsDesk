from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..config import get_settings
from ..db import database_is_up
from ..observability import metrics_response

router = APIRouter(tags=["ops"])


def _identity() -> dict:
    s = get_settings()
    return {"application": s.app_name, "version": s.app_version, "revision": s.app_revision, "environment": s.environment}


@router.get("/health/live", summary="Liveness probe : le processus répond")
def live():
    return {"status": "alive", **_identity()}


@router.get("/health/ready", summary="Readiness probe : la base de données répond")
def ready():
    if database_is_up():
        return {"status": "ready", "database": "up", **_identity()}
    return JSONResponse({"status": "not_ready", "database": "down", **_identity()}, status_code=503)


@router.get("/version")
def version():
    return _identity()


@router.get("/metrics", include_in_schema=False)
def metrics():
    return metrics_response()
