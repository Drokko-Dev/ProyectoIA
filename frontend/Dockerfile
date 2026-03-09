# 1. Imagen base de Node (Ligera)
FROM node:20-alpine

# 2. Directorio de trabajo
WORKDIR /app

# 3. TRUCO DE CACHÉ: Copiamos solo los archivos de paquetes primero
COPY package*.json ./

# 4. Instalamos las dependencias
RUN npm install

# 5. Copiamos el resto del código
COPY . .

# 6. Informamos el puerto (Vite usa el 5173 por defecto)
EXPOSE 5173

# 7. Comando para arrancar en modo desarrollo
# --host es VITAL para que Docker pueda "sacar" el puerto hacia afuera
CMD ["npm", "run", "dev", "--", "--host"]