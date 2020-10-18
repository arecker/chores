#!/bin/bash -e

if [ "$ENTRYPOINT" == "chorebot" ]; then
    python chorebot.py
else
    gunicorn \
	--bind 0.0.0.0:5000 \
	--workers 1 \
	"app:app"
fi
