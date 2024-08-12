FROM python:alpine3.16

RUN addgroup -S bot
RUN adduser -S -D -h /app bot bot
USER bot

WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN python -m poetry install
COPY . .

ENV WORKERS 4
ENV PORT 80
EXPOSE $PORT

ENTRYPOINT ["sh", "./docker/docker-entrypoint.sh"]
