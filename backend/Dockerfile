# syntax=docker/dockerfile:1
# API OpsDesk : base Alpine minimale, compilation et exécution séparées, utilisateur non-root.

FROM docker.io/library/python:3.13-alpine AS build
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /build
COPY requirements.txt .
RUN python -m venv /opt/venv \
 && /opt/venv/bin/pip install --upgrade pip \
 && /opt/venv/bin/pip install -r requirements.txt \
 && /opt/venv/bin/pip check \
 && /opt/venv/bin/python -m pip uninstall -y pip

FROM docker.io/library/python:3.13-alpine AS runtime
ARG APP_VERSION=2.0.0
ARG APP_REVISION=dev
LABEL org.opencontainers.image.title="opsdesk-api" \
      org.opencontainers.image.description="OpsDesk — API de tickets IT (FastAPI)" \
      org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.revision="${APP_REVISION}" \
      org.opencontainers.image.licenses="MIT"

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_VERSION=${APP_VERSION} \
    APP_REVISION=${APP_REVISION} \
    ENVIRONMENT=production \
    FORWARDED_ALLOW_IPS=127.0.0.1 \
    PORT=8000

# Appliquer les correctifs Alpine disponibles et créer un utilisateur non privilégié.
# L'image de build utilise le même système musl pour les roues Python natives.
RUN apk upgrade --no-cache \
 && addgroup -g 10001 -S opsdesk \
 && adduser -S -D -H -u 10001 -G opsdesk opsdesk
# Supprimer pip de l'image d'exécution : les dépendances sont déjà installées.
RUN /usr/local/bin/python -m pip uninstall -y pip
COPY --from=build /opt/venv /opt/venv
WORKDIR /app
COPY --chown=10001:10001 app ./app
# Migrations nécessaires à l'exécution et au contrôle du schéma de production.
COPY --chown=10001:10001 alembic.ini ./alembic.ini
COPY --chown=10001:10001 migrations ./migrations

USER 10001
EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=3s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health/live', timeout=2).status == 200 else 1)"

# Seuls les proxys explicitement désignés peuvent fournir des en-têtes de transfert.
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --proxy-headers --forwarded-allow-ips=\"${FORWARDED_ALLOW_IPS}\" --no-server-header"]
