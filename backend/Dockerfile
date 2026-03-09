# 1. Imagen base: Una versión ligera de Python 3.11
FROM python:3.11-slim

# 2. Evitar que Python genere archivos .pyc y que el buffer se llene
ENV PYTHONDONTWRITEBYTECODE 1  
ENV PYTHONUNBUFFERED 1  

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalamos dependencias del sistema (si fueran necesarias)
# En este caso, al ser slim, mantenemos todo limpio.

# 5. Copiar solo el requirements.txt primero (TRUCO DE PRODUCTIVIDAD)
COPY requirements.txt .

# 6. Instalar las librerías de Python
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copiar el resto del código del proyecto
COPY . .

# 8. Informar qué puerto usaremos
EXPOSE 8000

# 9. El comando para arrancar la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]