FROM python:3.8.2-slim-buster
MAINTAINER Alex Recker <alex@reckerfamily.com>

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE "1"
ENV PYTHONUNBUFFERED "1"
ENV FLASK_ENV "production"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./
COPY templates ./templates/
COPY static ./static/
COPY scripts/entry.sh .

ENTRYPOINT ["./entry.sh"]
