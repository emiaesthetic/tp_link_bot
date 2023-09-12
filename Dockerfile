FROM python:3.11-slim as base

RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/root/poetry python3 -
ENV PATH="${PATH}:/root/poetry/bin"

WORKDIR /opt/bot


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY poetry.lock pyproject.toml /
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . .

CMD ["python", "app.py"]
