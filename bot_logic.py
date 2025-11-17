"""
Lógica del bot CDC - Solo la funcionalidad core
Sin Streamlit, sin UI, solo procesamiento
"""

import os
import json
import pandas as pd
from datetime import datetime, timedelta
from langchain_groq import ChatGroq

# =====================================================
# CONFIGURACIÓN
# =====================================================

INFO_CENTRO = """El Centro de Día Comunitario de 25 de Mayo es un dispositivo territorial comunitario 
que brinda atención en salud mental y adicciones. Depende de la Subsecretaría de Salud Mental y 
Adicciones del Gobierno de La Pampa, la Municipalidad de 25 de Mayo y SEDRONAR."""

HORARIOS = """Lunes a Viernes:
• Mañana: 9:00 a 13:00 hs
• Tarde: 15:00 a 18:30 hs"""

DIRECCION = "Trenel 53, Colonia 25 de Mayo, La Pampa"
TELEFONO = "299 4152668"
EMAIL = "cdc.25demayolp.coordinacion@gmail.com"

# Datos en memoria para los documentos del RAG
DOC_TEXTS = [
    # Información institucional
    {"title": "Centro de Día Comunitario", "content": INFO_CENTRO},
    {"title": "Horarios", "content": HORARIOS},
    {"title": "Contacto", "content": f"Dirección: {DIRECCION}\nTeléfono: {TELEFONO}\nEmail: {EMAIL}"},
    
    # Historia del CDC
    {"title": "Fundación", "content": """El Centro de Día Comunitario se puso en funcionamiento el 5 de octubre de 2021 
    como parte del trabajo conjunto entre la municipalidad, provincia y nación para dar respuesta específica en materia 
    de consumos problemáticos y salud mental en 25 de Mayo."""},
    
    # Servicios
    {"title": "Atención profesional", "content": """Servicios de atención profesional:
    - Psicoterapia individual: Martes, miércoles y viernes de 9 a 12 hs
    - Grupos terapéuticos: Miércoles 14 hs
    - Primera Escucha (demanda espontánea): Martes, jueves y viernes de 17:00 a 18:00 hs
    - Psiquiatría: Viernes por la mañana (requiere turno previo)"""},
    
    # Talleres
    {"title": "Talleres", "content": """Talleres disponibles en el CDC:
    1. TransformArte (reciclado creativo): Lunes y jueves 18:00 a 20:00 hs
    2. Amor de Huerta (horticultura): Martes y viernes 18:30 a 20:30 hs, Miércoles 10:30 a 12:30 hs
    3. Teatro Leído y Escritura: Viernes 18:00 a 19:00 hs
    4. Espacio Grupal (terapia grupal): Miércoles 14:00 hs
    5. Columna Radial: Difusión en salud mental"""},
]

# Estado de usuarios (en memoria)
USER_STATES = {}

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def load_turnos():
    """Carga turnos desde archivo JSON"""
    if os.path.exists("turnos_data.json"):
        try:
            with open("turnos_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return pd.DataFrame(data)
        except:
            return pd.DataFrame(columns=["telefono", "nombre", "dni", "motivo", "fecha", "hora", "primera_vez", "timestamp"])
    return pd.DataFrame(columns=["telefono", "nombre", "dni", "motivo", "fecha", "hora", "primera_vez", "timestamp"])

def save_turnos(df):
    """Guarda turnos en archivo JSON"""
    with open("turnos_data.json", "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, ensure_ascii=False, indent=2)

def get_user_state(user_id):
    """Obtiene o crea el estado de un usuario"""
    if user_id not in USER_STATES:
        USER_STATES[user_id] = {
            "step": "menu",
            "mis_turnos": [],
            "data": {}
        }
    return USER_STATES[user_id]

def init_rag():
    """Inicializa el sistema RAG ULTRA LIGERO (búsqueda en texto, sin embeddings)"""
    try:
        # Inicializar LLM
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY no configurada")
        
        llm = ChatGroq(
            api_key=groq_api_key,
            model="llama-3.1-8b-instant",
            temperature=0.3,
            max_tokens=500
        )
        
        # Crear base de conocimiento simple (lista de textos)
        knowledge_base = []
        
        # Agregar documentos base
        for doc in DOC_TEXTS:
            knowledge_base.append(doc["content"])
        
        # Cargar archivos de data si existen
        data_files = ["info_cdc.txt", "talleres.txt", "preguntas_frecuentes.txt"]
        for filename in data_files:
            filepath = f"data/{filename}"
            if os.path.exists(filepath):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        knowledge_base.append(content)
                except:
                    pass
        
        return llm, knowledge_base, INFO_CENTRO, HORARIOS, DIRECCION, TELEFONO, EMAIL
    
    except Exception as e:
        print(f"Error inicializando RAG: {e}")
        return None, [], INFO_CENTRO, HORARIOS, DIRECCION, TELEFONO, EMAIL

def rag_answer(query, llm, knowledge_base):
    """Responde usando RAG ULTRA LIGERO (búsqueda simple por keywords)"""
    if not llm or not knowledge_base:
        return "⚠️ El sistema de respuestas inteligentes no está disponible temporalmente."
    
    try:
        # Búsqueda simple: encontrar textos que contengan palabras de la query
        query_lower = query.lower()
        relevant_texts = []
        
        for text in knowledge_base:
            text_lower = text.lower()
            # Contar coincidencias de palabras
            query_words = query_lower.split()
            matches = sum(1 for word in query_words if len(word) > 3 and word in text_lower)
            if matches > 0:
                relevant_texts.append((matches, text))
        
        # Ordenar por relevancia y tomar los top 3
        relevant_texts.sort(reverse=True, key=lambda x: x[0])
        context = "\n\n".join([text for _, text in relevant_texts[:3]])
        
        # Si no hay contexto relevante, usar info general
        if not context:
            context = INFO_CENTRO + "\n\n" + HORARIOS
        
        prompt = f"""Sos un asistente del Centro de Día Comunitario de 25 de Mayo.
Respondé la pregunta usando SOLO esta información:

{context}

Pregunta: {query}

Respuesta (máximo 3 oraciones, directo al punto):"""
        
        response = llm.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        print(f"Error en RAG: {e}")
        return "❌ Error procesando la consulta."

def menu_principal():
    """Genera el menú principal"""
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

👉 Escribí el número de la opción.
"""

def bot_response(raw, user_id):
    """Procesa mensaje y genera respuesta"""
    msg = raw.strip().lower()
    state = get_user_state(user_id)
    
    # Detección automática de preguntas
    question_keywords = ["qué", "que", "cómo", "como", "cuándo", "cuando", "dónde", "donde", 
                         "por qué", "porque", "cuál", "cual", "quién", "quien", "horario", 
                         "taller", "turno", "atencion", "ayuda"]
    
    is_question = "?" in raw or any(kw in msg for kw in question_keywords)
    
    if state["step"] == "menu" and (msg == "hola" or not raw):
        return f"👋 *Bienvenido/a al Centro de Día Comunitario 25 de Mayo*{menu_principal()}"
    
    if state["step"] == "menu":
        if msg in ["1", "uno"]:
            return f"{INFO_CENTRO}{menu_principal()}"
        elif msg in ["2", "dos"]:
            return f"📍 {DIRECCION}\n📞 {TELEFONO}\n📧 {EMAIL}\n\n⏰ {HORARIOS}{menu_principal()}"
        elif msg in ["3", "tres"]:
            return f"""🏥 *Servicios gratuitos del CDC:*

• Atención psicológica individual
• Atención psiquiátrica
• Grupos terapéuticos
• Primera escucha (demanda espontánea)
• Talleres socio-terapéuticos
• Capacitaciones
• Articulaciones institucionales{menu_principal()}"""
        elif msg in ["4", "cuatro"]:
            return """🎨 *Talleres disponibles:*

1. TransformArte (reciclado): Lun y Jue 18-20hs
2. Amor de Huerta: Mar y Vie 18:30-20:30, Mié 10:30-12:30
3. Teatro y Escritura: Vie 18-19hs
4. Espacio Grupal: Mié 14hs
5. Columna Radial

👉 Todos los talleres son gratuitos y abiertos a la comunidad.""" + menu_principal()
        elif msg in ["5", "cinco"]:
            state["step"] = "turno"
            return "📅 *Sistema de turnos con psiquiatra*\n\nLos turnos son los viernes por la mañana.\n\n👉 Escribí el número de la opción."
        elif msg in ["6", "seis"]:
            if state["mis_turnos"]:
                turnos_text = "\n\n".join([
                    f"📅 {t['fecha']} {t['hora']}\n👤 {t['nombre']}\n🧠 {t['motivo']}"
                    for t in state["mis_turnos"]
                ])
                return f"📋 *Tus turnos:*\n\n{turnos_text}{menu_principal()}"
            else:
                return f"❌ No tenés turnos registrados.{menu_principal()}"
        elif msg in ["7", "siete"] or is_question:
            # Inicializar RAG si no está
            if not hasattr(bot_response, 'llm'):
                bot_response.llm, bot_response.knowledge_base, _, _, _, _, _ = init_rag()
            
            if is_question and msg not in ["7", "siete"]:
                answer = rag_answer(raw, bot_response.llm, bot_response.knowledge_base)
                return f"🤖 {answer}{menu_principal()}"
            else:
                state["step"] = "rag"
                return "🧠 Escribí tu pregunta sobre el Centro de Día:"
        else:
            return f"❌ Opción inválida. Elegí un número del 1 al 7.{menu_principal()}"
    
    if state["step"] == "rag":
        if not hasattr(bot_response, 'llm'):
            bot_response.llm, bot_response.knowledge_base, _, _, _, _, _ = init_rag()
        
        answer = rag_answer(raw, bot_response.llm, bot_response.knowledge_base)
        state["step"] = "menu"
        return f"🤖 {answer}{menu_principal()}"
    
    # Manejo de turnos (simplificado)
    if state["step"] == "turno":
        # Aquí iría la lógica completa de turnos
        # Por ahora, retornar al menú
        state["step"] = "menu"
        return f"🚧 Sistema de turnos en desarrollo.{menu_principal()}"
    
    return f"❌ No entendí tu mensaje.{menu_principal()}"

# Inicializar RAG al importar
print("Inicializando sistema RAG...")
try:
    bot_response.llm, bot_response.knowledge_base, _, _, _, _, _ = init_rag()
    print("✅ Sistema RAG inicializado correctamente")
except Exception as e:
    print(f"⚠️ Error al inicializar RAG: {e}")
    bot_response.llm = None
    bot_response.knowledge_base = []

