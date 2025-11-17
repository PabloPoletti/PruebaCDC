FROM python:3.11-slim

WORKDIR /app

# Copiar archivos
COPY . /app/

# Instalar dependencias de WhatsApp Bot
RUN pip install --no-cache-dir -r requirements_whatsapp.txt

# Exponer puerto
EXPOSE 8000

# Comando de inicio para FastAPI
CMD ["uvicorn", "whatsapp_bot:app", "--host", "0.0.0.0", "--port", "8000"]

