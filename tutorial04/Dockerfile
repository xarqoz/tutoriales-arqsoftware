# 1. Imagen base oficial de Python ligera (slim)
FROM python:3.11-slim

# 2. Evitamos .pyc y forzamos logs sin buffer (se ven en tiempo real)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Dependencias del SO necesarias para compilar/usar PostgreSQL (psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiamos requerimientos e instalamos dependencias de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamos el resto del código fuente
COPY . /app/

# 7. Exponemos el puerto 8000
EXPOSE 8000

# 8. Comando por defecto: 0.0.0.0 hace accesible el contenedor desde fuera
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
