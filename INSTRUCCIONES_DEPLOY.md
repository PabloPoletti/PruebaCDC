# 📦 INSTRUCCIONES PARA SUBIR A GITHUB Y DEPLOYAR EN STREAMLIT

## 🔑 PASO 0: Obtener API Key de GROQ

1. Ve a: https://console.groq.com/keys
2. Crea una cuenta gratis (si no la tenés)
3. Click en "Create API Key"
4. **COPIA LA KEY** (empieza con `gsk_...`)
5. Guardala en un lugar seguro

---

## 📤 PASO 1: Subir archivos a GitHub

### Opción A: Usando Git (Terminal/CMD)

1. **Abrir terminal en la carpeta del proyecto**

2. **Inicializar Git y subir archivos:**

```bash
git init
git add .
git commit -m "Initial commit - Bot CDC"
git branch -M main
git remote add origin https://github.com/PabloPoletti/PruebaCDC.git
git push -u origin main
```

3. Si te pide usuario/contraseña:
   - Usuario: `PabloPoletti`
   - Contraseña: Usa un **Personal Access Token** (no tu contraseña de GitHub)
   - Para crear token: https://github.com/settings/tokens

### Opción B: Usando GitHub Desktop (Más fácil)

1. Descarga GitHub Desktop: https://desktop.github.com/
2. Abre GitHub Desktop
3. File → Add Local Repository
4. Selecciona la carpeta del proyecto
5. Click en "Publish repository"
6. Selecciona "PruebaCDC"
7. Click en "Publish"

### Opción C: Subir archivos manualmente (Más simple)

1. Ve a: https://github.com/PabloPoletti/PruebaCDC
2. Click en "Add file" → "Upload files"
3. Arrastra todos los archivos:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `.gitignore`
   - Carpeta `.streamlit/` con `config.toml`
4. Click en "Commit changes"

---

## 🚀 PASO 2: Deploy en Streamlit Cloud

### 1. Crear cuenta en Streamlit Cloud

1. Ve a: https://share.streamlit.io/
2. Click en "Sign up" o "Continue with GitHub"
3. Autoriza Streamlit a acceder a tu GitHub

### 2. Crear nueva app

1. Click en **"New app"**
2. Completa los campos:
   - **Repository**: `PabloPoletti/PruebaCDC`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Click en **"Advanced settings"**

### 3. Configurar Secrets (IMPORTANTE)

En la sección "Secrets", pega esto:

```toml
GROQ_API_KEY = "gsk_TU_API_KEY_AQUI"
```

**⚠️ REEMPLAZA** `gsk_TU_API_KEY_AQUI` con tu API Key real de GROQ (del Paso 0)

### 4. Deploy

1. Click en **"Deploy!"**
2. Espera 2-3 minutos mientras se instala todo
3. ¡Listo! Tu app estará en una URL como:
   ```
   https://pruebacdc.streamlit.app
   ```

---

## 🔗 PASO 3: Compartir el link

Una vez deployado, copia la URL y compartila con quien quieras.

**Ejemplo de URL:**
```
https://pruebacdc.streamlit.app
```

---

## 🐛 Solución de problemas

### Error: "No module named 'streamlit'"
- Verifica que `requirements.txt` esté en la raíz del proyecto

### Error: "GROQ_API_KEY not found"
- Ve a tu app en Streamlit Cloud
- Settings → Secrets
- Agrega tu API Key

### Error: "Repository not found"
- Verifica que el repositorio sea público
- O autoriza Streamlit a acceder a repos privados

### La app se "duerme"
- Es normal en el plan gratuito
- Se reactiva automáticamente cuando alguien entra (toma 30 seg)

---

## 📊 Ver turnos guardados

Los turnos se guardan en `turnos_data.json` en el servidor de Streamlit.

Para descargar/ver los turnos:
1. Ve a tu app en Streamlit Cloud
2. Settings → Logs
3. O agrega una función de exportación en el código

---

## 🎉 ¡Listo!

Tu bot ya está online y funcionando 24/7.

**Características:**
- ✅ Disponible 24/7
- ✅ Múltiples usuarios simultáneos
- ✅ Turnos compartidos entre todos
- ✅ Respuestas en 1-3 segundos
- ✅ Interface tipo WhatsApp

---

## 📞 Soporte

Si tenés problemas:
1. Revisa los logs en Streamlit Cloud
2. Verifica que la API Key de GROQ sea válida
3. Asegúrate de que todos los archivos estén en GitHub

**Documentación oficial:**
- Streamlit: https://docs.streamlit.io/
- Groq: https://console.groq.com/docs

