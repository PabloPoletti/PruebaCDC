# 🏥 Bot Centro de Día Comunitario - 25 de Mayo

Bot de atención automatizada para el Centro de Día Comunitario de 25 de Mayo, La Pampa.

## 🚀 Características

- ✅ **Interface tipo WhatsApp**: Diseño familiar y fácil de usar
- ✅ **IA con RAG**: Responde preguntas usando Groq + LangChain
- ✅ **Sistema de turnos**: Gestión de turnos de psiquiatría
- ✅ **Persistencia de datos**: Los turnos se guardan y comparten entre usuarios
- ✅ **Detección automática**: Responde preguntas sin necesidad de menú

## 📋 Funcionalidades

1. **Información del Centro**: Horarios, dirección, teléfono
2. **Preguntas abiertas**: IA responde usando información del centro
3. **Gestión de turnos**: Reserva de turnos de psiquiatría (viernes)
4. **Consulta de turnos**: Búsqueda por DNI
5. **Turnos compartidos**: Todos los usuarios ven la disponibilidad real

## 🛠️ Tecnologías

- **Frontend**: Streamlit
- **IA**: Groq (Llama 3.1 8B)
- **RAG**: LangChain + ChromaDB + Sentence Transformers
- **Persistencia**: JSON local

## 🌐 Deploy en Streamlit Cloud

### Paso 1: Configurar Secrets

En Streamlit Cloud, ve a **Settings → Secrets** y agrega:

```toml
GROQ_API_KEY = "tu_api_key_de_groq"
```

### Paso 2: Deploy

1. Conecta tu repositorio de GitHub
2. Selecciona la rama `main`
3. El archivo principal es `app.py`
4. Click en **Deploy**

## 📱 Uso

1. Abre la aplicación
2. Interactúa como si fuera WhatsApp
3. Escribe preguntas directamente o usa el menú numérico
4. Para turnos, sigue el flujo guiado

## 📞 Contacto

**Centro de Día Comunitario 25 de Mayo**
- 📍 Dirección: Trenel 53 - 25 de Mayo (La Pampa)
- 📞 Teléfono: 0299 524-3358
- 🕒 Horarios: Lunes a Viernes de 8 a 13 y 16 a 19

---

💚 Desarrollado para mejorar la atención a la comunidad

