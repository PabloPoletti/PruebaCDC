"""
Bot de WhatsApp para el Centro de Día Comunitario - 25 de Mayo
Servidor FastAPI que recibe webhooks de Twilio y procesa mensajes
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
import os
import sys

# Importar la lógica del bot (versión ligera sin Streamlit)
try:
    from bot_logic import bot_response
    print("✅ Bot logic importado correctamente")
except ImportError as e:
    print(f"Error: No se pudo importar bot_logic.py: {e}")
    sys.exit(1)

# Inicializar FastAPI
app = FastAPI(title="CDC WhatsApp Bot", version="1.0.0")

@app.get("/")
async def root():
    """Endpoint raíz - verificar que el servidor está activo"""
    return {
        "status": "active",
        "service": "CDC WhatsApp Bot",
        "version": "1.0.0",
        "description": "Bot de atención automatizada para Centro de Día Comunitario 25 de Mayo"
    }

@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {
        "status": "healthy",
        "rag_initialized": llm is not None and retriever is not None
    }

@app.post("/whatsapp")
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(...),
    To: str = Form(...),
    MessageSid: str = Form(None)
):
    """
    Webhook que recibe mensajes de WhatsApp desde Twilio
    
    Args:
        Body: Contenido del mensaje del usuario
        From: Número del usuario (formato: whatsapp:+5492991234567)
        To: Número del bot (Twilio)
        MessageSid: ID único del mensaje
    
    Returns:
        TwiML response con la respuesta del bot
    """
    
    try:
        # Limpiar el formato del número
        user_phone = From.replace("whatsapp:", "")
        
        # Log del mensaje recibido
        print(f"📱 Mensaje recibido de {user_phone}: {Body}")
        
        # Procesar con el bot actual
        # La función bot_response maneja todo: menús, turnos, RAG, etc.
        bot_reply = bot_response(Body, user_phone)
        
        # Log de la respuesta
        print(f"🤖 Respuesta enviada: {bot_reply[:100]}...")
        
        # Crear respuesta TwiML
        response = MessagingResponse()
        
        # Si la respuesta es muy larga, dividirla en múltiples mensajes
        # WhatsApp tiene límite de ~1600 caracteres por mensaje
        if len(bot_reply) > 1500:
            # Dividir en chunks
            chunks = [bot_reply[i:i+1500] for i in range(0, len(bot_reply), 1500)]
            for chunk in chunks:
                response.message(chunk)
        else:
            response.message(bot_reply)
        
        # Retornar como XML (TwiML)
        return Response(content=str(response), media_type="application/xml")
    
    except Exception as e:
        # Log del error
        print(f"❌ Error procesando mensaje: {e}")
        
        # Respuesta de error amigable
        response = MessagingResponse()
        response.message(
            "❌ Disculpá, hubo un error procesando tu mensaje. "
            "Por favor intentá de nuevo en unos minutos.\n\n"
            "Si el problema persiste, llamá al 299 4152668."
        )
        
        return Response(content=str(response), media_type="application/xml")

@app.post("/status")
async def whatsapp_status(request: Request):
    """
    Webhook para recibir actualizaciones de estado de mensajes
    (entregado, leído, fallido, etc.)
    """
    # Este endpoint es opcional pero útil para debugging
    data = await request.form()
    message_status = data.get("MessageStatus")
    message_sid = data.get("MessageSid")
    
    print(f"📊 Estado del mensaje {message_sid}: {message_status}")
    
    return Response(content="OK", status_code=200)

# Configuración para Railway/Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

