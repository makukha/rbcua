ARG PYTHON_IMAGE=python:3.12.5-slim-bookworm

FROM ${PYTHON_IMAGE} as base
SHELL ["/bin/bash", "-eux", "-o", "pipefail", "-c"]

# sys
RUN apt update; \
    apt install -y curl tzdata; \
    rm -rf /var/lib/apt/lists/*
ENV TZ="Europe/Kyiv"

# supercronic
ENV SUPERCRONIC_VERSION=0.2.30 \
    SUPERCRONIC_SHA1SUM=9f27ad28c5c57cd133325b2a66bba69ba2235799 \
    SUPERCRONIC=supercronic-linux-amd64
RUN curl -fsSLO "https://github.com/aptible/supercronic/releases/download/v${SUPERCRONIC_VERSION}/${SUPERCRONIC}"; \
    echo "${SUPERCRONIC_SHA1SUM} ${SUPERCRONIC}" | sha1sum -c -; \
    chmod +x "${SUPERCRONIC}"; \
    mv "${SUPERCRONIC}" "/usr/local/bin/${SUPERCRONIC}"; \
    ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

# user
RUN adduser --uid 999 --home /app app; \
    mkdir -p /var/{lib,run}/app; \
    chown app:app /var/{lib,run}/app
WORKDIR /app

# python environment
ENV PIP_DISABLE_PIP_VERSION_CHECK=true
RUN python -m venv .venv
ENV PATH=/app/.venv/bin:$PATH
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY rbcua.py ./

# entrypoint
COPY crontab ./
ENTRYPOINT []
CMD supercronic -passthrough-logs /app/crontab
