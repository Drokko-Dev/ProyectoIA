# --- 1. IMAGEN BASE ---
# Usamos Python 3.10 versión 'slim' (ligera). 
# Es la versión más estable y recomendada para correr PyTorch y modelos de IA.
FROM python:3.10-slim

# --- 2. DEPENDENCIAS DEL SISTEMA OPERATIVO ---
# Actualizamos Linux e instalamos 'ffmpeg' (el motor estándar de la industria para manipular audio)
# y 'build-essential' (necesario para compilar algunas partes de XTTS).
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# --- 3. ENTORNO DE TRABAJO ---
# Le decimos a Docker que todo lo que hagamos a partir de ahora será dentro de la carpeta /app
WORKDIR /app

# --- 4. INSTALACIÓN DE LIBRERÍAS DE PYTHON ---
# Copiamos SOLAMENTE el requirements.txt primero. 
# (Esto es un truco Pro: si cambias tu código mañana, Docker no volverá a descargar PyTorch de 2GB, usará su caché).
COPY requirements.txt .

# Instalamos las librerías sin guardar basura (--no-cache-dir) para que la imagen pese menos.
RUN pip install --no-cache-dir -r requirements.txt

# --- 5. CÓDIGO FUENTE ---
# Ahora sí, copiamos nuestro main.py y cualquier otro archivo a la carpeta /app del contenedor.
COPY . .

# --- 6. PUERTO Y ARRANQUE ---
# Exponemos el puerto 8001 (que es el que elegimos para no chocar con tu backend en el 8000)
EXPOSE 8001

# El comando final que ejecuta el contenedor al despertar
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]