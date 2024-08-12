#!/bin/sh

python -m poetry run \
    alembic upgrade head
python -m poetry run \
    uvicorn main:app --bind=0.0.0.0:$PORT --workers=$WORKERS
