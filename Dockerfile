FROM python:3.11-slim

# Force rebuild - 2025-11-17
WORKDIR /app

# Copiar SOLO requirements primero (para cache de Docker)
COPY requirements_whatsapp.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements_whatsapp.txt

# Copiar SOLO los archivos necesarios para el bot
COPY whatsapp_bot.py .
COPY bot_logic.py .
COPY sheets_manager.py .
COPY config.py .
COPY db_manager.py .

# Copiar carpeta data (necesaria para RAG)
COPY data/ ./data/

# Exponer puerto
EXPOSE 8000

# Comando de inicio (usar script de shell para expandir $PORT)
CMD sh -c "uvicorn whatsapp_bot:app --host 0.0.0.0 --port ${PORT:-8000}"

