"""
Gestor de Google Sheets para sistema de turnos del CDC
Maneja lectura y escritura de turnos en Google Sheets
"""

import os
import json
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials

# =====================================================
# CONFIGURACIÓN
# =====================================================

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Horarios disponibles para turnos con psiquiatra (viernes por la mañana)
TURNOS_DISPONIBLES = [
    "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00"
]

# =====================================================
# FUNCIONES DE CONEXIÓN
# =====================================================

def get_google_sheets_client():
    """
    Conecta con Google Sheets usando credenciales de cuenta de servicio
    
    Returns:
        gspread.Client: Cliente autenticado de Google Sheets
    """
    try:
        # Intentar cargar credenciales desde variable de entorno
        creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
        
        if not creds_json:
            print("⚠️ Variable GOOGLE_SHEETS_CREDENTIALS no encontrada")
            return None
        
        # Parsear JSON
        creds_dict = json.loads(creds_json)
        
        # Crear credenciales
        credentials = Credentials.from_service_account_info(
            creds_dict,
            scopes=SCOPES
        )
        
        # Crear cliente
        client = gspread.authorize(credentials)
        
        print("✅ Conectado exitosamente a Google Sheets")
        return client
        
    except Exception as e:
        print(f"❌ Error al conectar con Google Sheets: {e}")
        return None

def get_turnos_sheet():
    """
    Obtiene la hoja de cálculo de turnos
    
    Returns:
        gspread.Worksheet: Worksheet de turnos o None si hay error
    """
    try:
        client = get_google_sheets_client()
        if not client:
            return None
        
        # Obtener ID del sheet desde variable de entorno
        sheet_id = os.getenv('GOOGLE_SHEET_ID')
        if not sheet_id:
            print("⚠️ Variable GOOGLE_SHEET_ID no encontrada")
            return None
        
        # Abrir el spreadsheet
        spreadsheet = client.open_by_key(sheet_id)
        
        # Obtener la worksheet "Turnos"
        worksheet = spreadsheet.worksheet("Turnos")
        
        print("✅ Worksheet 'Turnos' cargada correctamente")
        return worksheet
        
    except gspread.exceptions.WorksheetNotFound:
        print("❌ No se encontró la solapa 'Turnos' en el Google Sheet")
        return None
    except Exception as e:
        print(f"❌ Error al abrir el sheet: {e}")
        return None

# =====================================================
# FUNCIONES DE LECTURA
# =====================================================

def get_turnos_ocupados(fecha):
    """
    Obtiene los turnos ocupados para una fecha específica
    
    Args:
        fecha (str): Fecha en formato 'YYYY-MM-DD'
    
    Returns:
        list: Lista de horarios ocupados (ej: ['09:00', '10:30'])
    """
    try:
        worksheet = get_turnos_sheet()
        if not worksheet:
            return []
        
        # Obtener todos los registros
        registros = worksheet.get_all_records()
        
        # Filtrar por fecha y obtener horarios
        turnos_ocupados = [
            registro['hora'] 
            for registro in registros 
            if registro.get('fecha') == fecha
        ]
        
        print(f"📅 Turnos ocupados para {fecha}: {turnos_ocupados}")
        return turnos_ocupados
        
    except Exception as e:
        print(f"❌ Error al leer turnos ocupados: {e}")
        return []

def get_turnos_disponibles(fecha):
    """
    Obtiene los turnos disponibles para una fecha específica
    
    Args:
        fecha (str): Fecha en formato 'YYYY-MM-DD'
    
    Returns:
        list: Lista de horarios disponibles
    """
    ocupados = get_turnos_ocupados(fecha)
    disponibles = [h for h in TURNOS_DISPONIBLES if h not in ocupados]
    
    print(f"✅ Turnos disponibles para {fecha}: {disponibles}")
    return disponibles

def get_turnos_usuario(telefono):
    """
    Obtiene todos los turnos de un usuario específico
    
    Args:
        telefono (str): Número de teléfono del usuario
    
    Returns:
        list: Lista de diccionarios con los turnos del usuario
    """
    try:
        worksheet = get_turnos_sheet()
        if not worksheet:
            return []
        
        # Obtener todos los registros
        registros = worksheet.get_all_records()
        
        # Filtrar por teléfono
        turnos_usuario = [
            registro 
            for registro in registros 
            if registro.get('telefono') == telefono
        ]
        
        print(f"👤 Turnos encontrados para {telefono}: {len(turnos_usuario)}")
        return turnos_usuario
        
    except Exception as e:
        print(f"❌ Error al leer turnos del usuario: {e}")
        return []

def get_proximos_viernes(cantidad=4):
    """
    Obtiene las fechas de los próximos viernes
    
    Args:
        cantidad (int): Cantidad de viernes a obtener
    
    Returns:
        list: Lista de fechas en formato 'YYYY-MM-DD'
    """
    fechas = []
    hoy = datetime.now().date()
    
    # Encontrar el próximo viernes
    dias_hasta_viernes = (4 - hoy.weekday()) % 7
    if dias_hasta_viernes == 0:
        dias_hasta_viernes = 7  # Si hoy es viernes, el próximo es en 7 días
    
    proximo_viernes = hoy + timedelta(days=dias_hasta_viernes)
    
    # Agregar los próximos viernes
    for i in range(cantidad):
        fecha = proximo_viernes + timedelta(weeks=i)
        fechas.append(fecha.strftime('%Y-%m-%d'))
    
    return fechas

# =====================================================
# FUNCIONES DE ESCRITURA
# =====================================================

def guardar_turno(telefono, nombre, dni, motivo, fecha, hora, primera_vez):
    """
    Guarda un nuevo turno en Google Sheets
    
    Args:
        telefono (str): Número de teléfono
        nombre (str): Nombre completo
        dni (str): DNI
        motivo (str): Motivo de la consulta
        fecha (str): Fecha en formato 'YYYY-MM-DD'
        hora (str): Hora en formato 'HH:MM'
        primera_vez (str): 'Si' o 'No'
    
    Returns:
        bool: True si se guardó correctamente, False si hubo error
    """
    try:
        worksheet = get_turnos_sheet()
        if not worksheet:
            return False
        
        # Crear timestamp actual
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Crear fila nueva
        nueva_fila = [
            telefono,
            nombre,
            dni,
            motivo,
            fecha,
            hora,
            primera_vez,
            timestamp
        ]
        
        # Agregar fila al final
        worksheet.append_row(nueva_fila)
        
        print(f"✅ Turno guardado: {nombre} - {fecha} {hora}")
        return True
        
    except Exception as e:
        print(f"❌ Error al guardar turno: {e}")
        return False

def cancelar_turno(telefono, fecha, hora):
    """
    Cancela un turno eliminándolo del sheet
    
    Args:
        telefono (str): Número de teléfono
        fecha (str): Fecha del turno
        hora (str): Hora del turno
    
    Returns:
        bool: True si se canceló correctamente, False si hubo error
    """
    try:
        worksheet = get_turnos_sheet()
        if not worksheet:
            return False
        
        # Obtener todos los registros con números de fila
        registros = worksheet.get_all_records()
        
        # Buscar el turno (la fila en el sheet empieza en 2, no en 1)
        for idx, registro in enumerate(registros, start=2):
            if (registro.get('telefono') == telefono and 
                registro.get('fecha') == fecha and 
                registro.get('hora') == hora):
                
                # Eliminar la fila
                worksheet.delete_rows(idx)
                print(f"✅ Turno cancelado: {fecha} {hora}")
                return True
        
        print(f"⚠️ No se encontró el turno para cancelar")
        return False
        
    except Exception as e:
        print(f"❌ Error al cancelar turno: {e}")
        return False

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def verificar_conexion():
    """
    Verifica que la conexión con Google Sheets funcione
    
    Returns:
        bool: True si la conexión funciona, False si no
    """
    try:
        worksheet = get_turnos_sheet()
        if worksheet:
            # Intentar leer la primera celda
            worksheet.acell('A1').value
            print("✅ Verificación de conexión exitosa")
            return True
        return False
    except Exception as e:
        print(f"❌ Error en verificación de conexión: {e}")
        return False

def inicializar_sheet_si_vacio():
    """
    Inicializa el sheet con encabezados si está vacío
    
    Returns:
        bool: True si se inicializó o ya existía, False si hubo error
    """
    try:
        worksheet = get_turnos_sheet()
        if not worksheet:
            return False
        
        # Verificar si hay encabezados
        primera_fila = worksheet.row_values(1)
        
        if not primera_fila or primera_fila[0] == '':
            # Sheet vacío, agregar encabezados
            encabezados = [
                'telefono', 'nombre', 'dni', 'motivo', 
                'fecha', 'hora', 'primera_vez', 'timestamp'
            ]
            worksheet.insert_row(encabezados, 1)
            print("✅ Encabezados agregados al sheet")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al inicializar sheet: {e}")
        return False

# =====================================================
# INICIALIZACIÓN
# =====================================================

if __name__ == "__main__":
    # Test de conexión
    print("🧪 Probando conexión con Google Sheets...")
    if verificar_conexion():
        print("✅ Conexión exitosa!")
        inicializar_sheet_si_vacio()
    else:
        print("❌ Error de conexión")

