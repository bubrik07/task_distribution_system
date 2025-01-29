#!/bin/bash

# Waiting for the database to be available
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is up"

# Waiting for Redis to be available
echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 0.1
done
echo "Redis is up"

# Running migrations
python manage.py migrate --noinput

# Starting the server or celery worker
if [ "$1" = 'celery' ]; then
  exec celery -A task_distribution worker --loglevel=info
else
  exec python manage.py runserver 0.0.0.0:8000
fi