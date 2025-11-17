# 🤖 Bot de WhatsApp - Centro de Día Comunitario 25 de Mayo

Bot de atención automatizada para WhatsApp usando Twilio y Groq AI.

## 📋 Características

- ✅ Información del CDC (horarios, servicios, talleres)
- ✅ Sistema de turnos con psiquiatra (integrado con Google Sheets)
- ✅ Respuestas inteligentes con IA (RAG)
- ✅ Menú interactivo tipo WhatsApp
- ✅ Gestión de turnos en tiempo real

## 🚀 Tecnologías

- **FastAPI** - Framework web
- **Twilio** - API de WhatsApp
- **Groq** - LLM (Llama 3.1 8B Instant)
- **Google Sheets API** - Gestión de turnos
- **Railway** - Hosting gratuito

## 📂 Estructura

```
whatsapp/
├── whatsapp_bot.py          # Servidor FastAPI + Twilio webhooks
├── bot_logic.py             # Lógica del bot y menú
├── sheets_manager.py        # Gestor de Google Sheets
├── requirements_whatsapp.txt # Dependencias
├── Dockerfile               # Docker para Railway
├── railway.json             # Configuración de Railway
├── Procfile                 # Comando de inicio
└── data/                    # Datos para RAG
    ├── info_cdc.txt
    ├── talleres.txt
    └── preguntas_frecuentes.txt
```

## ⚙️ Variables de Entorno

```bash
# Groq AI
GROQ_API_KEY=tu_groq_api_key

# Google Sheets (para turnos)
GOOGLE_SHEET_ID=tu_sheet_id
GOOGLE_SHEETS_CREDENTIALS={"type":"service_account",...}

# Puerto (Railway lo configura automáticamente)
PORT=8000
```

## 🌐 Deploy en Railway

1. Fork este repositorio
2. Conectar con Railway
3. Configurar variables de entorno
4. Deploy automático

**URL del bot:** https://web-production-33a77.up.railway.app/

## 📱 Configuración de Twilio

1. Crear cuenta en Twilio
2. Configurar WhatsApp Sandbox
3. Webhook URL: `https://tu-railway-url.up.railway.app/webhook`
4. Método: POST

## 📞 Contacto

Centro de Día Comunitario – 25 de Mayo  
📍 Trenel 53, Colonia 25 de Mayo, La Pampa  
📞 299 4152668  
📧 cdc.25demayolp.coordinacion@gmail.com

---

**Repositorio de Streamlit:** https://github.com/PabloPoletti/PruebaCDC-Streamlit  
**App Web:** https://pruebacdc.streamlit.app/
