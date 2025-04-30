FROM python:slim

WORKDIR /flask

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry 
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-root

RUN poetry install --no-root

COPY app app

RUN apt-get purge -y gcc python3-dev libffi-dev && apt-get autoremove -y

CMD ["python3", "-m", "app"]