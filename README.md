# 🏥 Bot Centro de Día Comunitario - 25 de Mayo

Bot de atención automatizada para el Centro de Día Comunitario de Colonia 25 de Mayo, La Pampa.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pruebacdc.streamlit.app)

---

## 🚀 Características

- ✅ **Interface tipo WhatsApp**: Diseño familiar y fácil de usar
- ✅ **IA con RAG**: Responde preguntas usando Groq + LangChain
- ✅ **Sistema de turnos**: Gestión de turnos de psiquiatría
- ✅ **Información completa**: Talleres, horarios, servicios
- ✅ **Persistencia de datos**: Los turnos se guardan y comparten entre usuarios
- ✅ **Detección automática**: Responde preguntas sin necesidad de menú

---

## 📋 Funcionalidades

### Menú Principal (7 opciones):

1. **¿Qué es el Centro de Día?** - Información institucional e histórica
2. **Horarios y Contacto** - Ubicación, teléfono, email, horarios
3. **Servicios que ofrecemos** - Lista completa de servicios gratuitos
4. **Talleres disponibles** - 5 talleres con horarios específicos
5. **Pedir turno con psiquiatra** - Reserva de turnos (viernes)
6. **Ver mis turnos** - Consulta y búsqueda por DNI
7. **Pregunta abierta** - IA responde con información del CDC

### Talleres Disponibles:

- 🎨 **TransformArte** - Reciclado creativo (Lun y Jue 18-20hs)
- 🌱 **Amor de Huerta** - Horticultura (Mar y Vie 18:30-20:30, Mié 10:30-12:30)
- 🎭 **Teatro Leído y Escritura** - Expresión (Vie 18-19hs)
- 👥 **Espacio Grupal** - Terapia grupal (Mié 14hs)
- 📻 **Columna Radial** - Difusión en salud mental

---

## 🛠️ Tecnologías

- **Frontend**: Streamlit
- **IA**: Groq (Llama 3.1 8B)
- **RAG**: LangChain + ChromaDB + Sentence Transformers
- **Persistencia**: JSON local
- **Deploy**: Streamlit Cloud

---

## 📦 Instalación Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/PabloPoletti/PruebaCDC.git
cd PruebaCDC
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar API Key de Groq
Crear archivo `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "tu_api_key_aqui"
```

Obtener API Key gratis en: https://console.groq.com/keys

### 4. (Opcional) Agregar imágenes
Guarda las imágenes del CDC en la carpeta `images/`:
- `cdc_frente.jpg` - Foto del frente del Centro
- `logos_institucionales.jpg` - Logos de las instituciones

Ver `images/README.md` para más detalles.

### 5. Ejecutar la aplicación
```bash
streamlit run app.py
```

---

## 🌐 Deploy en Streamlit Cloud

1. Fork este repositorio
2. (Opcional) Agrega las imágenes en la carpeta `images/`
3. Ve a https://share.streamlit.io/
4. Conecta tu repositorio de GitHub
5. Configura el secret `GROQ_API_KEY` en Settings → Secrets
6. Deploy!

---

## 📞 Información del Centro

**Centro de Día Comunitario 25 de Mayo**

- 📍 **Dirección**: Trenel 53, Colonia 25 de Mayo, La Pampa
- 📞 **Teléfono**: 299 4152668
- 📧 **Email**: cdc.25demayolp.coordinacion@gmail.com
- 🌐 **Web**: https://sites.google.com/view/centro-de-da-25-de-mayo/
- 🕒 **Horarios**: Lunes a Viernes - Mañana: 9-13hs | Tarde: 15-18:30hs

### Dependencias Institucionales:
- SEDRONAR (Secretaría de Políticas Integrales sobre Drogas de la Nación)
- Subsecretaría de Salud Mental y Adicciones del Gobierno de La Pampa
- Municipalidad de Colonia 25 de Mayo

---

## 📊 Estructura del Proyecto

```
PruebaCDC/
├── app.py                    # Aplicación principal
├── requirements.txt          # Dependencias
├── data/                     # Datos para RAG
│   ├── info_cdc.txt         # Información del CDC
│   ├── talleres.txt         # Info de talleres
│   └── preguntas_frecuentes.txt
├── images/                   # Imágenes del CDC
│   ├── cdc_frente.jpg       # Foto del frente (opcional)
│   ├── logos_institucionales.jpg  # Logos (opcional)
│   └── README.md            # Instrucciones de imágenes
├── .streamlit/
│   └── config.toml          # Configuración de Streamlit
└── README.md                # Este archivo
```

---

## 🎯 Características del RAG

El bot utiliza RAG (Retrieval-Augmented Generation) con:

- **25+ documentos** de información del CDC
- **Horarios específicos** de todos los servicios y talleres
- **Historia del CDC** (creado el 5 de octubre de 2021)
- **Articulaciones institucionales** (INTA, policía, bomberos, etc.)
- **Logros**: +200 personas atendidas, +500 en talleres

---

## 💰 Costos

**TODO ES GRATIS:**
- ✅ Streamlit Cloud: Gratis (1 app pública)
- ✅ Groq API: Gratis (14,400 requests/día)
- ✅ Modelos de IA: Open source

**Total: $0/mes** 🎉

---

## 📝 Licencia

Este proyecto es de código abierto y está disponible para la comunidad.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

---

## 📧 Contacto

Para consultas sobre el bot o el Centro de Día:
- **Email CDC**: cdc.25demayolp.coordinacion@gmail.com
- **Teléfono**: 299 4152668

---

💚 **Desarrollado para mejorar la atención a la comunidad de 25 de Mayo**

*Última actualización: Noviembre 2025*
