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
    }
    
    /* Ocultar menú y footer de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Título principal */
    .main-title {
        background: linear-gradient(135deg, #128C7E 0%, #075E54 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
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
    
    INFO_CENTRO = """
Dispositivo Territorial Comunitario
Subsecretaría de Salud Mental y Adicciones del Gobierno de La Pampa
Municipalidad de 25 de Mayo. SEDRONAR.
Secretaría de Políticas Integrales sobre Drogas de la Nación Argentina.
"""
    
    HORARIOS = "Lunes a Viernes de 8 a 13 y 16 a 19"
    DIRECCION = "Trenel 53 - 25 de Mayo (La Pampa)"
    TELEFONO = "0299 524-3358"
    
    DOC_TEXTS = [
        "El Centro de Día Comunitario de 25 de Mayo es un Dispositivo Territorial Comunitario que brinda atención en salud mental y adicciones.",
        "El Centro depende de la Subsecretaría de Salud Mental y Adicciones del Gobierno de La Pampa, la Municipalidad de 25 de Mayo, y SEDRONAR (Secretaría de Políticas Integrales sobre Drogas de la Nación Argentina).",
        f"El Centro atiende de lunes a viernes en dos turnos. Dirección: {DIRECCION}. Teléfono: {TELEFONO}.",
        "Horarios de atención: LUNES de 8 a 13 y de 16 a 19. MARTES de 8 a 13 y de 16 a 19. MIÉRCOLES de 8 a 13 y de 16 a 19. JUEVES de 8 a 13 y de 16 a 19. VIERNES de 8 a 13 y de 16 a 19.",
        "El jueves el Centro trabaja de 8 a 13 horas (mañana) y de 16 a 19 horas (tarde). Son dos turnos: mañana y tarde.",
        "Los turnos de psiquiatría se realizan ÚNICAMENTE los viernes por la mañana de 8:00 a 11:30. El psiquiatra solo atiende los viernes.",
        "El Centro articula con el Municipio, la Subsecretaría de Salud Mental y SEDRONAR para brindar atención integral.",
        "El Centro ofrece servicios de salud mental, atención psiquiátrica, y abordaje de problemáticas de adicciones en la comunidad de 25 de Mayo.",
        "Todos los días de la semana (lunes a viernes) el Centro tiene horario de mañana (8 a 13) y horario de tarde (16 a 19)."
    ]
    
    docs = [Document(page_content=t) for t in DOC_TEXTS]
    vector_store = Chroma.from_documents(docs, embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    return retriever, INFO_CENTRO, HORARIOS, DIRECCION, TELEFONO

llm = init_llm()
retriever, INFO_CENTRO, HORARIOS, DIRECCION, TELEFONO = init_rag()

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
1️⃣ Sobre el Centro
2️⃣ Horarios / Dirección / Teléfono
3️⃣ Pedir turno con psiquiatra
4️⃣ Ver turnos registrados
5️⃣ Pregunta abierta (IA + RAG)
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
        return "👋 *Bienvenido/a al Centro de Día Comunitario 25 de Mayo*" + menu_principal()
    
    state = st.session_state.user_states[user_id]
    msg = mensaje.lower().strip()
    raw = mensaje.strip()
    
    # MENÚ PRINCIPAL
    if state["step"] == "menu":
        if msg == "1":
            return INFO_CENTRO + menu_principal()
        
        if msg == "2":
            return f"📍 Dirección: {DIRECCION}\n🕒 Horarios: {HORARIOS}\n📞 Teléfono: {TELEFONO}" + menu_principal()
        
        if msg == "3":
            state["step"] = "fecha"
            fechas = get_fridays()
            listado = "\n".join([f"{i+1}) {f}" for i, f in enumerate(fechas)])
            return f"📅 *Turnos de psiquiatría*\n\nLos turnos son *solo los viernes por la mañana*.\n\nElegí una fecha:\n{listado}\n\n👉 Respondé con el número correspondiente."
        
        if msg == "4":
            mis_turnos = state["mis_turnos"]
            if len(mis_turnos) > 0:
                text = "📋 *Tus turnos en esta sesión:*\n\n"
                for t in mis_turnos:
                    text += f"📅 {t['fecha']} - ⏰ {t['hora']}\n👤 {t['nombre']} (DNI {t['dni']})\n🧠 Motivo: {t['motivo']}\n📌 Primera vez: {t['primera_vez']}\n\n"
                return text + menu_principal()
            
            state["step"] = "buscar_dni_confirm"
            return "📭 No registraste turnos en esta sesión.\n\n¿Querés buscar si ya tenés turnos cargados anteriormente por DNI?\n👉 Respondé *si* o *no*."
        
        if msg == "5":
            state["step"] = "rag"
            return "🧠 Escribí tu pregunta sobre el Centro de Día:"
        
        # Detección automática de preguntas
        palabras_pregunta = ["que", "cual", "cuando", "donde", "como", "quien", "horario", "turno", "psiquiatra", "atiende", "dia", "telefono", "direccion"]
        if any(palabra in msg for palabra in palabras_pregunta) or "?" in raw:
            respuesta = rag_answer(raw)
            return f"🤖 {respuesta}" + menu_principal()
        
        return "❌ Opción inválida. Elegí un número del 1 al 5." + menu_principal()
    
    # RAG
    if state["step"] == "rag":
        respuesta = rag_answer(raw)
        state["step"] = "menu"
        return f"🤖 {respuesta}" + menu_principal()
    
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

# Título
st.markdown('<div class="main-title"><h1>🏥 Centro de Día Comunitario</h1><p>25 de Mayo - La Pampa</p></div>', unsafe_allow_html=True)

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensaje de bienvenida automático
    welcome_msg = bot_response("hola", "web_user")
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

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
        user_input = st.text_input("Escribí tu mensaje...", key="user_input", label_visibility="collapsed")
    
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
    
    # Recargar para mostrar nuevos mensajes
    st.rerun()

# Botón para reiniciar conversación
if st.button("🔄 Nueva conversación"):
    st.session_state.messages = []
    if "user_states" in st.session_state:
        st.session_state.user_states = {}
    st.rerun()

# Footer
st.markdown("---")
st.markdown("💚 *Bot de atención automatizada - Centro de Día Comunitario 25 de Mayo*")

