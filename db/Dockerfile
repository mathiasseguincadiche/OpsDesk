# Conserver PostgreSQL 17 officiel et son script de démarrage.
# L'outil gosu inclus utilise une ancienne bibliothèque standard Go (issue #51).
FROM docker.io/library/postgres:17-alpine

# Alpine fournit su-exec : même usage pour l'abaissement des privilèges
# (gosu postgres commande), sans dépendance à l'ancienne bibliothèque Go.
# Conserver le nom gosu pour ne pas modifier le script officiel PostgreSQL.
RUN set -eux; \
    apk upgrade --no-cache; \
    apk add --no-cache su-exec; \
    rm /usr/local/bin/gosu; \
    ln -s "$(command -v su-exec)" /usr/local/bin/gosu; \
    gosu postgres true; \
    test "$(gosu postgres id -u)" = "$(id -u postgres)"

# Ne pas modifier ENTRYPOINT, CMD, USER, volume ou les paramètres PostgreSQL.
