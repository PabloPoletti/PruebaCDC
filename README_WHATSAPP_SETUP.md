# 📱 Setup WhatsApp Bot - Guía Paso a Paso

## 🎯 Objetivo
Tener tu bot funcionando en WhatsApp 100% GRATIS en 2-3 horas.

---

## 📋 CHECKLIST RÁPIDO

- [ ] Cuenta Twilio creada
- [ ] WhatsApp Sandbox configurado
- [ ] Cuenta Railway creada
- [ ] Variables de entorno configuradas
- [ ] Deploy realizado
- [ ] Webhook conectado
- [ ] Bot testeado

---

## 🚀 PASO 1: Crear Cuenta Twilio (15 minutos)

### 1.1. Ir a Twilio
```
https://www.twilio.com/try-twilio
```

### 1.2. Registrarse
- Email
- Contraseña
- Nombre del proyecto: "CDC 25 de Mayo Bot"

### 1.3. Verificar teléfono
- Ingresá tu número personal
- Recibís código por SMS
- Ingresá el código

### 1.4. Completar encuesta
- "What do you want to build?": Alerts & Notifications
- "How do you want to build?": With code
- "What is your preferred language?": Python

### 1.5. Obtener créditos
- ✅ Recibís $15 USD de crédito GRATIS
- ✅ Suficiente para ~3,000 mensajes

---

## 🟢 PASO 2: Configurar WhatsApp Sandbox (10 minutos)

### 2.1. En Twilio Console
```
Messaging → Try it out → Send a WhatsApp message
```

### 2.2. Verás tu número Sandbox
```
Número: +1 415 523 8886
Tu código join: join [palabra-aleatoria]
Ejemplo: join coffee-duck
```

### 2.3. Activar el sandbox desde tu WhatsApp
1. Agregar contacto: +1 415 523 8886
2. Enviar: `join coffee-duck` (tu código específico)
3. Recibirás: "You are all set!"

### 2.4. Probar manualmente
- Enviar: "Hola"
- Deberías recibir: "Hello from your Twilio Sandbox"

---

## ☁️ PASO 3: Setup Railway (15 minutos)

### 3.1. Crear cuenta Railway
```
https://railway.app
```

### 3.2. Login con GitHub
- Click en "Login with GitHub"
- Autorizar Railway

### 3.3. Crear nuevo proyecto
```
Dashboard → New Project → Deploy from GitHub repo
```

### 3.4. Seleccionar tu repo
```
PabloPoletti/PruebaCDC
```

### 3.5. Railway detectará automáticamente:
- ✅ `Procfile` (para saber cómo ejecutar)
- ✅ `requirements_whatsapp.txt` (dependencias)

---

## 🔧 PASO 4: Configurar Variables de Entorno (10 minutos)

### 4.1. En Railway, ir a tu proyecto
```
Tu Proyecto → Variables
```

### 4.2. Agregar variables (click en "New Variable")

#### Variable 1: TWILIO_ACCOUNT_SID
```
1. En Twilio Console, ir a: Home → Account Info
2. Copiar "Account SID"
3. En Railway: 
   Key: TWILIO_ACCOUNT_SID
   Value: [pegar Account SID]
```

#### Variable 2: TWILIO_AUTH_TOKEN
```
1. En Twilio Console, en la misma página
2. Copiar "Auth Token" (mostrar primero)
3. En Railway:
   Key: TWILIO_AUTH_TOKEN
   Value: [pegar Auth Token]
```

#### Variable 3: GROQ_API_KEY
```
Key: GROQ_API_KEY
Value: [tu Groq API key actual]
```

### 4.3. Guardar
Railway reiniciará automáticamente con las nuevas variables.

---

## 🌐 PASO 5: Obtener URL Pública (5 minutos)

### 5.1. En Railway
```
Tu Proyecto → Settings → Networking
```

### 5.2. Generate Domain
```
Click en "Generate Domain"
```

### 5.3. Copiar URL
```
Ejemplo: https://cdc-bot-production.up.railway.app
```

### 5.4. Verificar que funciona
```
Ir a: https://tu-url.railway.app
Deberías ver: {"status":"active","service":"CDC WhatsApp Bot",...}
```

---

## 🔗 PASO 6: Conectar Twilio con Railway (10 minutos)

### 6.1. En Twilio Console
```
Messaging → Try it out → Sandbox settings
```

### 6.2. Configurar "WHEN A MESSAGE COMES IN"
```
URL: https://tu-url.railway.app/whatsapp
HTTP Method: POST
```

### 6.3. Configurar "STATUS CALLBACK URL" (opcional)
```
URL: https://tu-url.railway.app/status
HTTP Method: POST
```

### 6.4. Guardar
```
Click en "Save"
```

---

## ✅ PASO 7: Probar el Bot (5 minutos)

### 7.1. Desde tu WhatsApp
```
Enviar a: +1 415 523 8886
Mensaje: Hola
```

### 7.2. Deberías recibir
```
👋 *Bienvenido/a al Centro de Día Comunitario 25 de Mayo*

📋 *Menú principal*
Elegí una opción:

1️⃣ ¿Qué es el Centro de Día?
2️⃣ Horarios y Contacto
3️⃣ Servicios que ofrecemos
4️⃣ Talleres disponibles
5️⃣ Pedir turno con psiquiatra
6️⃣ Ver mis turnos
7️⃣ Pregunta abierta (IA)

👉 Escribí el número de la opción.
```

### 7.3. Probar opciones
```
Enviar: 1
Enviar: 2
Enviar: Qué talleres tienen?
```

---

## 🐛 TROUBLESHOOTING

### Problema 1: "Module not found: app"
**Solución:**
```
Verificar que app.py esté en el repo
Railway debe tener acceso a todos los archivos
```

### Problema 2: "Invalid webhook URL"
**Solución:**
```
Verificar que la URL sea HTTPS (no HTTP)
Verificar que termine en /whatsapp
Ejemplo correcto: https://tu-app.railway.app/whatsapp
```

### Problema 3: Bot no responde
**Solución:**
```
1. Verificar logs en Railway:
   Tu Proyecto → Deployments → [último deploy] → Logs
   
2. Verificar que las variables estén configuradas
   
3. Reiniciar deploy:
   Settings → Restart
```

### Problema 4: "Twilio credentials invalid"
**Solución:**
```
1. Verificar Account SID y Auth Token en Twilio
2. Verificar que estén bien copiados en Railway
3. NO debe tener espacios al inicio/final
```

---

## 📊 MONITOREAR EL BOT

### En Railway (Logs)
```
Tu Proyecto → Deployments → Logs

Verás:
📱 Mensaje recibido de +5492991234567: Hola
🤖 Respuesta enviada: Bienvenido al Centro...
```

### En Twilio (Mensajes)
```
Console → Monitor → Logs → Messaging

Verás todos los mensajes enviados/recibidos
```

---

## 💰 COSTOS ACTUALES

```
✅ Twilio Sandbox: GRATIS
✅ Twilio Crédito: $15 USD GRATIS (~3,000 mensajes)
✅ Railway: $5 USD crédito/mes GRATIS
✅ Groq API: GRATIS (14,400 requests/día)

TOTAL: $0 USD/mes (por 2-3 meses)
```

---

## 📱 COMPARTIR CON USUARIOS

### Crear estas instrucciones para difundir:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 BOT DE WHATSAPP - CDC 25 DE MAYO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

¿Cómo usar el bot?

1️⃣ Guardá este contacto en tu WhatsApp:
   +1 415 523 8886
   Nombre: Bot CDC 25 de Mayo

2️⃣ Enviá este mensaje EXACTO:
   join coffee-duck
   (solo la primera vez)

3️⃣ Esperá la confirmación

4️⃣ Ya podés chatear:
   • Consultá horarios
   • Pedí turnos
   • Preguntá sobre talleres
   • ¡Y más!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💚 Atención automatizada 24/7
Trenel 53, 25 de Mayo, La Pampa
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔄 ACTUALIZAR EL BOT

### Cuando modifiques el código:

```bash
# 1. Hacer cambios en tu código local
# 2. Commit
git add .
git commit -m "Actualizar respuestas del bot"

# 3. Push
git push

# 4. Railway detecta automáticamente y hace redeploy
# Esperar 1-2 minutos
```

---

## 📈 SIGUIENTE PASO: Número Dedicado

### Cuando estés listo para número propio:

**En Twilio:**
```
1. Phone Numbers → Buy a number
2. Buscar número en Argentina: +54 299...
3. Costo: ~$20 USD/mes
4. Configurar WhatsApp en el número
5. Actualizar webhook a tu Railway
```

**Ventajas:**
- ✅ Tu número único
- ✅ Sin "join" requerido
- ✅ Más profesional
- ✅ Sin limitaciones

---

## ✅ CHECKLIST FINAL

- [ ] Bot responde en WhatsApp
- [ ] Menú funciona correctamente
- [ ] RAG responde preguntas
- [ ] Sistema de turnos funciona
- [ ] Logs se ven en Railway
- [ ] Instrucciones listas para compartir

---

## 🎉 ¡LISTO!

Tu bot está funcionando en WhatsApp. Ahora puedes:
1. ✅ Compartir con usuarios del CDC
2. ✅ Monitorear uso en Railway/Twilio
3. ✅ Ajustar respuestas según feedback

---

💚 **¡El CDC ahora tiene un bot en WhatsApp!**

