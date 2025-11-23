# 🚀 Guía Completa: Meta WhatsApp Business API para CDC

## 📋 **ÍNDICE**
1. [Resumen de la Solución](#resumen)
2. [Requisitos Previos](#requisitos)
3. [Paso 1: Crear Cuenta Meta Business](#paso-1)
4. [Paso 2: Configurar WhatsApp Business API](#paso-2)
5. [Paso 3: Conectar tu Número](#paso-3)
6. [Paso 4: Verificar Negocio](#paso-4)
7. [Paso 5: Obtener Credenciales API](#paso-5)
8. [Paso 6: Actualizar Código](#paso-6)
9. [Paso 7: Configurar Webhook](#paso-7)
10. [Paso 8: Testing y Deployment](#paso-8)
11. [Costos y Facturación](#costos)
12. [Troubleshooting](#troubleshooting)

---

## 🎯 **RESUMEN DE LA SOLUCIÓN** {#resumen}

**Objetivo:** Migrar de Twilio Sandbox → Meta WhatsApp Business API

**Beneficios:**
- ✅ **Sin "join"**: Usuarios escriben directo
- ✅ **1000 conversaciones GRATIS/mes**
- ✅ **Número propio**: Tu chip prepago
- ✅ **Check verde** (verificado)
- ✅ **Más profesional**

**Tiempo estimado:** 
- Configuración técnica: 2-3 horas
- Aprobación Meta: 1-5 días hábiles

**Costo inicial:** $0 USD

---

## 📦 **REQUISITOS PREVIOS** {#requisitos}

### **Hardware/SIM:**
- [x] Chip prepago activo
- [x] Número de teléfono argentino
- [ ] **IMPORTANTE**: El número NO debe estar registrado en WhatsApp personal

### **Documentación:**
- [ ] Nombre oficial de la organización: "Centro de Día Comunitario 25 de Mayo"
- [ ] Dirección: Trenel 53, Colonia 25 de Mayo, La Pampa
- [ ] Email de la organización: cdc.25demayolp.coordinacion@gmail.com
- [ ] Logo del CDC (si tienen)
- [ ] Descripción del servicio (para perfil de WhatsApp)

### **Cuentas:**
- [ ] Cuenta de Facebook (personal o de la organización)
- [ ] Cuenta de Gmail (para Meta Business)

### **Técnico:**
- [x] Código del bot funcionando (ya lo tenés)
- [x] Servidor para webhook (Railway/Render)

---

## 🏢 **PASO 1: CREAR CUENTA META BUSINESS** {#paso-1}

### **1.1 Ir a Meta Business Suite**

🔗 **URL:** https://business.facebook.com/

### **1.2 Crear Cuenta Business**

1. **Click en** "Crear cuenta"
2. **Completar:**
   ```
   Nombre de la empresa: Centro de Día Comunitario 25 de Mayo
   Tu nombre: [Tu nombre]
   Email: cdc.25demayolp.coordinacion@gmail.com
   ```

3. **Click en** "Siguiente"

### **1.3 Configurar Cuenta**

1. **Agregar detalles:**
   ```
   Dirección: Trenel 53
   Ciudad: Colonia 25 de Mayo
   Provincia: La Pampa
   Código Postal: L6338
   País: Argentina
   Número de teléfono: [tu número administrativo]
   ```

2. **Tipo de negocio:**
   - Seleccionar: **"Organización sin fines de lucro"** o **"Salud y bienestar"**

3. **Click en** "Enviar"

### **1.4 Verificar Email**

- Revisar bandeja de entrada
- Click en el link de verificación

---

## 📱 **PASO 2: CONFIGURAR WHATSAPP BUSINESS API** {#paso-2}

### **2.1 Acceder a WhatsApp**

1. En Meta Business Suite, ir a:
   - **Menú izquierdo** → "WhatsApp Accounts"
   - O ir directo a: https://business.facebook.com/wa/manage/home/

2. **Click en** "Create a WhatsApp Business Account"

### **2.2 Configurar Cuenta de WhatsApp**

1. **Nombre para mostrar:**
   ```
   CDC 25 de Mayo
   ```

2. **Categoría:**
   ```
   Organización sin fines de lucro
   ```

3. **Descripción:**
   ```
   Centro de Día Comunitario de 25 de Mayo. 
   Atención en salud mental y acompañamiento. 
   Espacio de encuentro, contención y crecimiento.
   ```

4. **Dirección:**
   ```
   Trenel 53, Colonia 25 de Mayo, La Pampa
   ```

5. **Horario de atención:**
   ```
   Lunes a viernes: 9:00 - 20:00
   (El bot responde 24/7)
   ```

6. **Click en** "Siguiente"

---

## 📞 **PASO 3: CONECTAR TU NÚMERO** {#paso-3}

### **⚠️ ADVERTENCIA CRÍTICA:**

**ANTES de continuar, verificá que:**
- ❌ El número NO esté registrado en WhatsApp personal
- ❌ NO tengas conversaciones en ese número
- ✅ Es un número nuevo o que podés resetear

**Si está en uso personal:**
1. Hacer backup de conversaciones importantes
2. Desinstalar WhatsApp del celular con ese número
3. Esperar 24 horas

---

### **3.1 Agregar Número**

1. En la pantalla "Agregar número de teléfono"
2. **Seleccionar:** "Argentina (+54)"
3. **Ingresar tu número:** (sin +54, sin 15, solo el número)
   ```
   Ejemplo: 2995123456
   ```

4. **Método de verificación:** 
   - Recomendado: **"Llamada de voz"** (más rápido)
   - Alternativo: **"SMS"**

5. **Click en** "Siguiente"

### **3.2 Verificar Número**

1. **Recibirás:**
   - Llamada automática con código de 6 dígitos
   - O SMS con el código

2. **Ingresar el código** en la pantalla

3. **Click en** "Verificar"

### **3.3 Confirmar**

✅ Deberías ver: **"Número verificado exitosamente"**

---

## 🏛️ **PASO 4: VERIFICAR NEGOCIO** {#paso-4}

### **4.1 Iniciar Proceso de Verificación**

Meta requiere verificar que sos una organización real.

1. Ir a: **Business Settings** → **Security Center** → **Business Verification**
2. **Click en** "Start Verification"

### **4.2 Método de Verificación**

**Opción A: Verificación por Documentos (MÁS RÁPIDO)**

Subir uno de estos:
- 📄 Documento de inscripción de la organización
- 📄 Estatuto/acta constitutiva
- 📄 Certificado de AFIP (si tienen)
- 📄 Factura de servicios (luz/agua) a nombre del CDC

**Opción B: Verificación por Dominio Email**

Si tenés email con dominio propio (ej: info@cdc25demayo.org):
- Meta enviará un código al email
- Más lento pero más fácil

**Opción C: Verificación por Teléfono**

Meta te llama para confirmar datos.

### **4.3 Información Requerida**

```
Nombre legal: Centro de Día Comunitario 25 de Mayo
Dirección: Trenel 53, Colonia 25 de Mayo, La Pampa, Argentina
Teléfono: 299 4152668
Email: cdc.25demayolp.coordinacion@gmail.com
Sitio web: https://sites.google.com/view/centro-de-dia-25-de-mayo/
          (o tu Vercel: https://prueba-cdc-vercel.vercel.app)
```

### **4.4 Tiempo de Espera**

- ⏱️ **Promedio:** 1-3 días hábiles
- 🚀 **Rápido:** Algunas veces en 24 hs
- 🐢 **Lento:** Hasta 5 días si piden más info

**Mientras esperás, podés continuar con los pasos técnicos (Paso 5-7).**

---

## 🔑 **PASO 5: OBTENER CREDENCIALES API** {#paso-5}

### **5.1 Acceder a Configuración API**

1. Ir a: https://developers.facebook.com/apps/
2. **Click en** "Create App"

### **5.2 Crear App**

1. **Tipo de app:** "Business"
2. **Nombre de la app:**
   ```
   CDC Bot WhatsApp
   ```
3. **Email de contacto:**
   ```
   cdc.25demayolp.coordinacion@gmail.com
   ```
4. **Business Account:** Seleccionar tu cuenta creada en Paso 1
5. **Click en** "Create App"

### **5.3 Configurar WhatsApp**

1. En el dashboard de la app:
   - **Click en** "Add Product"
   - Buscar **"WhatsApp"**
   - **Click en** "Set Up"

2. **Seleccionar:**
   - WhatsApp Business Account: El que creaste en Paso 2
   - WhatsApp Business Phone Number: Tu número verificado

### **5.4 Obtener Token de Acceso**

1. En la sección **"WhatsApp" → "API Setup"**
2. Copiar:
   ```
   📋 Temporary Access Token: whatsapp_business_xxxxxxxxxx
   📋 Phone Number ID: 123456789012345
   📋 WhatsApp Business Account ID: 987654321098765
   ```

3. **⚠️ IMPORTANTE:** Este token es temporal (24 hs)
   - Más adelante configuraremos un token permanente

### **5.5 Generar Token Permanente**

1. Ir a: **App Settings** → **Basic**
2. **Click en** "Show" junto a "App Secret"
3. Copiar el **App Secret**

4. Ir a: **WhatsApp** → **Getting Started**
5. **Click en** "Generate Permanent Token"
6. **Permisos requeridos:**
   - ✅ `whatsapp_business_messaging`
   - ✅ `whatsapp_business_management`

7. **Copiar el token permanente:**
   ```
   📋 Permanent Access Token: EAAxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## 💻 **PASO 6: ACTUALIZAR CÓDIGO** {#paso-6}

Ahora vamos a **reemplazar Twilio con Meta API** en tu código.

### **6.1 Estructura Nueva**

```
whatsapp/
├── bot_logic.py              ← (sin cambios, ya funciona)
├── sheets_manager.py         ← (sin cambios)
├── whatsapp_bot.py          ← ❌ REEMPLAZAR (usa Twilio)
├── whatsapp_bot_meta.py     ← ✅ NUEVO (usa Meta API)
├── requirements_meta.txt     ← ✅ NUEVO
├── env.example.txt          ← 🔄 ACTUALIZAR
└── ...
```

### **6.2 Crear Nuevo Bot con Meta API**

**Archivo: `whatsapp/whatsapp_bot_meta.py`**

```python
"""
Bot de WhatsApp para CDC usando Meta WhatsApp Business API
Reemplaza Twilio con la API oficial de Meta
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os
import sys
import hmac
import hashlib
import requests
from typing import Dict, Any

# Importar lógica del bot
try:
    from bot_logic import bot_response
    print("✅ Bot logic importado correctamente")
except ImportError as e:
    print(f"❌ Error importando bot_logic: {e}")
    sys.exit(1)

# Configuración
VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "CDC_BOT_VERIFY_2024")
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
APP_SECRET = os.getenv("META_APP_SECRET")

# Validar configuración
if not ACCESS_TOKEN or not PHONE_NUMBER_ID:
    print("⚠️ Faltan variables de entorno: WHATSAPP_ACCESS_TOKEN o WHATSAPP_PHONE_NUMBER_ID")

# Inicializar FastAPI
app = FastAPI(
    title="CDC WhatsApp Bot - Meta API",
    version="2.0.0",
    description="Bot de WhatsApp oficial para CDC usando Meta Business API"
)

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def verify_signature(payload: bytes, signature: str) -> bool:
    """
    Verificar que el webhook viene de Meta (seguridad)
    """
    if not APP_SECRET:
        return True  # En desarrollo
    
    expected_signature = hmac.new(
        APP_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature)

def send_whatsapp_message(to: str, message: str) -> Dict[str, Any]:
    """
    Enviar mensaje de WhatsApp usando Meta API
    
    Args:
        to: Número del destinatario (formato: 5492991234567)
        message: Texto del mensaje
    
    Returns:
        Respuesta de la API
    """
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error enviando mensaje: {e}")
        return {"error": str(e)}

def mark_message_as_read(message_id: str):
    """
    Marcar mensaje como leído (opcional pero mejora UX)
    """
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id
    }
    
    try:
        requests.post(url, json=payload, headers=headers, timeout=5)
    except:
        pass  # No crítico si falla

# =====================================================
# ENDPOINTS
# =====================================================

@app.get("/")
async def root():
    """Endpoint raíz - verificar que el servidor está activo"""
    return {
        "status": "active",
        "service": "CDC WhatsApp Bot (Meta API)",
        "version": "2.0.0",
        "api": "Meta WhatsApp Business API",
        "description": "Bot oficial sin 'join' para CDC 25 de Mayo"
    }

@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "whatsapp_configured": bool(ACCESS_TOKEN and PHONE_NUMBER_ID),
        "bot_logic": "active"
    }

@app.get("/webhook")
async def verify_webhook(
    request: Request,
):
    """
    Verificación del webhook (requerido por Meta)
    Meta hace un GET para validar que el webhook es tuyo
    """
    params = request.query_params
    
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")
    
    print(f"📋 Verificación webhook - Mode: {mode}, Token recibido: {token}")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook verificado correctamente")
        return int(challenge)
    else:
        print(f"❌ Verificación fallida - Token esperado: {VERIFY_TOKEN}")
        raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook")
async def webhook(request: Request):
    """
    Webhook principal - recibe mensajes de WhatsApp
    """
    try:
        # Leer el body
        body = await request.body()
        
        # Verificar firma (seguridad)
        signature = request.headers.get("X-Hub-Signature-256", "")
        if APP_SECRET and not verify_signature(body, signature):
            print("❌ Firma inválida")
            raise HTTPException(status_code=403, detail="Invalid signature")
        
        # Parsear JSON
        data = await request.json()
        
        # Log del webhook completo (para debugging)
        print(f"📥 Webhook recibido: {data}")
        
        # Extraer información del mensaje
        if "entry" in data and len(data["entry"]) > 0:
            for entry in data["entry"]:
                if "changes" in entry and len(entry["changes"]) > 0:
                    for change in entry["changes"]:
                        if "value" in change and "messages" in change["value"]:
                            # Procesar cada mensaje
                            for message in change["value"]["messages"]:
                                await process_message(message, change["value"])
        
        # Meta requiere un 200 OK rápido
        return JSONResponse(content={"status": "ok"}, status_code=200)
    
    except Exception as e:
        print(f"❌ Error en webhook: {e}")
        # Aún así devolver 200 para que Meta no reintente
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=200)

async def process_message(message: Dict[str, Any], value: Dict[str, Any]):
    """
    Procesar un mensaje individual de WhatsApp
    """
    try:
        # Extraer datos
        message_id = message.get("id")
        from_number = message.get("from")
        message_type = message.get("type")
        
        # Solo procesar mensajes de texto
        if message_type != "text":
            print(f"⚠️ Tipo de mensaje no soportado: {message_type}")
            return
        
        # Obtener el texto
        text = message.get("text", {}).get("body", "")
        
        if not text:
            return
        
        print(f"📱 Mensaje de {from_number}: {text}")
        
        # Marcar como leído (opcional)
        if message_id:
            mark_message_as_read(message_id)
        
        # Procesar con la lógica del bot
        bot_reply = bot_response(text, from_number)
        
        print(f"🤖 Respuesta generada: {bot_reply[:100]}...")
        
        # Enviar respuesta
        # Si es muy largo, dividir en chunks
        if len(bot_reply) > 4000:  # Límite de WhatsApp
            chunks = [bot_reply[i:i+4000] for i in range(0, len(bot_reply), 4000)]
            for chunk in chunks:
                send_whatsapp_message(from_number, chunk)
        else:
            send_whatsapp_message(from_number, bot_reply)
        
        print(f"✅ Mensaje enviado a {from_number}")
    
    except Exception as e:
        print(f"❌ Error procesando mensaje: {e}")
        
        # Enviar mensaje de error al usuario
        try:
            error_message = (
                "❌ Disculpá, hubo un error procesando tu mensaje. "
                "Por favor intentá de nuevo en unos minutos.\n\n"
                "Si el problema persiste, llamá al 299 4152668."
            )
            send_whatsapp_message(message.get("from"), error_message)
        except:
            pass

# Configuración para Railway/Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Iniciando servidor en puerto {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### **6.3 Crear Requirements para Meta API**

**Archivo: `whatsapp/requirements_meta.txt`**

```txt
# FastAPI y servidor
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6

# WhatsApp - Meta API
requests==2.31.0

# Bot Logic - LLM y RAG
langchain==0.1.4
langchain-groq==0.0.1
groq==0.4.2

# Google Sheets
gspread==5.12.3
google-auth==2.26.2
google-auth-oauthlib==1.2.0
google-auth-httplib2==0.2.0
pandas==2.1.4

# Utilidades
python-dotenv==1.0.0
```

### **6.4 Actualizar Variables de Entorno**

**Archivo: `whatsapp/env.example.txt`**

```bash
# =====================================================
# META WHATSAPP BUSINESS API - CONFIGURACIÓN
# =====================================================

# Token de acceso permanente (del Paso 5.5)
WHATSAPP_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxxxx

# Phone Number ID (del Paso 5.4)
WHATSAPP_PHONE_NUMBER_ID=123456789012345

# WhatsApp Business Account ID (del Paso 5.4)
WHATSAPP_BUSINESS_ACCOUNT_ID=987654321098765

# App Secret (para verificar webhooks - del Paso 5.5)
META_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxx

# Token para verificar webhook (elegí uno fuerte)
WEBHOOK_VERIFY_TOKEN=CDC_BOT_VERIFY_2024_tu_token_secreto_aqui

# =====================================================
# GROQ API (IA/LLM)
# =====================================================

GROQ_API_KEY=tu_groq_api_key_aqui

# =====================================================
# GOOGLE SHEETS (Sistema de turnos)
# =====================================================

GOOGLE_SHEET_ID=tu_sheet_id_aqui
GOOGLE_SHEETS_CREDENTIALS={"type":"service_account",...}

# =====================================================
# SERVIDOR
# =====================================================

PORT=8000
```

### **6.5 Crear archivo .env real**

**Archivo: `whatsapp/.env`** (NO subir a Git)

Copiar `env.example.txt` → `.env` y completar con tus valores reales del Paso 5.

---

## 🔗 **PASO 7: CONFIGURAR WEBHOOK** {#paso-7}

### **7.1 Deployar Código Nuevo**

Primero, subir el código nuevo a Railway/Render:

**Si usás Railway:**

```bash
# Ir a la carpeta whatsapp
cd "F:\Arci Data\Arci 2025\CDC pruebas\whatsapp"

# Agregar archivo nuevo
git add whatsapp_bot_meta.py requirements_meta.txt

# Commit
git commit -m "feat: migrar de Twilio a Meta WhatsApp Business API"

# Push (esto dispara auto-deploy en Railway)
git push
```

**Actualizar comando de inicio en Railway:**

En Railway Dashboard → Settings → Start Command:
```bash
python whatsapp_bot_meta.py
```

### **7.2 Obtener URL del Webhook**

Una vez deployado, copiar tu URL:
```
https://tu-app.railway.app/webhook
```

### **7.3 Configurar Webhook en Meta**

1. Ir a: https://developers.facebook.com/apps/
2. Seleccionar tu app "CDC Bot WhatsApp"
3. Ir a: **WhatsApp** → **Configuration**
4. En la sección **"Webhook"**:
   
   **Callback URL:**
   ```
   https://tu-app.railway.app/webhook
   ```
   
   **Verify Token:**
   ```
   CDC_BOT_VERIFY_2024_tu_token_secreto_aqui
   ```
   (El mismo que pusiste en `WEBHOOK_VERIFY_TOKEN`)

5. **Click en** "Verify and Save"

✅ Deberías ver: **"Webhook verified successfully"**

### **7.4 Subscribir a Eventos**

En la misma página, en **"Webhook fields"**:

✅ Marcar:
- `messages` (requerido - para recibir mensajes)
- `message_status` (opcional - para saber si fue entregado/leído)

**Click en** "Save"

---

## 🧪 **PASO 8: TESTING Y DEPLOYMENT** {#paso-8}

### **8.1 Test 1: Verificar Webhook**

```bash
# Verificar que el servidor responde
curl https://tu-app.railway.app/health

# Deberías ver:
{
  "status": "healthy",
  "whatsapp_configured": true,
  "bot_logic": "active"
}
```

### **8.2 Test 2: Enviar Mensaje de Prueba**

1. **Desde otro teléfono** (no el del bot)
2. **Agregar a contactos:** El número del bot
3. **Abrir WhatsApp**
4. **Enviar mensaje:** "hola"

✅ **Deberías recibir:**
```
👋 Bienvenido/a al Centro de Día Comunitario 25 de Mayo

📋 Menú principal
Elegí una opción:
1️⃣ ¿Qué es el Centro de Día?
...
```

### **8.3 Test 3: Verificar Sin "join"**

🎉 **NO debería pedir "join" → ¡Funciona directo!**

### **8.4 Test 4: Verificar Logs**

En Railway/Render → Logs, deberías ver:
```
📥 Webhook recibido: {...}
📱 Mensaje de 5492991234567: hola
🤖 Respuesta generada: 👋 Bienvenido/a...
✅ Mensaje enviado a 5492991234567
```

### **8.5 Test 5: Probar Diferentes Funciones**

```
Usuario: 1
Bot: [Info del CDC]

Usuario: que talleres hay?
Bot: [Respuesta con IA/RAG]

Usuario: 5
Bot: [Sistema de turnos]
```

---

## 💰 **COSTOS Y FACTURACIÓN** {#costos}

### **Estructura de Costos**

```
📊 CONVERSACIONES GRATIS: 1,000/mes

✅ Primeras 1,000 conversaciones: $0 USD

Después de 1,000:
💰 Conversación iniciada por usuario: $0.0148 USD (~$15 ARS)
💰 Conversación iniciada por bot: $0.0592 USD (~$60 ARS)
```

### **¿Qué es una Conversación?**

- **Ventana de 24 horas** donde pueden intercambiar mensajes ilimitados
- 1 usuario escribe → 1 conversación (aunque mande 100 mensajes en ese día)

### **Ejemplo Real CDC:**

**Mes 1: 50 usuarios**
- 50 conversaciones
- Costo: **$0 USD** ✅ (dentro del free tier)

**Mes 2: 200 usuarios**
- 200 conversaciones
- Costo: **$0 USD** ✅

**Mes 12: 1,500 usuarios** (crecimiento)
- 1,500 conversaciones
- Gratis: 1,000
- Pagás: 500 × $0.0148 = **$7.40 USD** (~$7,400 ARS/mes)

### **Configurar Método de Pago**

Solo se requiere cuando **superes las 1,000 conversaciones**:

1. Ir a: https://business.facebook.com/billing/
2. **Click en** "Add Payment Method"
3. Agregar tarjeta de crédito/débito

⚠️ **No te cobran hasta que superes el límite gratuito**

### **Monitorear Uso**

1. Ir a: https://business.facebook.com/wa/manage/analytics/
2. Ver:
   - Conversaciones del mes
   - Mensajes enviados/recibidos
   - Costo estimado

---

## 🔧 **TROUBLESHOOTING** {#troubleshooting}

### **Problema 1: "Webhook verification failed"**

**Causa:** El `WEBHOOK_VERIFY_TOKEN` no coincide

**Solución:**
1. Verificar que en `.env` tenés el mismo token
2. Verificar que en Meta pusiste el mismo token
3. Redeploy del servidor

### **Problema 2: "Messages not being received"**

**Causa:** Webhook no está subscrito a eventos

**Solución:**
1. Ir a: WhatsApp → Configuration → Webhook fields
2. Marcar `messages`
3. Save

### **Problema 3: "Invalid access token"**

**Causa:** Token expirado o incorrecto

**Solución:**
1. Generar nuevo token permanente (Paso 5.5)
2. Actualizar `WHATSAPP_ACCESS_TOKEN` en `.env`
3. Redeploy

### **Problema 4: El número ya está en uso**

**Causa:** El número está registrado en WhatsApp personal

**Solución:**
1. Desinstalar WhatsApp del celular
2. Esperar 24 horas
3. Volver a intentar en Meta

### **Problema 5: "Business verification pending"**

**Causa:** Meta aún no aprobó tu negocio

**Solución:**
- ⏳ Esperar (puede tomar 1-5 días)
- Mientras tanto, el bot funciona pero con límites:
  - Máximo 250 conversaciones/mes (en vez de 1000)
  - Solo pueden escribirte usuarios que vos agregues primero

### **Problema 6: Bot no responde**

**Debugging:**

```bash
# 1. Verificar logs en Railway/Render
railway logs

# 2. Verificar health
curl https://tu-app.railway.app/health

# 3. Verificar webhook en Meta
# Ir a: WhatsApp → Configuration → Test button

# 4. Verificar variables de entorno
railway variables
```

---

## 📊 **MONITOREO Y ANALYTICS**

### **Métricas Importantes**

**En Meta Business:**
- Conversaciones totales
- Tasa de respuesta
- Tiempo promedio de respuesta

**En tu Google Sheet:**
- Mensajes por usuario
- Opciones más usadas
- Horarios pico

### **Configurar Alertas**

En Meta Business Manager:
1. Ir a: Settings → Notifications
2. Activar alertas para:
   - Conversaciones cerca del límite
   - Errores del webhook
   - Problemas de facturación

---

## ✅ **CHECKLIST FINAL**

Antes de considerar el deployment completo:

### **Cuenta y Configuración:**
- [ ] Cuenta Meta Business creada
- [ ] WhatsApp Business Account configurada
- [ ] Número verificado y conectado
- [ ] Negocio verificado (o en proceso)
- [ ] App de Facebook creada
- [ ] Tokens generados y guardados

### **Código:**
- [ ] `whatsapp_bot_meta.py` creado
- [ ] `requirements_meta.txt` actualizado
- [ ] `.env` configurado con todos los tokens
- [ ] Código deployado en Railway/Render

### **Webhook:**
- [ ] Webhook configurado en Meta
- [ ] URL verificada correctamente
- [ ] Subscrito a evento `messages`

### **Testing:**
- [ ] Health check responde OK
- [ ] Mensaje de prueba recibido
- [ ] Bot responde sin "join"
- [ ] RAG/IA funcionando
- [ ] Sistema de turnos funcionando
- [ ] Logs visibles y claros

### **Producción:**
- [ ] Variables de entorno en producción
- [ ] Monitoring configurado
- [ ] Método de pago agregado (cuando superes 1000)
- [ ] Equipo capacitado en uso del sistema

---

## 🎉 **¡LISTO!**

Ahora tenés un bot de WhatsApp **profesional**, **sin "join"**, y con **1000 conversaciones gratis/mes**.

**Próximos pasos:**
1. Seguir esta guía paso a paso
2. Ir marcando los checkboxes
3. Testear exhaustivamente
4. Lanzar a producción

**Soporte:**
Si tenés dudas en algún paso, avisame y te ayudo en tiempo real.

---

**Última actualización:** 2025-11-21
**Versión:** 2.0
**Autor:** AI Assistant + Pablo Poletti

