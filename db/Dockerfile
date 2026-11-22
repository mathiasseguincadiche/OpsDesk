# PostgreSQL 17 officiel : nous conservons l'initialisation et les binaires amont.
# L'ancienne version de gosu (Go) est remplacée par su-exec d'Alpine (C).
FROM docker.io/library/postgres:17-alpine AS prepared

RUN set -eux; \
    apk upgrade --no-cache; \
    apk add --no-cache su-exec; \
    rm /usr/local/bin/gosu; \
    ln -s "$(command -v su-exec)" /usr/local/bin/gosu; \
    gosu postgres true; \
    test "$(gosu postgres id -u)" = "$(id -u postgres)"

# Recréer une couche finale à partir du système de fichiers ACTUEL :
# ne pas redistribuer les couches historiques contenant l'ancien binaire Go.
# Les métadonnées runtime essentielles de postgres:17-alpine sont explicitées.
FROM scratch
COPY --from=prepared / /
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    LANG=en_US.utf8 \
    PG_MAJOR=17 \
    PGDATA=/var/lib/postgresql/data
VOLUME /var/lib/postgresql/data
ENTRYPOINT ["docker-entrypoint.sh"]
STOPSIGNAL SIGINT
EXPOSE 5432
CMD ["postgres"]
