# syntax=docker/dockerfile:1
# OpsDesk frontend — build React/Vite puis service statique par nginx non-root.

FROM docker.io/library/node:22-alpine AS build
WORKDIR /build
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY . .
RUN npm run build \
 && node -e "const s=require('fs').readFileSync('dist/index.html','utf8').match(/<script>([\s\S]*?)<\/script>/)[1];process.stdout.write(require('crypto').createHash('sha256').update(s).digest('base64'))" > /build/inline-script.sha256

FROM docker.io/nginxinc/nginx-unprivileged:1.29-alpine AS runtime
ARG APP_VERSION=2.0.0
ARG APP_REVISION=dev
LABEL org.opencontainers.image.title="opsdesk-frontend" \
      org.opencontainers.image.description="OpsDesk — interface web (React)" \
      org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.revision="${APP_REVISION}" \
      org.opencontainers.image.licenses="MIT"

ENV BACKEND_URL=http://backend:8000 \
    NGINX_ENTRYPOINT_LOCAL_RESOLVERS=1 \
    NGINX_ENVSUBST_FILTER="^(BACKEND_URL|INLINE_SCRIPT_HASH|NGINX_LOCAL_RESOLVERS)$"
COPY nginx.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build /build/dist /usr/share/nginx/html
COPY --from=build /build/inline-script.sha256 /tmp/inline-script.sha256
# Expose the CSP hash of the inline theme script to envsubst.
USER root
# Apply available Alpine security fixes before returning to the non-root runtime.
RUN apk upgrade --no-cache
RUN printf '#!/bin/sh\nexport INLINE_SCRIPT_HASH="$(cat /tmp/inline-script.sha256)"\n' > /docker-entrypoint.d/05-csp-hash.envsh \
 && chmod +x /docker-entrypoint.d/05-csp-hash.envsh
USER 101

EXPOSE 8080
HEALTHCHECK --interval=15s --timeout=3s --retries=3 CMD wget -qO- http://127.0.0.1:8080/healthz >/dev/null || exit 1
