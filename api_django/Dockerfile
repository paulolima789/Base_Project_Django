FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE=core.settings

COPY . .

RUN mkdir -p /data/web/staticfiles
RUN mv /app/favicon.ico /data/web/staticfiles/favicon.ico

RUN python -m venv /venv
RUN apt-get update && \
	apt-get install -y --no-install-recommends && \
	rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]