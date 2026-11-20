# syntax=docker/dockerfile:1
# OpsDesk API — image multi-étapes, non-root, au format OCI (Docker, Kubernetes).

FROM docker.io/library/python:3.13-slim AS build
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /build
COPY requirements.txt .
RUN python -m venv /opt/venv \
 && /opt/venv/bin/pip install --upgrade pip \
 && /opt/venv/bin/pip install -r requirements.txt

FROM docker.io/library/python:3.13-slim AS runtime
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
    PORT=8000

# Apply available security fixes in the existing Debian release at build time.
# The periodic scan is still necessary: unavailable fixes remain documented risks.
RUN apt-get update \
 && apt-get upgrade -y --no-install-recommends \
 && rm -rf /var/lib/apt/lists/* \
 && useradd --system --uid 10001 --no-create-home --shell /usr/sbin/nologin opsdesk
COPY --from=build /opt/venv /opt/venv
WORKDIR /app
COPY --chown=10001:10001 app ./app

USER 10001
EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=3s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health/live', timeout=2).status == 200 else 1)"

CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --proxy-headers --forwarded-allow-ips='*' --no-server-header"]
