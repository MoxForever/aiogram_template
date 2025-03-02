FROM python:alpine3.16

RUN addgroup -S bot
RUN adduser -S -D -h /app bot bot
USER bot

ENV PATH="/app/.venv/bin:${PATH}"

WORKDIR /app
RUN pip install poetry --no-cache-dir
RUN python -m poetry config virtualenvs.in-project true

COPY pyproject.toml poetry.lock ./
RUN python -m poetry install --only main
COPY . .

ENV WORKERS 4
ENV PORT 80
EXPOSE $PORT

ENTRYPOINT ["sh", "./docker/docker-entrypoint.sh"]
