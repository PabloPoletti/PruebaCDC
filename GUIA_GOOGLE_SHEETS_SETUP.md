# 📊 Configuración de Google Sheets para Sistema de Turnos

## 🎯 Objetivo

Integrar Google Sheets con el bot de WhatsApp y Streamlit para gestionar turnos en tiempo real.

---

## 📋 PASO 1: Crear Google Sheet

### 1.1 Crear el documento

1. Ir a https://sheets.google.com/
2. Click en **"Hoja de cálculo en blanco"**
3. Nombrar el documento: **"CDC Turnos"**

### 1.2 Crear la estructura

**En la primera fila (encabezados):**

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| telefono | nombre | dni | motivo | fecha | hora | primera_vez | timestamp |

**Ejemplo de datos:**

| telefono | nombre | dni | motivo | fecha | hora | primera_vez | timestamp |
|----------|--------|-----|--------|-------|------|-------------|-----------|
| 2994152668 | Juan Pérez | 12345678 | Consulta inicial | 2025-11-22 | 09:00 | Si | 2025-11-17 10:30:00 |
| 2995551234 | María García | 23456789 | Seguimiento | 2025-11-22 | 09:30 | No | 2025-11-17 11:00:00 |

### 1.3 Nombrar la solapa

1. Click derecho en la pestaña (abajo) que dice "Hoja 1"
2. Click en **"Cambiar nombre"**
3. Nombrarla: **"Turnos"**

### 1.4 Copiar ID del sheet

En la URL del Google Sheet, copiar el ID:

```
https://docs.google.com/spreadsheets/d/[ESTE_ES_EL_ID]/edit
```

**Ejemplo:**
```
https://docs.google.com/spreadsheets/d/1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t/edit
                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                      Este es el SHEET_ID
```

📝 **Guardá este ID, lo vas a necesitar.**

---

## 🔑 PASO 2: Crear Credenciales de Google Cloud

### 2.1 Ir a Google Cloud Console

1. Ir a: https://console.cloud.google.com/
2. Click en **"Seleccionar un proyecto"** (arriba a la izquierda)
3. Click en **"NUEVO PROYECTO"**

### 2.2 Crear el proyecto

1. **Nombre del proyecto:** `CDC Bot Turnos`
2. Click en **"CREAR"**
3. Esperar a que se cree (30 segundos aprox.)

### 2.3 Habilitar Google Sheets API

1. En el menú lateral (☰), ir a: **APIs y servicios → Biblioteca**
2. Buscar: `Google Sheets API`
3. Click en **"Google Sheets API"**
4. Click en **"HABILITAR"**

### 2.4 Habilitar Google Drive API (también necesario)

1. Volver a **Biblioteca**
2. Buscar: `Google Drive API`
3. Click en **"Google Drive API"**
4. Click en **"HABILITAR"**

---

## 🔐 PASO 3: Crear Cuenta de Servicio

### 3.1 Crear la cuenta

1. Ir a: **APIs y servicios → Credenciales**
2. Click en **"+ CREAR CREDENCIALES"** (arriba)
3. Seleccionar: **"Cuenta de servicio"**

### 3.2 Completar datos

**Paso 1 de 3:**
- **Nombre de la cuenta de servicio:** `cdc-bot-sheets`
- **ID de la cuenta de servicio:** (se completa solo)
- **Descripción:** `Cuenta para acceder a Google Sheets desde el bot del CDC`
- Click en **"CREAR Y CONTINUAR"**

**Paso 2 de 3:**
- **Función:** Seleccionar **"Editor"**
- Click en **"CONTINUAR"**

**Paso 3 de 3:**
- Dejar en blanco
- Click en **"LISTO"**

### 3.3 Descargar el archivo JSON

1. En la lista de **"Cuentas de servicio"**, encontrar la que creaste
2. Click en el **email** de la cuenta (ej: `cdc-bot-sheets@cdc-bot-turnos.iam.gserviceaccount.com`)
3. Ir a la pestaña **"CLAVES"**
4. Click en **"AGREGAR CLAVE"** → **"Crear clave nueva"**
5. Seleccionar tipo: **"JSON"**
6. Click en **"CREAR"**
7. Se descarga un archivo JSON (ej: `cdc-bot-turnos-abc123.json`)

📝 **IMPORTANTE:** Guardá este archivo en un lugar seguro, lo vas a necesitar.

---

## 🔗 PASO 4: Compartir el Google Sheet con la Cuenta de Servicio

### 4.1 Copiar el email de la cuenta de servicio

Abrir el archivo JSON descargado y buscar el campo `client_email`:

```json
{
  "type": "service_account",
  "project_id": "cdc-bot-turnos",
  "client_email": "cdc-bot-sheets@cdc-bot-turnos.iam.gserviceaccount.com",
  ...
}
```

Copiar ese email (ej: `cdc-bot-sheets@cdc-bot-turnos.iam.gserviceaccount.com`)

### 4.2 Compartir el sheet

1. Abrir el Google Sheet **"CDC Turnos"**
2. Click en **"Compartir"** (arriba a la derecha)
3. Pegar el email de la cuenta de servicio
4. Cambiar permisos a: **"Editor"**
5. **DESMARCAR** la casilla "Notificar a las personas"
6. Click en **"Compartir"** o **"Enviar"**

✅ **Listo, ahora el bot puede leer y escribir en el sheet!**

---

## 🔧 PASO 5: Configurar el Bot

### 5.1 Subir credenciales a Railway

**Para WhatsApp Bot (Railway):**

1. Ir a Railway → Tu proyecto → **Variables**
2. Agregar nueva variable:
   - **Name:** `GOOGLE_SHEETS_CREDENTIALS`
   - **Value:** Pegar TODO el contenido del archivo JSON (completo)

**Ejemplo del JSON (TODO esto va en la variable):**
```json
{
  "type": "service_account",
  "project_id": "cdc-bot-turnos",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBg...\n-----END PRIVATE KEY-----\n",
  "client_email": "cdc-bot-sheets@cdc-bot-turnos.iam.gserviceaccount.com",
  "client_id": "123456789...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/..."
}
```

3. Agregar otra variable:
   - **Name:** `GOOGLE_SHEET_ID`
   - **Value:** El ID del sheet que copiaste antes

### 5.2 Configurar Streamlit Cloud

**Para Bot Web (Streamlit):**

1. Ir a Streamlit Cloud → Tu app → **Settings** → **Secrets**
2. Agregar en el editor:

```toml
GROQ_API_KEY = "tu_api_key_de_groq"

[google_sheets]
sheet_id = "TU_SHEET_ID_AQUI"
credentials = '''
{
  "type": "service_account",
  "project_id": "cdc-bot-turnos",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBg...\n-----END PRIVATE KEY-----\n",
  "client_email": "cdc-bot-sheets@cdc-bot-turnos.iam.gserviceaccount.com",
  "client_id": "123456789...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/..."
}
'''
```

3. Click en **"Save"**

---

## ✅ VERIFICACIÓN

### Probar conexión

Después de configurar todo, el bot debería:

1. ✅ Leer turnos existentes del sheet
2. ✅ Mostrar solo horarios disponibles
3. ✅ Guardar nuevos turnos automáticamente
4. ✅ Actualizar el sheet en tiempo real

### Revisar logs

**En Railway:**
- Ir a **Deployments** → Click en el último deploy → Ver **Logs**
- Buscar mensajes como: "✅ Conectado a Google Sheets"

**En Streamlit:**
- Ir a **Settings** → **Logs**

---

## 🆘 Troubleshooting

### Error: "Permission denied"
- ✅ Verificar que compartiste el sheet con el email de la cuenta de servicio
- ✅ Verificar que el permiso sea "Editor"

### Error: "Invalid credentials"
- ✅ Verificar que copiaste TODO el JSON completo
- ✅ Verificar que no haya saltos de línea adicionales

### Error: "Spreadsheet not found"
- ✅ Verificar que el SHEET_ID sea correcto
- ✅ Verificar que el sheet sea accesible

---

## 📞 Contacto

Si tenés problemas con la configuración, avisame y te ayudo paso a paso.

---

**Fecha:** 17 de noviembre de 2025  
**Versión:** 1.0

