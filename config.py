"""
Configuración centralizada para el Bot del CDC
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Credenciales y Claves
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# Información Institucional
INFO_CENTRO = """El Centro de Día Comunitario – 25 de Mayo es un dispositivo territorial comunitario 
que brinda atención en salud mental y adicciones. Depende de la Subsecretaría de Salud Mental y 
Adicciones del Gobierno de La Pampa, la Municipalidad de 25 de Mayo y SEDRONAR.

¿Quiénes pueden asistir?
Personas mayores de 13 años que necesiten acompañamiento, contención y espacios terapéuticos."""

HORARIOS = """HORARIOS DE VERANO:
• Lunes a viernes (mañana): 9:00 a 12:00 hs
• Lunes, miércoles y jueves (tarde): 16:00 a 19:00 hs
• Martes y viernes (tarde): 17:00 a 20:00 hs"""

DIRECCION = "Trenel 53, Colonia 25 de Mayo, La Pampa"
TELEFONO = "299 4152668"
EMAIL = "cdc.25demayolp.coordinacion@gmail.com"

# Textos para RAG
DOC_TEXTS = [
    # Información institucional
    {"title": "Centro de Día Comunitario", "content": INFO_CENTRO},
    {"title": "Horarios", "content": HORARIOS},
    {"title": "Contacto", "content": f"Dirección: {DIRECCION}\nTeléfono: {TELEFONO}\nEmail: {EMAIL}"},
    
    # Historia del CDC
    {"title": "Fundación", "content": """El Centro de Día Comunitario se puso en funcionamiento el 5 de octubre de 2021 
    como parte del trabajo conjunto entre la municipalidad, provincia y nación para dar respuesta específica en materia 
    de consumos problemáticos y salud mental en 25 de Mayo."""},
    
    # Ingreso
    {"title": "Ingreso al Centro de Día", "content": """Para participar de las actividades se realiza una primera escucha con el equipo profesional.
    Luego de esta entrevista inicial se asignan turnos según disponibilidad para:
    - Psicoterapia individual
    - Talleres terapéuticos
    - Dispositivos grupales
    - Acompañamiento en salud mental comunitaria"""},
    
    # Dispositivos
    {"title": "Dispositivos disponibles", "content": """Dispositivos del CDC:
    - Acompañamiento para personas en situación de consumos problemáticos
    - Dispositivo grupal quincenal para familiares de personas con consumos
    - Talleres con modalidad terapéutica
    - Espacios grupales de salud mental
    - Psicoterapia individual según evaluación y disponibilidad"""},
    
    # Acompañamiento psiquiátrico
    {"title": "Psiquiatría", "content": """El psiquiatra del Centro de Día realiza el seguimiento y acompañamiento farmacológico de quienes lo necesitan.
    La interconsulta psiquiátrica es solicitada por el psicólogo/a del Centro, para trabajar de manera articulada en espacios individuales, grupales o talleres.
    Atención: Viernes por la mañana (requiere turno previo)"""},
    
    # Talleres
    {"title": "Talleres", "content": """Talleres disponibles en el CDC:
    1. TransformArte (reciclado creativo): Lunes y jueves 18:00 a 20:00 hs
    2. Amor de Huerta (horticultura): Martes y viernes 18:30 a 20:30 hs, Miércoles 10:30 a 12:30 hs
       El taller es gratuito. Como parte del circuito productivo, el grupo vende lo que produce (plantas y aromáticas) con fines formativos e integradores.
    3. Teatro Leído y Escritura: Viernes 18:00 a 19:00 hs
    4. Espacio Grupal (terapia grupal): Miércoles 14:00 hs
    5. Columna Radial: Todos los lunes a las 11:00 hs en la radio municipal. Se abordan temas de salud mental, promoción de salud comunitaria y consumos problemáticos."""},
    
    # Preguntas frecuentes
    {"title": "Preguntas frecuentes", "content": """
    ¿Puedo asistir con compañía o con mi hijo si no tengo con quién dejarlo?
    Sí. Podés asistir acompañado/a. Entendemos las situaciones familiares y buscamos facilitar el acceso.
    
    ¿Las actividades tienen costo?
    No. Todas las actividades del Centro de Día son gratuitas."""},
]
