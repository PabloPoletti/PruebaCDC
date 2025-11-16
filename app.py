import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import json

# =====================================================
# CONFIGURACIÓN DE PÁGINA
# =====================================================
st.set_page_config(
    page_title="Centro de Día Comunitario - 25 de Mayo",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =====================================================
# ESTILOS CSS TIPO WHATSAPP
# =====================================================
st.markdown("""
<style>
    /* Fondo general */
    .stApp {
        background-color: #e5ddd5;
        position: relative;
    }
    
    /* Imagen de fondo estilo lienzo (watermark) */
    .stApp > div:first-child {
        background-image: url('https://raw.githubusercontent.com/PabloPoletti/PruebaCDC/main/images/cdc_frente.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        position: relative;
    }
    
    .stApp > div:first-child::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(229, 221, 213, 0.90);
        z-index: 0;
        pointer-events: none;
    }
    
    /* Asegurar que el contenido esté por encima del overlay */
    .stApp > div:first-child > * {
        position: relative;
        z-index: 1;
    }
    
    /* Ocultar menú y footer de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Título principal - contenedor de imagen */
    .main-title {
        padding: 0;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        overflow: hidden;
    }
    
    .main-title img {
        width: 100%;
        height: auto;
        display: block;
        border-radius: 10px;
    }
    
    /* Mensajes del bot */
    .bot-message {
        background-color: white;
        padding: 12px 15px;
        border-radius: 8px;
        margin: 8px 0;
        margin-right: 60px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    
    /* Mensajes del usuario */
    .user-message {
        background-color: #dcf8c6;
        padding: 12px 15px;
        border-radius: 8px;
        margin: 8px 0;
        margin-left: 60px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        text-align: right;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    
    /* Contenedor de chat */
    .chat-container {
        background-color: #e5ddd5;
        padding: 20px;
        border-radius: 10px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* Input de texto */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 1px solid #128C7E;
        padding: 10px 20px;
    }
    
    /* Botón de enviar */
    .stButton > button {
        background-color: #128C7E;
        color: white;
        border-radius: 25px;
        border: none;
        padding: 10px 30px;
        font-weight: bold;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #075E54;
    }
    
    /* Timestamp */
    .timestamp {
        font-size: 11px;
        color: #667781;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# CONFIGURACIÓN GROQ
# =====================================================
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))

if not GROQ_API_KEY:
    st.error("⚠️ No se encontró la API Key de GROQ. Configúrala en Streamlit Secrets.")
    st.stop()

# =====================================================
# INICIALIZAR MODELOS (CACHE)
# =====================================================
@st.cache_resource
def init_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.1,
        max_tokens=150,
        api_key=GROQ_API_KEY
    )

@st.cache_resource
def init_rag():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Cargar archivos de datos externos
    try:
        with open('data/info_cdc.txt', 'r', encoding='utf-8') as f:
            info_cdc = f.read()
        with open('data/talleres.txt', 'r', encoding='utf-8') as f:
            talleres = f.read()
        with open('data/preguntas_frecuentes.txt', 'r', encoding='utf-8') as f:
            preguntas = f.read()
    except:
        # Fallback si no existen los archivos
        info_cdc = talleres = preguntas = ""
    
    INFO_CENTRO = """Centro de Día Comunitario - Colonia 25 de Mayo
Dispositivo Territorial para salud mental y consumos problemáticos
Dependencias: SEDRONAR, Subsecretaría de Salud Mental y Adicciones de La Pampa, Municipalidad de 25 de Mayo"""
    
    HORARIOS = "Lunes a Viernes: Mañana 9 a 13 hs - Tarde 15 a 18:30 hs"
    DIRECCION = "Trenel 53, Colonia 25 de Mayo, La Pampa"
    TELEFONO = "299 4152668"
    EMAIL = "cdc.25demayolp.coordinacion@gmail.com"
    
    DOC_TEXTS = [
        # Información general e histórica
        "El Centro de Día Comunitario de Colonia 25 de Mayo se puso en funcionamiento el 5 de octubre de 2021. Es un dispositivo territorial que aborda problemáticas de salud mental y consumos problemáticos de sustancias. Depende de SEDRONAR, la Subsecretaría de Salud Mental y Adicciones del Gobierno de La Pampa, y la Municipalidad de 25 de Mayo.",
        "El CDC es uno de los efectores de la Red Integrada de Salud Mental y Adicciones con base en la Comunidad, dedicado a la promoción, prevención, tratamiento y principalmente la rehabilitación psicosocial. En poco tiempo ha logrado ser una institución de referencia local y de provincias vecinas.",
        "Desde el inicio, más de 200 personas han recibido atención psicoterapéutica y más de 500 jóvenes y adultos han participado en talleres y actividades de prevención y promoción comunitaria.",
        
        # Ubicación y contacto
        f"Ubicación: Calle Trenel N°53, Colonia 25 de Mayo, La Pampa. Teléfono: {TELEFONO}. Email: {EMAIL}. Horarios: Lunes a viernes, mañana de 9 a 13 hs y tarde de 15 a 18:30 hs.",
        
        # Horarios específicos
        "El Centro atiende de lunes a viernes. Horario de mañana: 9:00 a 13:00 horas. Horario de tarde: 15:00 a 18:30 horas. No atiende sábados ni domingos.",
        "Los lunes el Centro trabaja de 9 a 13 horas y de 15 a 18:30 horas. Los martes de 9 a 13 y de 15 a 18:30. Los miércoles de 9 a 13 y de 15 a 18:30. Los jueves de 9 a 13 y de 15 a 18:30. Los viernes de 9 a 13 y de 15 a 18:30.",
        
        # Servicios
        "El CDC ofrece: abordajes clínicos individuales con nexo en equipos de salud locales, acompañamientos terapéuticos singulares y grupales, seguimientos psicosociales integrales, actividades grupales y comunitarias de prevención y promoción.",
        
        # Atención psiquiátrica
        "Los turnos de psiquiatría se realizan ÚNICAMENTE los viernes por la mañana. El psiquiatra atiende solo los viernes de 9:00 a 13:00 horas. Para sacar turno llamar al 299 4152668 o acercarse al CDC.",
        
        # Atención Profesional
        "Psicoterapia individual: martes, miércoles y viernes de 9:00 a 12:00 horas. Con turno previo llamando al 299 4152668.",
        "Grupos terapéuticos: miércoles a las 14:00 horas. Grupo cerrado con inscripción previa.",
        "Primera Escucha - Demanda espontánea: martes, jueves y viernes de 17:00 a 18:00 horas. Sin turno previo, libre demanda.",
        
        # Talleres con horarios específicos
        "Taller TransformArte (reciclado creativo): lunes y jueves de 18:00 a 20:00 horas. Reciclado creativo donde se aprende a dar segundo uso a diferentes materiales mediante expresión artística.",
        "Taller Amor de Huerta (horticultura): martes y viernes de 18:30 a 20:30 horas, y miércoles de 10:30 a 12:30 horas. Aprendizaje de técnicas de trabajo hortícola en conjunto con otros participantes. Articulación con INTA.",
        "Taller de Teatro Leído y Escritura: viernes de 18:00 a 19:00 horas. Forma parte del proyecto ExpresaMente. Uso de la palabra como medio de expresión y comunicación. Se crea contenido para el Diario Digital 'La Voz del CDC'.",
        "Espacio Grupal terapéutico: miércoles a las 14:00 horas. Espacio para dialogar con otros participantes sobre temas específicos, coordinado por profesional de salud mental.",
        "Columna Radial: programa a cargo del Lic. en Psicología Sebastián Mendicoa sobre diferentes temáticas de salud mental para llegar a la casa de los vecinos.",
        
        # Proyecto La Voz del CDC
        "La Voz del CDC es el diario digital del Centro con el objetivo de promover la salud mental y el bienestar en la comunidad, informar, sensibilizar y fomentar el cuidado de las emociones y abordar el consumo problemático.",
        
        # Modalidad de atención
        "El CDC funciona con libre demanda para primera consulta, no se necesita derivación médica. Para seguimientos se programa turno. Los servicios y talleres son gratuitos.",
        
        # Población objetivo
        "El CDC atiende a personas con problemáticas de salud mental, consumos problemáticos de sustancias, familias y entorno de personas en tratamiento, y realiza actividades de prevención abiertas a toda la comunidad.",
        
        # Enfoque
        "El CDC trabaja con enfoque territorial, integral, comunitario y personalizado. Se generan herramientas acordes a cada persona para potenciar su proyecto de vida.",
        
        # Articulación
        "El CDC articula con equipos de salud locales, hospital, servicios sociales municipales, instituciones educativas, policía, bomberos, Club de Leones, iglesias, INTA (Instituto Nacional de Tecnología Agropecuaria) y diferentes áreas de la municipalidad.",
        "El CDC abre los talleres a toda la comunidad para que sea un lugar de circulación, abierto, accesible y de pertenencia para toda la comunidad, no solo para usuarios con consumos problemáticos o padecimientos mentales.",
        
        # Inscripción talleres
        "Para inscribirse en talleres: acercarse al CDC en horario de atención, llamar al 299 4152668, o enviar email a cdc.25demayolp.coordinacion@gmail.com. Los talleres son gratuitos y los materiales son provistos por el CDC.",
        
        # Información adicional
        "El CDC cuenta con equipo de psicólogos, psiquiatras, acompañantes terapéuticos y talleristas. También tiene programa de bolsa de trabajo para participantes.",
        
        # Datos de archivos externos
        info_cdc,
        talleres,
        preguntas
    ]
    
    docs = [Document(page_content=t) for t in DOC_TEXTS if t.strip()]
    vector_store = Chroma.from_documents(docs, embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    
    return retriever, INFO_CENTRO, HORARIOS, DIRECCION, TELEFONO, EMAIL

llm = init_llm()
retriever, INFO_CENTRO, HORARIOS, DIRECCION, TELEFONO, EMAIL = init_rag()

# =====================================================
# FUNCIONES RAG
# =====================================================
def rag_answer(pregunta):
    docs_recuperados = retriever.invoke(pregunta)
    contexto = "\n".join([doc.page_content for doc in docs_recuperados])
    
    prompt = f"""Usa SOLO la siguiente información para responder:

{contexto}

Pregunta: {pregunta}

Instrucciones:
- Si pregunta por horarios de un día específico, menciona AMBOS turnos (mañana Y tarde)
- Responde en 1-2 oraciones máximo
- Usa solo la información del contexto

Respuesta:"""
    
    try:
        respuesta = llm.invoke(prompt)
        if hasattr(respuesta, 'content'):
            return respuesta.content.strip()
        return str(respuesta).strip()
    except Exception as e:
        return f"Error al generar respuesta: {str(e)}"

# =====================================================
# GESTIÓN DE TURNOS (PERSISTENTE)
# =====================================================
TURNOS_FILE = "turnos_data.json"

def load_turnos():
    """Cargar turnos desde archivo JSON"""
    if os.path.exists(TURNOS_FILE):
        try:
            with open(TURNOS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return pd.DataFrame(data)
        except:
            pass
    return pd.DataFrame(columns=[
        "telefono", "nombre", "dni", "motivo",
        "fecha", "hora", "primera_vez", "timestamp"
    ])

def save_turnos(df):
    """Guardar turnos en archivo JSON"""
    try:
        with open(TURNOS_FILE, 'w', encoding='utf-8') as f:
            json.dump(df.to_dict('records'), f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Error al guardar turnos: {e}")

# =====================================================
# FUNCIONES DE TURNOS
# =====================================================
TURNOS_PSI = ["08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30"]

def get_fridays(n=5):
    hoy = datetime.today()
    fechas = []
    for i in range(1, 60):
        d = hoy + timedelta(days=i)
        if d.weekday() == 4:
            fechas.append(d.strftime("%d/%m/%Y"))
        if len(fechas) == n:
            break
    return fechas

def turnos_libres(fecha):
    turnos_df = load_turnos()
    ocupados = turnos_df[turnos_df["fecha"] == fecha]["hora"].tolist()
    return [h for h in TURNOS_PSI if h not in ocupados]

# =====================================================
# MENÚ PRINCIPAL
# =====================================================
def menu_principal():
    return """

📋 *Menú principal*
Elegí una opción:
1️⃣ ¿Qué es el Centro de Día?
2️⃣ Horarios y Contacto
3️⃣ Servicios que ofrecemos
4️⃣ Talleres disponibles
5️⃣ Pedir turno con psiquiatra
6️⃣ Ver mis turnos
7️⃣ Pregunta abierta (IA)
👉 Escribí el número de la opción."""

# =====================================================
# LÓGICA DEL BOT
# =====================================================
def bot_response(mensaje, user_id):
    """Procesar mensaje y generar respuesta"""
    
    # Inicializar estado del usuario si no existe
    if "user_states" not in st.session_state:
        st.session_state.user_states = {}
    
    if user_id not in st.session_state.user_states:
        st.session_state.user_states[user_id] = {
            "step": "menu",
            "data": {},
            "mis_turnos": []
        }
        return """👋 *Bienvenido/a al Centro de Día Comunitario*
*Colonia 25 de Mayo - La Pampa*

🏥 Espacio de salud mental y consumos problemáticos
💚 Atención gratuita y sin derivación médica
🤝 Te acompañamos en tu proyecto de vida""" + menu_principal()
    
    state = st.session_state.user_states[user_id]
    msg = mensaje.lower().strip()
    raw = mensaje.strip()
    
    # MENÚ PRINCIPAL
    if state["step"] == "menu":
        # 1) ¿Qué es el Centro de Día?
        if msg == "1":
            return INFO_CENTRO + "\n\n" + rag_answer("¿Qué es el Centro de Día y qué hace?") + menu_principal()
        
        # 2) Horarios y Contacto
        if msg == "2":
            return f"""📍 *Ubicación y Contacto*

🏠 Dirección: {DIRECCION}
🕒 Horarios: {HORARIOS}
📞 Teléfono: {TELEFONO}
📧 Email: {EMAIL}
🌐 Web: https://sites.google.com/view/centro-de-da-25-de-mayo/

💡 Podés acercarte sin turno para primera consulta.""" + menu_principal()
        
        # 3) Servicios que ofrecemos
        if msg == "3":
            return """🏥 *Servicios del CDC*

✅ Abordajes clínicos individuales
✅ Acompañamientos terapéuticos
✅ Seguimientos psicosociales
✅ Atención psiquiátrica (viernes)
✅ Atención psicológica
✅ Actividades grupales
✅ Talleres diversos
✅ Bolsa de trabajo

📌 Todos los servicios son gratuitos
📌 No se necesita derivación médica
📌 Primera consulta: libre demanda""" + menu_principal()
        
        # 4) Talleres disponibles
        if msg == "4":
            state["step"] = "talleres_menu"
            return """🎨 *Talleres del CDC*

1️⃣ **TransformArte** - Reciclado creativo
   📅 Lunes y Jueves 18:00-20:00

2️⃣ **Amor de Huerta** - Horticultura
   📅 Martes y Viernes 18:30-20:30
   📅 Miércoles 10:30-12:30

3️⃣ **Teatro Leído y Escritura**
   📅 Viernes 18:00-19:00

4️⃣ **Espacio Grupal** - Terapia grupal
   📅 Miércoles 14:00

5️⃣ **Columna Radial** - Salud mental

📌 Talleres gratuitos
📌 Materiales provistos por el CDC
📌 Inscripción: 299 4152668

💡 Escribí el número del taller para más info
0️⃣ Volver al menú principal"""
        
        # 5) Pedir turno con psiquiatra
        if msg == "5":
            state["step"] = "fecha"
            fechas = get_fridays()
            listado = "\n".join([f"{i+1}) {f}" for i, f in enumerate(fechas)])
            return f"""📅 *Turnos de Psiquiatría*

⏰ Atención: Solo viernes de 9:00 a 13:00 hs

Elegí una fecha:
{listado}

👉 Respondé con el número correspondiente."""
        
        # 6) Ver mis turnos
        if msg == "6":
            mis_turnos = state["mis_turnos"]
            if len(mis_turnos) > 0:
                text = "📋 *Tus turnos registrados:*\n\n"
                for t in mis_turnos:
                    text += f"📅 {t['fecha']} - ⏰ {t['hora']}\n👤 {t['nombre']} (DNI {t['dni']})\n🧠 Motivo: {t['motivo']}\n📌 Primera vez: {t['primera_vez']}\n\n"
                return text + menu_principal()
            
            state["step"] = "buscar_dni_confirm"
            return "📭 No registraste turnos en esta sesión.\n\n¿Querés buscar si ya tenés turnos cargados anteriormente por DNI?\n👉 Respondé *si* o *no*."
        
        # 7) Pregunta abierta (IA)
        if msg == "7":
            state["step"] = "rag"
            return "🧠 Escribí tu pregunta sobre el Centro de Día:"
        
        # Detección automática de preguntas
        palabras_pregunta = ["que", "cual", "cuando", "donde", "como", "quien", "horario", "turno", "psiquiatra", "atiende", "dia", "telefono", "direccion", "taller", "servicio"]
        if any(palabra in msg for palabra in palabras_pregunta) or "?" in raw:
            respuesta = rag_answer(raw)
            return f"🤖 {respuesta}" + menu_principal()
        
        return "❌ Opción inválida. Elegí un número del 1 al 7." + menu_principal()
    
    # RAG
    if state["step"] == "rag":
        respuesta = rag_answer(raw)
        state["step"] = "menu"
        return f"🤖 {respuesta}" + menu_principal()
    
    # MENÚ DE TALLERES DETALLADO
    if state["step"] == "talleres_menu":
        if msg == "0":
            state["step"] = "menu"
            return "Volviendo al menú principal..." + menu_principal()
        
        if msg == "1":
            state["step"] = "menu"
            return """🎨 *TALLER TRANSFORMARTE*
Reciclado creativo y expresión artística

📅 **Horarios:**
• Lunes: 18:00 a 20:00 hs
• Jueves: 18:00 a 20:00 hs

📝 **Descripción:**
Taller donde aprendés a dar segundo uso a diferentes materiales mediante la expresión artística. Trabajamos con papel, cartón, plásticos, telas, madera y vidrio.

🎯 **Actividades:**
• Reciclado de materiales
• Creación de objetos decorativos
• Técnicas de transformación
• Pintura y decoración

✨ **Beneficios:**
• Desarrollo de creatividad
• Conciencia ecológica
• Habilidades manuales
• Posibilidad de generar ingresos

📞 Inscripción: 299 4152668
💚 Taller gratuito con materiales incluidos""" + menu_principal()
        
        if msg == "2":
            state["step"] = "menu"
            return """🌱 *TALLER AMOR DE HUERTA*
Horticultura y cultivo en comunidad

📅 **Horarios:**
• Martes: 18:30 a 20:30 hs
• Miércoles: 10:30 a 12:30 hs
• Viernes: 18:30 a 20:30 hs

📝 **Descripción:**
Aprendé técnicas de cultivo y trabajo en la tierra junto a otros participantes. Trabajo en articulación con INTA.

🎯 **Actividades:**
• Preparación de suelo
• Siembra y trasplante
• Cuidado de plantas
• Cosecha
• Compostaje

✨ **Beneficios:**
• Actividad física al aire libre
• Trabajo en equipo
• Contacto con la naturaleza
• Producción de alimentos saludables

📞 Inscripción: 299 4152668
💚 Taller gratuito con herramientas incluidas""" + menu_principal()
        
        if msg == "3":
            state["step"] = "menu"
            return """🎭 *TALLER DE TEATRO LEÍDO Y ESCRITURA*
Expresión a través del teatro y la palabra

📅 **Horario:**
• Viernes: 18:00 a 19:00 hs

📝 **Descripción:**
Espacio de expresión a través del teatro leído y la escritura creativa. Forma parte del proyecto "ExpresaMente".

🎯 **Actividades:**
• Teatro leído
• Escritura creativa
• Producción de notas para "La Voz del CDC"
• Entrevistas y testimonios

✨ **Beneficios:**
• Desarrollo de habilidades comunicacionales
• Fortalecimiento de autoestima
• Expresión de emociones
• Creación de contenido comunitario

📞 Inscripción: 299 4152668
💚 Taller gratuito""" + menu_principal()
        
        if msg == "4":
            state["step"] = "menu"
            return """👥 *ESPACIO GRUPAL TERAPÉUTICO*
Terapia grupal coordinada por profesional

📅 **Horario:**
• Miércoles: 14:00 hs

📝 **Descripción:**
Espacio terapéutico para dialogar con otros participantes sobre temas específicos, coordinado por profesional de salud mental.

🎯 **Temas abordados:**
• Salud mental
• Consumos problemáticos
• Relaciones interpersonales
• Manejo de emociones
• Proyectos de vida

✨ **Modalidad:**
• Grupo cerrado con inscripción previa
• Confidencialidad y respeto
• Participación voluntaria
• Apoyo mutuo

📞 Inscripción: 299 4152668
💚 Espacio gratuito""" + menu_principal()
        
        if msg == "5":
            state["step"] = "menu"
            return """📻 *COLUMNA RADIAL*
Difusión en salud mental

👨‍⚕️ **Coordinador:**
Lic. en Psicología Sebastián Mendicoa

📝 **Descripción:**
Programa radial sobre diferentes temáticas de salud mental para llegar a la casa de los vecinos.

🎯 **Contenidos:**
• Salud mental
• Prevención de consumos problemáticos
• Recursos comunitarios
• Entrevistas a profesionales
• Testimonios

📡 **Alcance:**
• Difusión radial local
• Publicación en redes sociales
• Archivo disponible en la web

💚 Programa de difusión comunitaria""" + menu_principal()
        
        return "❌ Opción inválida. Elegí un número del 1 al 5, o 0 para volver." + "\n\n" + """🎨 *Talleres del CDC*

1️⃣ TransformArte
2️⃣ Amor de Huerta
3️⃣ Teatro Leído y Escritura
4️⃣ Espacio Grupal
5️⃣ Columna Radial
0️⃣ Volver al menú principal"""
    
    # BUSCAR TURNOS POR DNI
    if state["step"] == "buscar_dni_confirm":
        if msg not in ["si", "no"]:
            return "❌ Respondé *si* o *no*."
        if msg == "no":
            state["step"] = "menu"
            return "Volviendo al menú..." + menu_principal()
        state["step"] = "buscar_dni_dni"
        return "🆔 Ingresá el DNI para buscar turnos anteriores:"
    
    if state["step"] == "buscar_dni_dni":
        turnos_df = load_turnos()
        encontrados = turnos_df[turnos_df["dni"] == raw.strip()]
        state["step"] = "menu"
        
        if encontrados.empty:
            return "❌ No se encontraron turnos con ese DNI." + menu_principal()
        
        text = "📋 *Turnos encontrados:*\n\n"
        for _, row in encontrados.iterrows():
            text += f"📅 {row['fecha']} - ⏰ {row['hora']}\n👤 {row['nombre']} (DNI {row['dni']})\n🧠 {row['motivo']}\n📌 Primera vez: {row['primera_vez']}\n\n"
        return text + menu_principal()
    
    # PROCESO DE TURNOS
    if state["step"] == "fecha":
        try:
            fecha_sel = get_fridays()[int(msg)-1]
        except:
            return "❌ Tenés que elegir un *número* de la lista.\nIntentá de nuevo."
        
        state["data"]["fecha"] = fecha_sel
        libres = turnos_libres(fecha_sel)
        
        if not libres:
            state["step"] = "menu"
            return "📭 No hay turnos disponibles ese día." + menu_principal()
        
        state["step"] = "hora"
        horarios = "\n".join([f"{i+1}) {h}" for i, h in enumerate(libres)])
        return f"📅 Fecha seleccionada: *{fecha_sel}*\n\n⏰ Elegí un horario:\n{horarios}\n\n👉 Respondé con el número del horario."
    
    if state["step"] == "hora":
        libres = turnos_libres(state["data"]["fecha"])
        try:
            hora_sel = libres[int(msg)-1]
        except:
            return "❌ Elegí un número válido."
        state["data"]["hora"] = hora_sel
        state["step"] = "nombre"
        return "👤 Ingresá el *nombre y apellido* del paciente:"
    
    if state["step"] == "nombre":
        state["data"]["nombre"] = raw
        state["step"] = "dni"
        return "🆔 Ingresá el *DNI* del paciente:"
    
    if state["step"] == "dni":
        state["data"]["dni"] = raw
        state["step"] = "motivo"
        return "🧠 Escribí el *motivo de la consulta*:"
    
    if state["step"] == "motivo":
        state["data"]["motivo"] = raw
        state["step"] = "primera"
        return "❓ ¿Es la primera vez que viene? (si/no)"
    
    if state["step"] == "primera":
        if msg not in ["si", "no"]:
            return "❌ Respondé *si* o *no*."
        
        data = state["data"]
        
        # Guardar turno en archivo
        turnos_df = load_turnos()
        nuevo_turno = {
            "telefono": user_id,
            "nombre": data["nombre"],
            "dni": data["dni"],
            "motivo": data["motivo"],
            "fecha": data["fecha"],
            "hora": data["hora"],
            "primera_vez": msg,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        turnos_df = pd.concat([turnos_df, pd.DataFrame([nuevo_turno])], ignore_index=True)
        save_turnos(turnos_df)
        
        # Guardar en sesión del usuario
        state["mis_turnos"].append({
            "fecha": data["fecha"],
            "hora": data["hora"],
            "nombre": data["nombre"],
            "dni": data["dni"],
            "motivo": data["motivo"],
            "primera_vez": msg
        })
        
        state["step"] = "menu"
        
        return f"✅ *Turno registrado exitosamente*\n\n📅 Fecha: {data['fecha']}\n⏰ Hora: {data['hora']}\n👤 Paciente: {data['nombre']}\n🆔 DNI: {data['dni']}\n🧠 Motivo: {data['motivo']}\n📌 Primera vez: {msg}" + menu_principal()
    
    return "❌ Algo salió mal. Volviendo al menú..." + menu_principal()

# =====================================================
# INTERFAZ STREAMLIT
# =====================================================

# Header con imagen (si existe la imagen del header, sino usar título HTML)
if os.path.exists("images/header_cdc.jpg"):
    st.markdown('<div class="main-title">', unsafe_allow_html=True)
    st.image("images/header_cdc.jpg", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="main-title"><h1>🏥 Centro de Día Comunitario</h1><p>25 de Mayo - La Pampa</p></div>', unsafe_allow_html=True)

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensaje de bienvenida automático
    welcome_msg = bot_response("hola", "web_user")
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# Inicializar contador para limpiar input
if "input_counter" not in st.session_state:
    st.session_state.input_counter = 0

# Mostrar historial de chat
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)

# Input del usuario
with st.container():
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input("Escribí tu mensaje...", key=f"user_input_{st.session_state.input_counter}", label_visibility="collapsed")
    
    with col2:
        send_button = st.button("📤 Enviar")

# Procesar mensaje
if send_button and user_input:
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Obtener respuesta del bot
    bot_reply = bot_response(user_input, "web_user")
    
    # Agregar respuesta del bot
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    
    # Incrementar contador para limpiar input
    st.session_state.input_counter += 1
    
    # Recargar para mostrar nuevos mensajes
    st.rerun()

# Botón para reiniciar conversación
if st.button("🔄 Nueva conversación"):
    st.session_state.messages = []
    if "user_states" in st.session_state:
        st.session_state.user_states = {}
    # Reiniciar contador del input
    st.session_state.input_counter = 0
    # Agregar mensaje de bienvenida automático
    welcome_msg = bot_response("hola", "web_user")
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    st.rerun()

# Footer con logos institucionales
st.markdown("---")

# Logos de las instituciones (si existen)
if os.path.exists("images/logos_institucionales.jpg"):
    st.image("images/logos_institucionales.jpg", use_container_width=True)

st.markdown("💚 *Bot de atención automatizada - Centro de Día Comunitario 25 de Mayo*")
st.markdown("*Trabajo conjunto: SEDRONAR, Subsecretaría de Salud Mental y Adicciones de La Pampa, Municipalidad de 25 de Mayo*")

