#!/usr/bin/env bash


npx tailwindcss -i ./src/input.css -o ./static/output.css

CONCURRENCY=$(expr 2 \* $(nproc) + 1)
gunicorn -w  $CONCURRENCY \
    --worker-class=gevent \
    --worker-connections=100 \
    --timeout 120 \
    --log-level=debug \
    --threads=$CONCURRENCY \
    --bind 0.0.0.0:9000 \
    app:app