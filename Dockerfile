FROM python:3.12-slim

# Python sozlamalari
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Ishchi papka
WORKDIR /app

# Kerakli tizim kutubxonalari
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Requirements faylini nusxalash
COPY requirements.txt .

# Python kutubxonalarini o'rnatish
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Loyiha fayllarini nusxalash
COPY . .

# Media va static papkalar
RUN mkdir -p /app/media /app/static

# Django porti
EXPOSE 8000

# Gunicorn orqali ishga tushirish
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]