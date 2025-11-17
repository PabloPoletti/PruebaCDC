# 🚀 Plan GRATIS Completo - WhatsApp Bot para CDC

## 🎯 Objetivo
Tener un número de WhatsApp funcionando 100% GRATIS que los usuarios del CDC puedan usar para consultas con el bot.

---

## ⚠️ IMPORTANTE: Limitación de WhatsApp Business API

**PROBLEMA:** Meta cambió su política en 2021-2022:
- ❌ WhatsApp Business API ya NO es gratis (requiere pago después de 1,000 conversaciones)
- ❌ No se pueden usar números virtuales con WhatsApp Business API oficial
- ❌ WhatsApp Business App (gratis) no tiene API para bots

**SOLUCIÓN:** Usar alternativas que sí son 100% GRATIS.

---

## ✅ ARQUITECTURA RECOMENDADA 100% GRATIS

### **Opción: Twilio Sandbox + Railway (Tier Gratuito)**

```
┌────────────────────────────────────────────┐
│  Usuario                                   │
│  Envía mensaje a WhatsApp                  │
└──────────────┬─────────────────────────────┘
               │
               │ "join [código]"
               │
┌──────────────▼─────────────────────────────┐
│  Twilio WhatsApp Sandbox (GRATIS)          │
│  Número compartido: +1 415 523 8886        │
│  - Recibe mensajes                         │
│  - Envía respuestas                        │
└──────────────┬─────────────────────────────┘
               │
               │ Webhook HTTP POST
               │
┌──────────────▼─────────────────────────────┐
│  Railway.app (GRATIS - $5 USD crédito/mes) │
│  Servidor Python + FastAPI                 │
│  - Recibe webhooks de Twilio               │
│  - Procesa mensajes                        │
└──────────────┬─────────────────────────────┘
               │
┌──────────────▼─────────────────────────────┐
│  Tu Bot (Lógica actual)                    │
│  - Groq API (GRATIS)                       │
│  - LangChain + ChromaDB                    │
│  - Sistema de turnos                       │
└────────────────────────────────────────────┘
```

---

## 📋 PASO A PASO - Setup Completo (2-3 horas)

### **FASE 1: Crear Cuenta Twilio (15 minutos)**

#### 1. Ir a Twilio
```
https://www.twilio.com/try-twilio
```

#### 2. Crear cuenta gratuita
- ✅ Email
- ✅ Teléfono para verificación (tu número personal)
- ✅ No requiere tarjeta de crédito inicialmente

#### 3. Verificar cuenta
- Código por SMS a tu teléfono

#### 4. Crédito inicial
- ✅ $15 USD de crédito GRATIS para probar
- ✅ Suficiente para ~3,000 mensajes de prueba

---

### **FASE 2: Configurar WhatsApp Sandbox (10 minutos)**

#### 1. En Twilio Console, ir a:
```
Messaging → Try it out → Send a WhatsApp message
```

#### 2. Verás un número compartido:
```
+1 415 523 8886 (número de Twilio Sandbox)
```

#### 3. Para activar, los usuarios deben:
```
1. Agregar +1 415 523 8886 a sus contactos
2. Enviar mensaje: "join [tu-código-único]"
   Ejemplo: "join coffee-duck"
3. Ya pueden chatear con el bot
```

**⚠️ Limitación del Sandbox:**
- Cada usuario debe hacer "join [código]" la primera vez
- Es GRATIS pero no es tu número propio
- Bueno para testing y proyectos sin presupuesto

---

### **FASE 3: Crear Servidor en Railway (20 minutos)**

#### 1. Ir a Railway.app
```
https://railway.app
```

#### 2. Crear cuenta
- ✅ Login con GitHub (usa tu cuenta actual)
- ✅ $5 USD de crédito GRATIS/mes
- ✅ Suficiente para tu bot

#### 3. Crear nuevo proyecto
```
New Project → Deploy from GitHub repo
```

#### 4. Conectar tu repositorio
```
https://github.com/PabloPoletti/PruebaCDC
```

---

### **FASE 4: Código del Bot para WhatsApp (40 minutos)**

Voy a crear los archivos necesarios:

#### **Archivo 1: `whatsapp_bot.py`** (nuevo)
```python
from fastapi import FastAPI, Request, Form
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
from app import bot_response  # Importar tu bot actual

app = FastAPI()

# Configuración Twilio (desde variables de entorno)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.post("/whatsapp")
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(...),
    To: str = Form(...)
):
    """
    Webhook que recibe mensajes de WhatsApp desde Twilio
    """
    # Obtener mensaje del usuario
    user_message = Body
    user_phone = From  # Formato: whatsapp:+5492991234567
    
    # Procesar con tu bot actual
    bot_reply = bot_response(user_message, user_phone)
    
    # Crear respuesta de Twilio
    response = MessagingResponse()
    response.message(bot_reply)
    
    return str(response)

@app.get("/")
async def root():
    return {"status": "WhatsApp Bot CDC - Activo"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

#### **Archivo 2: `requirements_whatsapp.txt`** (nuevo)
```txt
fastapi
uvicorn[standard]
twilio
python-multipart
# Importar los existentes
-r requirements.txt
```

#### **Archivo 3: `Procfile`** (nuevo para Railway)
```
web: uvicorn whatsapp_bot:app --host 0.0.0.0 --port $PORT
```

#### **Archivo 4: `.env.example`** (nuevo)
```
TWILIO_ACCOUNT_SID=tu_account_sid_aqui
TWILIO_AUTH_TOKEN=tu_auth_token_aqui
GROQ_API_KEY=tu_groq_key_aqui
```

---

### **FASE 5: Deploy en Railway (15 minutos)**

#### 1. En Railway, configurar variables de entorno:
```
Settings → Variables

Agregar:
- TWILIO_ACCOUNT_SID: [de tu cuenta Twilio]
- TWILIO_AUTH_TOKEN: [de tu cuenta Twilio]
- GROQ_API_KEY: [tu key actual]
```

#### 2. Railway detectará el Procfile y hará deploy automáticamente

#### 3. Obtener URL pública:
```
Settings → Networking → Generate Domain
Ejemplo: https://cdc-bot.railway.app
```

---

### **FASE 6: Conectar Twilio con Railway (10 minutos)**

#### 1. En Twilio Console:
```
Messaging → Try it out → Sandbox settings
```

#### 2. Configurar Webhook:
```
WHEN A MESSAGE COMES IN:
https://cdc-bot.railway.app/whatsapp

HTTP POST
```

#### 3. Guardar

---

### **FASE 7: Probar el Bot (5 minutos)**

#### 1. Desde tu WhatsApp:
```
1. Agregar contacto: +1 415 523 8886
2. Enviar: join [tu-código-sandbox]
   (Twilio te mostrará el código en el dashboard)
3. Enviar: Hola
4. El bot debería responder!
```

---

## 💰 COSTOS REALES (100% GRATIS por 2-3 meses)

| Servicio | Costo | Límites Gratuitos |
|----------|-------|-------------------|
| **Twilio Sandbox** | GRATIS | Ilimitado (con limitaciones) |
| **Twilio Crédito** | $15 USD gratis | ~3,000 mensajes |
| **Railway Hosting** | GRATIS | $5 USD crédito/mes |
| **Groq API** | GRATIS | 14,400 requests/día |
| **ChromaDB** | GRATIS | Ilimitado |
| **TOTAL MES 1-2** | **$0 USD** | ✅ |

**Después de 2-3 meses:**
- Twilio: ~$5-10 USD/mes (si superas crédito)
- Railway: GRATIS (si estás dentro de $5/mes)

---

## ⚠️ LIMITACIONES del Sandbox (IMPORTANTES)

### **1. Usuarios deben hacer "join" primero**
- ❌ No es automático
- ✅ Solución: Poner instrucciones claras

### **2. Número compartido**
- ❌ No es tu número único
- ❌ Otros proyectos usan el mismo número
- ✅ Es GRATIS

### **3. Mensajes tienen prefijo**
```
Twilio puede agregar:
"Sent from your Twilio trial account - "
```

### **4. Sesión expira después de 3 días**
- ❌ Usuario debe hacer "join" de nuevo si no usa el bot por 3 días
- ✅ Puedes enviar recordatorio

---

## 🎯 ALTERNATIVA: Número Propio (NO gratis, pero mejor)

Si después de testear quieres un número propio sin limitaciones:

### **Opción: Twilio Número Dedicado**

**Costo:**
- Número WhatsApp: ~$20 USD/mes
- Mensajes: $0.005 USD/mensaje
- **Total:** $20-50 USD/mes (para tu volumen)

**Ventajas vs Sandbox:**
- ✅ Tu propio número
- ✅ Sin limitación de "join"
- ✅ Sin expiración de sesión
- ✅ Más profesional
- ✅ Sin prefijo de Twilio

---

## 📱 INSTRUCCIONES PARA USUARIOS DEL CDC

### **Opción 1: Con Sandbox (GRATIS)**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📱 BOT DE WHATSAPP - CDC 25 DE MAYO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Para usar el bot por WhatsApp:

1️⃣ Guardá este contacto:
   +1 415 523 8886
   Nombre: Bot CDC 25 de Mayo

2️⃣ Enviá este mensaje:
   join coffee-duck
   (solo la primera vez)

3️⃣ Esperá confirmación:
   "You are all set!"

4️⃣ Ya podés chatear:
   - Consultá horarios
   - Pedí turnos
   - Preguntá sobre talleres
   - ¡Y más!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💚 Atención automatizada 24/7
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🚀 PLAN DE ACCIÓN - TIMELINE

### **HOY (Día 1): Setup Inicial (2-3 horas)**
```
✅ 1. Crear cuenta Twilio (15 min)
✅ 2. Configurar WhatsApp Sandbox (10 min)
✅ 3. Crear cuenta Railway (5 min)
✅ 4. Yo te creo los archivos del bot (40 min)
✅ 5. Deploy en Railway (15 min)
✅ 6. Conectar webhook (10 min)
✅ 7. Probar el bot (5 min)

RESULTADO: Bot funcionando en WhatsApp
```

### **Día 2-7: Testing**
```
✅ Testear con 5-10 usuarios del CDC
✅ Ajustar respuestas
✅ Documentar problemas
✅ Optimizar flujo
```

### **Día 8-14: Lanzamiento Suave**
```
✅ Compartir con 50-100 usuarios
✅ Monitorear uso
✅ Ajustar según feedback
```

### **Día 15+: Evaluación**
```
¿Funciona bien el Sandbox?
  → SÍ: Seguir con GRATIS
  → NO: Evaluar número dedicado ($20/mes)
```

---

## 🛠️ ARCHIVOS QUE VOY A CREAR PARA TI

1. ✅ `whatsapp_bot.py` - Servidor FastAPI con webhook
2. ✅ `requirements_whatsapp.txt` - Dependencias
3. ✅ `Procfile` - Configuración Railway
4. ✅ `.env.example` - Template de variables
5. ✅ `README_WHATSAPP.md` - Instrucciones completas
6. ✅ `deploy_railway.sh` - Script automatizado (opcional)

---

## 💡 VENTAJAS de esta Arquitectura

### **1. 100% GRATIS para empezar**
- ✅ Twilio Sandbox: GRATIS
- ✅ Railway: GRATIS ($5 crédito/mes)
- ✅ Groq: GRATIS

### **2. Escalable**
- ✅ Si funciona bien → Actualizar a número dedicado
- ✅ Si necesitas más poder → Actualizar Railway Pro

### **3. Sin riesgo**
- ✅ No requiere tarjeta de crédito inicialmente
- ✅ Puedes cancelar cuando quieras
- ✅ No hay contratos

### **4. Rápido de implementar**
- ✅ 2-3 horas de setup
- ✅ Yo te ayudo con el código
- ✅ Deploy automático

---

## 🎯 PRÓXIMO PASO

**¿Quieres que empiece a crear los archivos para WhatsApp?**

Voy a crear:
1. `whatsapp_bot.py` - Servidor con webhook
2. `requirements_whatsapp.txt` - Dependencias
3. `Procfile` - Config Railway
4. `README_WHATSAPP.md` - Instrucciones paso a paso

Y te guío en el setup de Twilio + Railway.

**¿Procedemos? 🚀**

---

## 📊 RESUMEN EJECUTIVO

| Aspecto | Solución |
|---------|----------|
| **Número WhatsApp** | Sandbox Twilio (+1 415 523 8886) |
| **Costo Mes 1-2** | $0 USD (100% GRATIS) |
| **Costo Mes 3+** | $0-10 USD (si superas crédito) |
| **Hosting** | Railway.app (GRATIS) |
| **Setup Time** | 2-3 horas |
| **Limitaciones** | Usuarios deben hacer "join" |
| **Upgrade Path** | Número dedicado $20/mes |

---

💚 **Este es el plan más económico y rápido para tener tu bot en WhatsApp!**

