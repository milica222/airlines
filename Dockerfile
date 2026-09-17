FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        default-jre-headless \
        procps \
        tini \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY requirements.lock.txt /tmp/requirements.lock.txt
RUN python -m pip install --upgrade pip \
    && pip install -r /tmp/requirements.lock.txt

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["bash"]
