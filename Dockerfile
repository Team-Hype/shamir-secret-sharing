FROM python:3.12

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY shard/pyproject.toml shard/poetry.lock ./

RUN poetry config virtualenvs.create false \
 && poetry install --no-root

COPY shard/ ./shard

RUN chmod +x shard/resources/scripts/proto_build.sh \
 && (cd shard && ./resources/scripts/proto_build.sh)
