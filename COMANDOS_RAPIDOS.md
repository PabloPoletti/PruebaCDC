# ⚡ COMANDOS RÁPIDOS

## 🚀 Deploy en 3 comandos (Git instalado)

```bash
git init
git add .
git commit -m "Bot CDC"
git branch -M main
git remote add origin https://github.com/PabloPoletti/PruebaCDC.git
git push -u origin main
```

---

## 🧪 Probar localmente (antes de subir)

### 1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

### 2. Crear archivo de secrets:
Copia `.streamlit/secrets.toml.example` a `.streamlit/secrets.toml`

Edita y agrega tu API Key:
```toml
GROQ_API_KEY = "gsk_TU_KEY_AQUI"
```

### 3. Ejecutar:
```bash
streamlit run app.py
```

Se abrirá en: http://localhost:8501

---

## 📦 Actualizar código (después del primer push)

```bash
git add .
git commit -m "Actualización del bot"
git push
```

Streamlit Cloud detectará los cambios y re-deployará automáticamente.

---

## 🔑 Links importantes

- **Tu GitHub**: https://github.com/PabloPoletti/PruebaCDC
- **Streamlit Cloud**: https://share.streamlit.io/
- **Groq Console**: https://console.groq.com/
- **Groq API Keys**: https://console.groq.com/keys

---

## 📊 Ver turnos guardados

Los turnos se guardan en `turnos_data.json` en el servidor.

Para acceder:
1. Ve a tu app en Streamlit Cloud
2. Settings → Manage app
3. Los logs mostrarán la info de turnos

---

## 🆘 Comandos de emergencia

### Resetear Git:
```bash
rm -rf .git
git init
```

### Limpiar caché de Streamlit:
```bash
streamlit cache clear
```

### Ver logs en vivo:
En Streamlit Cloud → Manage app → Logs

---

## ✅ Checklist pre-deploy

- [ ] Todos los archivos creados están en la carpeta
- [ ] Tienes tu API Key de GROQ lista
- [ ] GitHub repo está creado (PruebaCDC)
- [ ] Git está instalado (o usarás GitHub web)

---

## 🎯 URL final

Después del deploy, tu app estará en:

```
https://pruebacdc.streamlit.app
```

(El nombre exacto te lo dará Streamlit Cloud)

---

## 📱 Compartir

Una vez deployado, simplemente comparte el link:

```
Hola! Probá el nuevo bot del Centro de Día:
https://pruebacdc.streamlit.app

Podés hacer preguntas y sacar turnos 24/7 🏥
```

---

¡Listo! 🎉

