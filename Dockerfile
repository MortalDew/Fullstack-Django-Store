FROM python:3.11-slim-bookworm

WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=api.settings \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python manage.py migrate && \
    gunicorn api.wsgi:application --bind 0.0.0.0:8000 --timeout 300
