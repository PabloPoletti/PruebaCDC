!pip install -q langchain langchain-community chromadb sentence-transformers

# =====================================================
#        BOT INTERACTIVO + RAG + OLLAMA
# =====================================================

import subprocess, time, requests
import pandas as pd
from datetime import datetime, timedelta

# =====================================================
# 1) Detectar si OLLAMA está corriendo
# =====================================================

def ollama_running():
    try:
        requests.get("http://localhost:11434/api/tags")
        return True
    except:
        return False

if not ollama_running():
    print("🔄 Iniciando Ollama server…")
    subprocess.Popen(["ollama", "serve"])
    time.sleep(5)
else:
    print("✅ Ollama ya está corriendo.")


# =====================================================
# 2) Cargar LLM (wrapper correcto)
# =====================================================

from langchain_community.llms import Ollama

llm = Ollama(
    model="llama3.2",
    temperature=0.1,
    num_predict=100,
    num_ctx=512,
    repeat_penalty=1.1
)
print("🤖 Modelo Llama3.2 cargado correctamente.")


# =====================================================
# 3) RAG con embeddings + Chroma
# =====================================================

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain.chains import RetrievalQA

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
    f"El Centro atiende de lunes a viernes. Horarios: lunes 8 a 13 y 16 a 19, martes 8 a 13 y 16 a 19, miércoles 8 a 13 y 16 a 19, jueves 8 a 13 y 16 a 19, viernes 8 a 13 y 16 a 19. Dirección: {DIRECCION}. Teléfono: {TELEFONO}.",
    "Los turnos de psiquiatría se realizan solo los viernes por la mañana de 8:00 a 11:30.",
    "El Centro articula con el Municipio, la Subsecretaría de Salud Mental y SEDRONAR para brindar atención integral.",
    "El Centro ofrece servicios de salud mental, atención psiquiátrica, y abordaje de problemáticas de adicciones en la comunidad de 25 de Mayo.",
    f"Días de atención: lunes, martes, miércoles, jueves y viernes. Horario de mañana: 8 a 13 horas. Horario de tarde: 16 a 19 horas."
]

docs = [Document(page_content=t) for t in DOC_TEXTS]

vector_store = Chroma.from_documents(docs, embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

def rag_answer(pregunta):
    # Recuperar documentos relevantes
    docs_recuperados = retriever.invoke(pregunta)
    
    # Construir contexto con los documentos recuperados
    contexto = "\n".join([doc.page_content for doc in docs_recuperados])
    
    # Crear prompt ultra-optimizado para respuestas rápidas
    prompt = f"""Contexto: {contexto}

Pregunta: {pregunta}

Responde en 1-2 oraciones usando solo el contexto:"""
    
    # Llamar al LLM directamente
    try:
        respuesta = llm.invoke(prompt)
        return respuesta.strip()
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
