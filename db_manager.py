"""
Gestor de Base de Datos (Supabase)
"""
import os
from datetime import datetime
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

# Variable global para el cliente
supabase: Client = None

def init_supabase():
    """Inicializa el cliente de Supabase"""
    global supabase
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("⚠️ Faltan credenciales de Supabase (SUPABASE_URL o SUPABASE_KEY)")
        return None
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Cliente Supabase inicializado")
        return supabase
    except Exception as e:
        print(f"❌ Error al inicializar Supabase: {e}")
        return None

def get_supabase():
    """Obtiene la instancia del cliente, inicializando si es necesario"""
    global supabase
    if supabase is None:
        init_supabase()
    return supabase

def guardar_turno_db(telefono, nombre, dni, motivo, fecha, hora, primera_vez):
    """
    Guarda un turno en la base de datos Supabase
    """
    client = get_supabase()
    if not client:
        return False
    
    try:
        data = {
            "telefono": telefono,
            "nombre": nombre,
            "dni": dni,
            "motivo": motivo,
            "fecha": fecha,
            "hora": hora,
            "primera_vez": primera_vez,
            "created_at": datetime.now().isoformat()
        }
        
        response = client.table("turnos").insert(data).execute()
        
        # Verificar respuesta (Supabase devuelve data en response.data)
        if response.data:
            print(f"✅ Turno guardado en DB: {nombre} - {fecha} {hora}")
            return True
        else:
            print("⚠️ No se recibieron datos de confirmación de Supabase")
            return False
            
    except Exception as e:
        print(f"❌ Error al guardar en DB: {e}")
        return False

def get_turnos_usuario_db(telefono):
    """
    Obtiene los turnos de un usuario desde Supabase
    """
    client = get_supabase()
    if not client:
        return []
    
    try:
        response = client.table("turnos").select("*").eq("telefono", telefono).order("fecha", desc=True).execute()
        return response.data
    except Exception as e:
        print(f"❌ Error al leer turnos de DB: {e}")
        return []

def get_turnos_ocupados_db(fecha):
    """
    Obtiene los horarios ocupados para una fecha
    """
    client = get_supabase()
    if not client:
        return []
    
    try:
        response = client.table("turnos").select("hora").eq("fecha", fecha).execute()
        return [row['hora'] for row in response.data]
    except Exception as e:
        print(f"❌ Error al leer ocupados de DB: {e}")
        return []
