FROM postgres:15-alpine

# Build-time args (pass DB values at build or provide env at runtime)
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD

# Map build args to runtime env vars used by the official image
# Do NOT set PGHOST/PGPORT here to avoid baking empty values into the image.
ENV POSTGRES_DB=${DB_NAME} \
    POSTGRES_USER=${DB_USER} \
    POSTGRES_PASSWORD=${DB_PASSWORD}

EXPOSE 5432

# Healthcheck (uses pg_isready from the postgres image)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD pg_isready -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" || exit 1

# Keep the default entrypoint/CMD from the base image

# docker exec -it postgres_django psql -U djangouser -d djangotraining