!pip install -q langchain langchain-groq chromadb sentence-transformers

# =====================================================
#        BOT INTERACTIVO + RAG + GROQ (RÁPIDO)
# =====================================================

import pandas as pd
from datetime import datetime, timedelta
import os

# =====================================================
# 1) Configurar API Key de GROQ (GRATIS)
# =====================================================
# Obtén tu API key gratis en: https://console.groq.com/keys

GROQ_API_KEY = "TU_API_KEY_AQUI"  # ← Reemplaza con tu key
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# =====================================================
# 2) Cargar LLM (GROQ - súper rápido)
# =====================================================

from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.1,
    max_tokens=150
)
print("🤖 Modelo Groq cargado correctamente (respuestas en 1-3 segundos).")


# =====================================================
# 3) RAG con embeddings + Chroma
# =====================================================

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
print("🔤 Embeddings cargados.")


# =====================================================
# Documentos del CDC
# =====================================================

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

def rag_answer(pregunta):
    # Recuperar documentos relevantes
    docs_recuperados = retriever.invoke(pregunta)
    
    # Construir contexto con los documentos recuperados
    contexto = "\n".join([doc.page_content for doc in docs_recuperados])
    
    # Crear prompt optimizado con instrucciones claras
    prompt = f"""Usa SOLO la siguiente información para responder:

{contexto}

Pregunta: {pregunta}

Instrucciones:
- Si pregunta por horarios de un día específico, menciona AMBOS turnos (mañana Y tarde)
- Responde en 1-2 oraciones máximo
- Usa solo la información del contexto

Respuesta:"""
    
    # Llamar al LLM directamente
    try:
        respuesta = llm.invoke(prompt)
        # ChatGroq devuelve un objeto AIMessage, extraer el contenido
        if hasattr(respuesta, 'content'):
            return respuesta.content.strip()
        return str(respuesta).strip()
    except Exception as e:
        return f"Error al generar respuesta: {str(e)}"





# =====================================================
# 4) Estado del usuario + turnos (como Google Sheets)
# =====================================================

turnos_df = pd.DataFrame(columns=[
    "telefono","nombre","dni","motivo",
    "fecha","hora","primera_vez","timestamp"
])

user_state = {}

TURNOS_PSI = ["08:00","08:30","09:00","09:30","10:00","10:30","11:00","11:30"]


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
    ocupados = turnos_df[turnos_df["fecha"] == fecha]["hora"].tolist()
    return [h for h in TURNOS_PSI if h not in ocupados]


# =====================================================
# 5) BOT PRINCIPAL (SIN GLOBAL) ✔✔✔
# =====================================================

def menu_principal():
    return (
        "\n\n📋 *Menú principal*\n"
        "Elegí una opción:\n"
        "1️⃣ Sobre el Centro\n"
        "2️⃣ Horarios / Dirección / Teléfono\n"
        "3️⃣ Pedir turno con psiquiatra\n"
        "4️⃣ Ver turnos registrados\n"
        "5️⃣ Pregunta abierta (IA + RAG)\n"
        "👉 Escribí el número de la opción."
    )


def bot(telefono, mensaje):
    msg = mensaje.lower().strip()
    raw = mensaje.strip()

    # PRIMER MENSAJE
    if telefono not in user_state:
        user_state[telefono] = {
            "step": "menu",
            "data": {},
            "mis_turnos": []  # turnos creados en esta sesión
        }
        return (
            "👋 *Bienvenido/a al Centro de Día Comunitario 25 de Mayo*"
            + menu_principal()
        )

    state = user_state[telefono]


    # ==================================================================
    #                           MENÚ PRINCIPAL
    # ==================================================================
    if state["step"] == "menu":

        # 1) SOBRE EL CENTRO
        if msg == "1":
            return INFO_CENTRO + menu_principal()

        # 2) Horarios, dirección, teléfono
        if msg == "2":
            return (
                f"📍 Dirección: {DIRECCION}\n"
                f"🕒 Horarios: {HORARIOS}\n"
                f"📞 Teléfono: {TELEFONO}"
                + menu_principal()
            )

        # 3) Pedir turno
        if msg == "3":
            state["step"] = "fecha"
            fechas = get_fridays()
            listado = "\n".join([f"{i+1}) {f}" for i, f in enumerate(fechas)])
            return (
                "📅 *Turnos de psiquiatría*\n\n"
                "Los turnos son *solo los viernes por la mañana*.\n\n"
                "Elegí una fecha:\n"
                f"{listado}\n\n"
                "👉 Respondé con el número correspondiente."
            )

        # 4) Ver turnos
        if msg == "4":
            mis_turnos = state["mis_turnos"]

            if len(mis_turnos) > 0:
                text = "📋 *Tus turnos en esta sesión:*\n\n"
                for t in mis_turnos:
                    text += (
                        f"📅 {t['fecha']} - ⏰ {t['hora']}\n"
                        f"👤 {t['nombre']} (DNI {t['dni']})\n"
                        f"🧠 Motivo: {t['motivo']}\n"
                        f"📌 Primera vez: {t['primera_vez']}\n\n"
                    )
                return text + menu_principal()

            # No tiene turnos → preguntar si buscar por DNI
            state["step"] = "buscar_dni_confirm"
            return (
                "📭 No registraste turnos en esta sesión.\n\n"
                "¿Querés buscar si ya tenés turnos cargados anteriormente por DNI?\n"
                "👉 Respondé *si* o *no*."
            )

        # 5) RAG
        if msg == "5":
            state["step"] = "rag"
            return "🧠 Escribí tu pregunta sobre el Centro de Día:"

        # Si no es un número del 1-5, detectar si es una pregunta
        # Palabras clave que indican pregunta
        palabras_pregunta = ["que", "cual", "cuando", "donde", "como", "quien", "horario", "turno", "psiquiatra", "atiende", "dia", "telefono", "direccion"]
        
        if any(palabra in msg for palabra in palabras_pregunta) or "?" in raw:
            # Es una pregunta → responder con RAG directamente
            respuesta = rag_answer(raw)
            return f"🤖 {respuesta}" + menu_principal()

        return "❌ Opción inválida. Elegí un número del 1 al 5." + menu_principal()


    # ==================================================================
    #                              RAG
    # ==================================================================
    if state["step"] == "rag":
        respuesta = rag_answer(raw)
        state["step"] = "menu"
        return f"🤖 {respuesta}" + menu_principal()


    # ==================================================================
    #                          BUSCAR TURNOS POR DNI
    # ==================================================================
    if state["step"] == "buscar_dni_confirm":
        if msg not in ["si", "no"]:
            return "❌ Respondé *si* o *no*."

        if msg == "no":
            state["step"] = "menu"
            return "Volviendo al menú..." + menu_principal()

        state["step"] = "buscar_dni_dni"
        return "🆔 Ingresá el DNI para buscar turnos anteriores:"


    if state["step"] == "buscar_dni_dni":
        dni_buscar = raw.strip()
        encontrados = turnos_df[turnos_df["dni"] == dni_buscar]

        state["step"] = "menu"

        if encontrados.empty:
            return "❌ No se encontraron turnos con ese DNI." + menu_principal()

        text = "📋 *Turnos encontrados:*\n\n"
        for _, row in encontrados.iterrows():
            text += (
                f"📅 {row['fecha']} - ⏰ {row['hora']}\n"
                f"👤 {row['nombre']} (DNI {row['dni']})\n"
                f"🧠 {row['motivo']}\n"
                f"📌 Primera vez: {row['primera_vez']}\n\n"
            )

        return text + menu_principal()


    # ==================================================================
    #                              TURNOS
    # ==================================================================

    # FECHA
    if state["step"] == "fecha":
        try:
            fecha_sel = get_fridays()[int(msg)-1]
        except:
            return (
                "❌ Tenés que elegir un *número* de la lista.\n"
                "Intentá de nuevo."
            )

        state["data"]["fecha"] = fecha_sel

        libres = turnos_libres(fecha_sel)
        if not libres:
            state["step"] = "menu"
            return "📭 No hay turnos disponibles ese día." + menu_principal()

        state["step"] = "hora"
        horarios = "\n".join([f"{i+1}) {h}" for i, h in enumerate(libres)])
        return (
            f"📅 Fecha seleccionada: *{fecha_sel}*\n\n"
            "⏰ Elegí un horario:\n"
            f"{horarios}\n\n👉 Respondé con el número del horario."
        )


    # HORA
    if state["step"] == "hora":
        libres = turnos_libres(state["data"]["fecha"])
        try:
            hora_sel = libres[int(msg)-1]
        except:
            return "❌ Elegí un número válido."

        state["data"]["hora"] = hora_sel
        state["step"] = "nombre"
        return "👤 Ingresá el *nombre y apellido* del paciente:"


    # NOMBRE
    if state["step"] == "nombre":
        state["data"]["nombre"] = raw
        state["step"] = "dni"
        return "🆔 Ingresá el *DNI* del paciente:"


    # DNI
    if state["step"] == "dni":
        state["data"]["dni"] = raw
        state["step"] = "motivo"
        return "🧠 Escribí el *motivo de la consulta*:"


    # MOTIVO
    if state["step"] == "motivo":
        state["data"]["motivo"] = raw
        state["step"] = "primera"
        return "❓ ¿Es la primera vez que viene? (si/no)"


    # PRIMERA VEZ
    if state["step"] == "primera":
        if msg not in ["si", "no"]:
            return "❌ Respondé *si* o *no*."

        data = state["data"]

        # Guardar turno en turnos_df
        turnos_df.loc[len(turnos_df)] = {
            "telefono": telefono,
            "nombre": data["nombre"],
            "dni": data["dni"],
            "motivo": data["motivo"],
            "fecha": data["fecha"],
            "hora": data["hora"],
            "primera_vez": msg,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Guardar turno en la sesión
        user_state[telefono]["mis_turnos"].append({
            "fecha": data["fecha"],
            "hora": data["hora"],
            "nombre": data["nombre"],
            "dni": data["dni"],
            "motivo": data["motivo"],
            "primera_vez": msg
        })

        state["step"] = "menu"

        return (
            "✅ *Turno registrado exitosamente*\n\n"
            f"📅 Fecha: {data['fecha']}\n"
            f"⏰ Hora: {data['hora']}\n"
            f"👤 Paciente: {data['nombre']}\n"
            f"🆔 DNI: {data['dni']}\n"
            f"🧠 Motivo: {data['motivo']}\n"
            f"📌 Primera vez: {msg}"
            + menu_principal()
        )



# =====================================================
# 6) LOOP DE CHAT (SIMULACIÓN WHATSAPP)
# =====================================================

def chat():
    tel = input("📱 Número (WhatsApp simulado): +")
    print("\nBOT:", bot(tel, "hola"))
    while True:
        msg = input("Vos: ")
        print("BOT:", bot(tel, msg))

chat()

