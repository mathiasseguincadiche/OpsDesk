"""OpsDesk API — FastAPI application entry point."""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

from .bootstrap import init_database
from .config import get_settings
from .db import SessionLocal, wait_for_database
from .observability import APP_INFO, REGISTRY, BusinessCollector, RequestMiddleware, configure_logging
from .routers import auth, health, stats, tickets, users

settings = get_settings()
configure_logging(settings.log_level, settings.log_format)
log = logging.getLogger("opsdesk")


@asynccontextmanager
async def lifespan(_: FastAPI):
    log.info("starting version=%s revision=%s env=%s", settings.app_version, settings.app_revision, settings.environment)
    wait_for_database(settings.db_connect_retries)
    init_database()
    log.info("ready")
    yield
    log.info("stopping")


app = FastAPI(
    title="OpsDesk API",
    version=settings.app_version,
    description="API de gestion de tickets IT : authentification JWT, tickets, commentaires, statistiques.",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url=None,
    openapi_url="/api/openapi.json",
)

app.add_middleware(RequestMiddleware)
if settings.cors_origin_list:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_methods=["*"],
        allow_headers=["*"],
    )

APP_INFO.labels(settings.app_version, settings.app_revision).set(1)
try:
    REGISTRY.register(BusinessCollector(SessionLocal))
except ValueError:  # already registered (module reloaded in tests)
    pass

for router in (health.router, auth.router, users.router, tickets.router, stats.router):
    app.include_router(router)


@app.exception_handler(HTTPException)
async def http_error(_: Request, exc: HTTPException):
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code, headers=exc.headers)


@app.exception_handler(RequestValidationError)
async def validation_error(_: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = ".".join(str(part) for part in error.get("loc", []) if part not in ("body", "query", "path"))
        message = str(error.get("msg", "Valeur invalide")).removeprefix("Value error, ")
        errors.append({"field": field, "message": message})
    summary = "; ".join(f"{e['field']} : {e['message']}" if e["field"] else e["message"] for e in errors)
    return JSONResponse({"detail": summary or "Requête invalide.", "errors": errors}, status_code=422)


@app.exception_handler(Exception)
async def unexpected_error(request: Request, exc: Exception):
    log.exception("unhandled_error path=%s", request.url.path, exc_info=exc)
    return JSONResponse({"detail": "Erreur interne du serveur."}, status_code=500)


@app.exception_handler(OperationalError)
async def database_down(_: Request, exc: OperationalError):
    log.error("database_unavailable error=%s", exc.orig.__class__.__name__)
    return JSONResponse({"detail": "Base de données indisponible, réessayez dans un instant."}, status_code=503)
