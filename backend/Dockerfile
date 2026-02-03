# Usar imagen oficial de Python 3.11
FROM python:3.11-slim
# Establecer directorio de trabajo
WORKDIR /app
# Copiar requirements primero (para cache de Docker)
COPY requirements.txt .
# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt
# Copiar el resto del código
COPY . .
# Exponer el puerto que usa FastAPI
EXPOSE 8000
# Comando para iniciar la aplicación7
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]