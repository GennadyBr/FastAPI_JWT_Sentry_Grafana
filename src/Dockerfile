FROM python:3.11-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR ./src

# system update & package install
RUN apt-get -y update \
    && apt-get -y install curl \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    openssl libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# pip & requirements
COPY requirements.txt requirements.txt
RUN python3 -m pip install --user --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt
