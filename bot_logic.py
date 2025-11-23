"""
Lógica del bot CDC - Solo la funcionalidad core
Sin Streamlit, sin UI, solo procesamiento
"""

import os
import json
import pandas as pd
from datetime import datetime, timedelta
from langchain_groq import ChatGroq
import config
from db_manager import (
    guardar_turno_db,
    get_turnos_usuario_db,
    get_turnos_ocupados_db
)

# Importar gestor de Google Sheets (renombrado para uso híbrido)
try:
    from sheets_manager import (
        get_turnos_disponibles as get_turnos_disponibles_sheet,
        get_turnos_usuario as get_turnos_usuario_sheet,
        get_proximos_viernes,
        guardar_turno as guardar_turno_sheet,
        cancelar_turno as cancelar_turno_sheet,
        verificar_conexion as verificar_sheets
    )
    SHEETS_DISPONIBLE = True
    print("✅ Módulo sheets_manager importado correctamente")
except ImportError as e:
    print(f"⚠️ No se pudo importar sheets_manager: {e}")
    SHEETS_DISPONIBLE = False

# =====================================================
# CONFIGURACIÓN (Importada de config.py)
# =====================================================

INFO_CENTRO = config.INFO_CENTRO
HORARIOS = config.HORARIOS
DIRECCION = config.DIRECCION
TELEFONO = config.TELEFONO
EMAIL = config.EMAIL
DOC_TEXTS = config.DOC_TEXTS

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

# =====================================================
# FUNCIONES HÍBRIDAS (DB + SHEETS)
# =====================================================

def guardar_turno_hibrido(telefono, nombre, dni, motivo, fecha, hora, primera_vez):
    """Guarda turno en Supabase Y en Google Sheets"""
    # 1. Intentar guardar en Supabase (Prioridad)
    db_success = guardar_turno_db(telefono, nombre, dni, motivo, fecha, hora, primera_vez)
    
    # 2. Intentar guardar en Sheets (Espejo)
    sheet_success = False
    if SHEETS_DISPONIBLE:
        sheet_success = guardar_turno_sheet(telefono, nombre, dni, motivo, fecha, hora, primera_vez)
    
    # Retornar True si al menos uno funcionó
    return db_success or sheet_success

def get_turnos_usuario_hibrido(telefono):
    """Obtiene turnos de Supabase o Sheets"""
    # Intentar DB primero
    turnos = get_turnos_usuario_db(telefono)
    if turnos:
        return turnos
        
    # Fallback a Sheets
    if SHEETS_DISPONIBLE:
        return get_turnos_usuario_sheet(telefono)
    
    return []

def get_turnos_disponibles_hibrido(fecha):
    """Obtiene turnos disponibles combinando fuentes"""
    # Por ahora usamos la lógica de Sheets que ya tiene los horarios definidos
    # Idealmente mover la lista de horarios a config.py
    if SHEETS_DISPONIBLE:
        return get_turnos_disponibles_sheet(fecha)
    return []

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
    
    # Detección de comando "volver al menú" en cualquier momento
    if msg in ["0", "menu", "menú", "volver", "inicio"]:
        state["step"] = "menu"
        return menu_principal()
    
    # Detección automática de preguntas
    question_keywords = ["qué", "que", "cómo", "como", "cuándo", "cuando", "dónde", "donde", 
                         "por qué", "porque", "cuál", "cual", "quién", "quien", "horario", 
                         "taller", "turno", "atencion", "ayuda"]
    
    is_question = "?" in raw or any(kw in msg for kw in question_keywords)
    
    if state["step"] == "menu" and (msg == "hola" or not raw):
        return f"👋 *Bienvenido/a al Centro de Día Comunitario 25 de Mayo*{menu_principal()}"
    
    if state["step"] == "menu":
        if msg in ["1", "uno"]:
            return f"{INFO_CENTRO}\n\n_Escribí *0* o *menú* para volver al menú principal._"
        elif msg in ["2", "dos"]:
            return f"📍 *Ubicación y Contacto*\n\n🏠 Dirección: {DIRECCION}\n📞 Teléfono: {TELEFONO}\n📧 Email: {EMAIL}\n\n⏰ *Horarios:*\n{HORARIOS}\n\n💡 Podés acercarte sin turno para primera consulta.\n\n_Escribí *0* o *menú* para volver al menú principal._"
        elif msg in ["3", "tres"]:
            return f"""🏥 *Servicios y Dispositivos del CDC:*

✅ Acompañamiento para personas en situación de consumos problemáticos
✅ Dispositivo grupal quincenal para familiares de personas con consumos
✅ Talleres con modalidad terapéutica
✅ Espacios grupales de salud mental
✅ Psicoterapia individual según evaluación y disponibilidad
✅ Acompañamiento psiquiátrico (viernes por la mañana)
✅ Primera escucha con el equipo profesional

📌 Todos los servicios son gratuitos
📌 No se necesita derivación médica
📌 Atención para mayores de 13 años

_Escribí *0* o *menú* para volver al menú principal._"""
        elif msg in ["4", "cuatro"]:
            state["step"] = "talleres_menu"
            return """🎨 *Talleres del CDC*

1️⃣ *TransformArte* - Reciclado creativo
   📅 Lunes y Jueves 18:00-20:00 hs
   ♻️ Transformamos materiales reciclables en arte

2️⃣ *Amor de Huerta* - Horticultura
   📅 Martes y Viernes 18:30-20:30 hs
   📅 Miércoles 10:30-12:30 hs
   🌱 Cultivamos alimentos y bienestar

3️⃣ *Teatro Leído y Escritura*
   📅 Viernes 18:00-19:00 hs
   🎭 Expresión a través del arte escénico

4️⃣ *Espacio Grupal* - Terapia grupal
   📅 Miércoles 14:00 hs
   💬 Acompañamiento terapéutico grupal

5️⃣ *Columna Radial*
   📻 Radio municipal - Lunes 11:00 hs

👉 Escribí el número para más información, o *0* para volver al menú."""
        elif msg in ["5", "cinco"]:
            state["step"] = "turno"
            return "📅 *Sistema de turnos con psiquiatra*\n\nLos turnos son los viernes por la mañana.\n\n👉 Escribí el número de la opción."
        elif msg in ["6", "seis"]:
            if not SHEETS_DISPONIBLE:
                # Fallback: usar turnos en memoria
                if state["mis_turnos"]:
                    turnos_text = "\n\n".join([
                        f"📅 {t['fecha']} {t['hora']}\n👤 {t['nombre']}\n🧠 {t['motivo']}"
                        for t in state["mis_turnos"]
                    ])
                    return f"📋 *Tus turnos:*\n\n{turnos_text}\n\n_Escribí *0* o *menú* para volver al menú principal._"
                else:
                    return f"❌ No tenés turnos registrados.\n\n_Escribí *0* o *menú* para volver al menú principal._"
            
            # Consultar turnos (Híbrido)
            turnos_usuario = get_turnos_usuario_hibrido(user_id)
            
            if turnos_usuario:
                turnos_text = ""
                for idx, turno in enumerate(turnos_usuario, 1):
                    # Convertir fecha a formato legible
                    try:
                        fecha_obj = datetime.strptime(turno['fecha'], '%Y-%m-%d')
                        fecha_legible = fecha_obj.strftime('%d/%m/%Y')
                    except:
                        fecha_legible = turno['fecha']
                    
                    turnos_text += f"{idx}. 📅 {fecha_legible} - {turno['hora']} hs\n"
                    turnos_text += f"   👤 {turno['nombre']}\n"
                    turnos_text += f"   🧠 {turno['motivo']}\n\n"
                
                return f"📋 *Tus turnos:*\n\n{turnos_text}_Escribí *0* o *menú* para volver al menú principal._"
            else:
                return f"❌ No tenés turnos registrados.\n\n_Escribí *0* o *menú* para volver al menú principal._"
        elif msg in ["7", "siete"] or is_question:
            # Inicializar RAG si no está
            if not hasattr(bot_response, 'llm'):
                bot_response.llm, bot_response.knowledge_base, _, _, _, _, _ = init_rag()
            
            if is_question and msg not in ["7", "siete"]:
                answer = rag_answer(raw, bot_response.llm, bot_response.knowledge_base)
                return f"🤖 {answer}\n\n_Escribí *0* o *menú* para volver al menú principal._"
            else:
                state["step"] = "rag"
                return "🧠 *Pregunta abierta con IA*\n\nEscribí tu pregunta sobre el Centro de Día y te responderé usando toda la información disponible.\n\n_Escribí *0* para cancelar y volver al menú._"
        else:
            return f"❌ Opción inválida. Elegí un número del 1 al 7.\n\n_Escribí *0* o *menú* para volver al menú principal._"
    
    if state["step"] == "rag":
        if not hasattr(bot_response, 'llm'):
            bot_response.llm, bot_response.knowledge_base, _, _, _, _, _ = init_rag()
        
        answer = rag_answer(raw, bot_response.llm, bot_response.knowledge_base)
        state["step"] = "menu"
        return f"🤖 {answer}\n\n_Escribí *0* o *menú* para volver al menú principal._"
    
    # SUBMENÚ DE TALLERES
    if state["step"] == "talleres_menu":
        if msg in ["0", "menu", "menú", "volver"]:
            state["step"] = "menu"
            return menu_principal()
        elif msg in ["1", "uno"]:
            state["step"] = "menu"
            return """🎨 *TransformArte*

♻️ *¿Qué es?*
Taller de reciclado creativo donde transformamos materiales descartables en obras de arte y objetos útiles. Trabajamos con cartón, plásticos, telas y otros materiales.

📅 *Horarios:*
• Lunes 18:00 a 20:00 hs
• Jueves 18:00 a 20:00 hs

👥 *¿Para quién?*
Abierto a toda la comunidad. No se requiere experiencia previa.

💚 *Beneficios:*
• Desarrollo de la creatividad
• Conciencia ambiental
• Espacio de encuentro y socialización
• Gratuito y sin inscripción

📍 Te esperamos en Trenel 53, 25 de Mayo.

_Escribí *0* o *menú* para volver._"""
        elif msg in ["2", "dos"]:
            state["step"] = "menu"
            return """🌱 *Amor de Huerta*

🥬 *¿Qué es?*
Taller de horticultura donde aprendemos a cultivar nuestros propios alimentos de forma orgánica. Armamos almácigos, cuidamos plantas y cosechamos verduras.

📅 *Horarios:*
• Martes 18:30 a 20:30 hs
• Miércoles 10:30 a 12:30 hs
• Viernes 18:30 a 20:30 hs

👥 *¿Para quién?*
Familias, adultos mayores, jóvenes. Todos pueden participar.

💚 *Beneficios:*
• Conexión con la naturaleza
• Alimentación saludable
• Trabajo en equipo
• Actividad física al aire libre
• Gratuito y sin inscripción

🥕 ¡Llevate tus propias verduras a casa!

_Escribí *0* o *menú* para volver._"""
        elif msg in ["3", "tres"]:
            state["step"] = "menu"
            return """🎭 *Teatro Leído y Escritura*

📖 *¿Qué es?*
Espacio de expresión artística donde leemos obras de teatro y creamos nuestros propios textos. Exploramos personajes, emociones y narrativas.

📅 *Horarios:*
• Viernes 18:00 a 19:00 hs

👥 *¿Para quién?*
Personas interesadas en el teatro, la lectura y la escritura creativa. No se requiere experiencia.

💚 *Beneficios:*
• Desarrollo de la expresión oral
• Estímulo de la creatividad
• Espacio de reflexión
• Trabajo colaborativo
• Gratuito y sin inscripción

🎬 ¡Animate a explorar nuevas formas de expresión!

_Escribí *0* o *menú* para volver._"""
        elif msg in ["4", "cuatro"]:
            state["step"] = "menu"
            return """💬 *Espacio Grupal*

🤝 *¿Qué es?*
Dispositivo terapéutico grupal coordinado por profesionales de salud mental. Es un espacio de escucha, contención y acompañamiento mutuo.

📅 *Horarios:*
• Miércoles 14:00 hs

👥 *¿Para quién?*
Personas que estén transitando procesos personales y busquen apoyo grupal.

💚 *Beneficios:*
• Acompañamiento profesional
• Contención emocional
• Aprendizaje compartido
• Espacio confidencial y seguro
• Gratuito

🧠 La participación es voluntaria y requiere continuidad.

_Escribí *0* o *menú* para volver._"""
        elif msg in ["5", "cinco"]:
            state["step"] = "menu"
            return """📻 *Columna Radial*

🎙️ *¿Qué es?*
Espacio de difusión en la radio municipal donde hablamos sobre salud mental, consumos problemáticos y actividades del CDC.

📡 *¿Cuándo escucharnos?*
📅 **Todos los lunes a las 11:00 hs**
📻 Radio municipal de 25 de Mayo

💚 *Temas que abordamos:*
• Salud mental
• Promoción de salud comunitaria
• Consumos problemáticos
• Actividades del CDC
• Desestigmatización

🗣️ ¡Podés participar! Acercate al CDC.

_Escribí *0* o *menú* para volver._"""
        else:
            return "❌ Opción inválida. Escribí un número del 1 al 5, o *0* para volver al menú."
    
    # Manejo de turnos
    if state["step"] == "turno":
        if not SHEETS_DISPONIBLE:
            state["step"] = "menu"
            return "⚠️ Sistema de turnos temporalmente no disponible. Llamá al 299 4152668 para agendar.\n\n_Escribí *0* o *menú* para volver._"
        
        # Mostrar próximos viernes disponibles
        viernes = get_proximos_viernes(4)
        state["step"] = "turno_fecha"
        state["data"]["viernes_disponibles"] = viernes
        
        mensaje = "📅 *Seleccioná una fecha:*\n\n"
        for idx, fecha in enumerate(viernes, 1):
            # Convertir fecha a formato legible
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
            fecha_legible = fecha_obj.strftime('%d/%m/%Y')
            mensaje += f"{idx}️⃣ {fecha_legible}\n"
        
        mensaje += "\n👉 Escribí el número de la fecha."
        return mensaje
    
    if state["step"] == "turno_fecha":
        if msg in ["1", "2", "3", "4"]:
            idx = int(msg) - 1
            fecha_elegida = state["data"]["viernes_disponibles"][idx]
            state["data"]["fecha"] = fecha_elegida
            
            # Obtener horarios disponibles
            horarios_disponibles = get_turnos_disponibles_hibrido(fecha_elegida)
            
            if not horarios_disponibles:
                state["step"] = "turno"
                return "❌ No hay horarios disponibles para esa fecha. Elegí otra fecha."
            
            state["data"]["horarios_disponibles"] = horarios_disponibles
            state["step"] = "turno_hora"
            
            # Convertir fecha a formato legible
            fecha_obj = datetime.strptime(fecha_elegida, '%Y-%m-%d')
            fecha_legible = fecha_obj.strftime('%d/%m/%Y')
            
            mensaje = f"🕒 *Horarios disponibles para {fecha_legible}:*\n\n"
            for idx, hora in enumerate(horarios_disponibles, 1):
                mensaje += f"{idx}️⃣ {hora} hs\n"
            
            mensaje += "\n👉 Escribí el número del horario."
            return mensaje
        else:
            return "❌ Opción inválida. Escribí un número del 1 al 4."
    
    if state["step"] == "turno_hora":
        if msg.isdigit() and 1 <= int(msg) <= len(state["data"]["horarios_disponibles"]):
            idx = int(msg) - 1
            hora_elegida = state["data"]["horarios_disponibles"][idx]
            state["data"]["hora"] = hora_elegida
            state["step"] = "turno_nombre"
            return "👤 *Datos personales*\n\nEscribí tu nombre completo:"
        else:
            return f"❌ Opción inválida. Escribí un número del 1 al {len(state['data']['horarios_disponibles'])}."
    
    if state["step"] == "turno_nombre":
        state["data"]["nombre"] = raw
        state["step"] = "turno_dni"
        return "🆔 Escribí tu DNI (solo números):"
    
    if state["step"] == "turno_dni":
        if not msg.isdigit() or len(msg) < 7:
            return "❌ DNI inválido. Escribí solo números (ej: 12345678):"
        
        state["data"]["dni"] = msg
        state["step"] = "turno_motivo"
        return "📋 Escribí el motivo de la consulta:"
    
    if state["step"] == "turno_motivo":
        state["data"]["motivo"] = raw
        state["step"] = "turno_primera_vez"
        return "❓ ¿Es tu primera consulta en el CDC?\n\n1️⃣ Sí\n2️⃣ No"
    
    if state["step"] == "turno_primera_vez":
        if msg in ["1", "si", "sí"]:
            primera_vez = "Si"
        elif msg in ["2", "no"]:
            primera_vez = "No"
        else:
            return "❌ Respuesta inválida. Escribí *1* para Sí o *2* para No."
        
        # Guardar turno en Sistema Híbrido (DB + Sheets)
        exito = guardar_turno_hibrido(
            telefono=user_id,
            nombre=state["data"]["nombre"],
            dni=state["data"]["dni"],
            motivo=state["data"]["motivo"],
            fecha=state["data"]["fecha"],
            hora=state["data"]["hora"],
            primera_vez=primera_vez
        )
        
        if exito:
            # Agregar a la lista de turnos del usuario
            state["mis_turnos"].append({
                "nombre": state["data"]["nombre"],
                "fecha": state["data"]["fecha"],
                "hora": state["data"]["hora"],
                "motivo": state["data"]["motivo"]
            })
            
            # Convertir fecha a formato legible
            fecha_obj = datetime.strptime(state["data"]["fecha"], '%Y-%m-%d')
            fecha_legible = fecha_obj.strftime('%d/%m/%Y')
            
            state["step"] = "menu"
            state["data"] = {}  # Limpiar datos
            
            return f"""✅ *Turno confirmado*

👤 Nombre: {state["mis_turnos"][-1]["nombre"]}
📅 Fecha: {fecha_legible}
🕒 Hora: {state["mis_turnos"][-1]["hora"]} hs
🧠 Motivo: {state["mis_turnos"][-1]["motivo"]}

📍 Dirección: {DIRECCION}
📞 Teléfono: {TELEFONO}

💡 Si necesitás cancelar, escribí *6* en el menú para ver tus turnos.

_Escribí *0* o *menú* para volver al menú principal._"""
        else:
            state["step"] = "menu"
            state["data"] = {}
            return "❌ Error al guardar el turno. Por favor, intentá nuevamente o llamá al 299 4152668.\n\n_Escribí *0* o *menú* para volver._"
    
    return f"❌ No entendí tu mensaje.\n\n_Escribí *0* o *menú* para volver al menú principal._"

# Inicializar RAG al importar
print("Inicializando sistema RAG...")
try:
    bot_response.llm, bot_response.knowledge_base, _, _, _, _, _ = init_rag()
    print("✅ Sistema RAG inicializado correctamente")
except Exception as e:
    print(f"⚠️ Error al inicializar RAG: {e}")
    bot_response.llm = None
    bot_response.knowledge_base = []

