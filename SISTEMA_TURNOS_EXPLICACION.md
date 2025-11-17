# 📅 Sistema de Turnos con Google Sheets - Explicación Completa

## 🎯 ¿Cómo Funciona?

El bot ahora tiene un **sistema completo de turnos** integrado con **Google Sheets**, que permite:

✅ **Consultar turnos disponibles en tiempo real** desde Google Sheets  
✅ **Reservar turnos** automáticamente  
✅ **Ver mis turnos** guardados  
✅ **Gestionar turnos manualmente** desde Google Sheets  
✅ **Sincronización instantánea** entre el bot y el sheet  

---

## 🔄 Flujo del Sistema

### **1. Usuario solicita turno (Opción 5 del menú)**

```
Usuario: 5
Bot: 📅 Seleccioná una fecha:
     1️⃣ 22/11/2025
     2️⃣ 29/11/2025
     3️⃣ 06/12/2025
     4️⃣ 13/12/2025
```

**¿Qué hace el bot?**
- Calcula los próximos 4 viernes
- Muestra las fechas disponibles

---

### **2. Usuario elige una fecha**

```
Usuario: 1
Bot: 🕒 Horarios disponibles para 22/11/2025:
     1️⃣ 09:00 hs
     2️⃣ 09:30 hs
     3️⃣ 10:00 hs
     ...
```

**¿Qué hace el bot?**
- **Consulta Google Sheets** para ver qué horarios ya están ocupados ese día
- Filtra y muestra **solo los horarios disponibles**
- Si no hay horarios, pide elegir otra fecha

---

### **3. Usuario elige un horario**

```
Usuario: 1
Bot: 👤 Datos personales
     Escribí tu nombre completo:
```

---

### **4. Bot solicita datos**

```
Bot: Escribí tu nombre completo:
Usuario: Juan Pérez

Bot: 🆔 Escribí tu DNI:
Usuario: 12345678

Bot: 📋 Escribí el motivo de la consulta:
Usuario: Primera consulta

Bot: ❓ ¿Es tu primera consulta en el CDC?
     1️⃣ Sí
     2️⃣ No
Usuario: 1
```

---

### **5. Bot guarda el turno en Google Sheets**

```
Bot: ✅ Turno confirmado

👤 Nombre: Juan Pérez
📅 Fecha: 22/11/2025
🕒 Hora: 09:00 hs
🧠 Motivo: Primera consulta

📍 Dirección: Trenel 53, Colonia 25 de Mayo, La Pampa
📞 Teléfono: 299 4152668
```

**¿Qué hace el bot?**
- **Guarda una nueva fila en Google Sheets** con todos los datos:
  - telefono
  - nombre
  - dni
  - motivo
  - fecha
  - hora
  - primera_vez
  - timestamp (fecha/hora de reserva)

---

### **6. Usuario consulta sus turnos (Opción 6 del menú)**

```
Usuario: 6
Bot: 📋 Tus turnos:

1. 📅 22/11/2025 - 09:00 hs
   👤 Juan Pérez
   🧠 Primera consulta

2. 📅 29/11/2025 - 10:30 hs
   👤 Juan Pérez
   🧠 Seguimiento
```

**¿Qué hace el bot?**
- **Consulta Google Sheets** filtrando por número de teléfono
- Muestra todos los turnos del usuario

---

## 📊 Estructura del Google Sheet

### **Columnas:**

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| **telefono** | **nombre** | **dni** | **motivo** | **fecha** | **hora** | **primera_vez** | **timestamp** |

### **Ejemplo de datos:**

| telefono | nombre | dni | motivo | fecha | hora | primera_vez | timestamp |
|----------|--------|-----|--------|-------|------|-------------|-----------|
| 2994152668 | Juan Pérez | 12345678 | Primera consulta | 2025-11-22 | 09:00 | Si | 2025-11-17 10:30:00 |
| 2995551234 | María García | 23456789 | Seguimiento | 2025-11-22 | 09:30 | No | 2025-11-17 11:00:00 |
| 2994152668 | Juan Pérez | 12345678 | Seguimiento | 2025-11-29 | 10:30 | No | 2025-11-18 14:20:00 |

---

## 🔧 Archivos del Sistema

### **1. `sheets_manager.py`** (Nuevo)
Gestor de conexión y operaciones con Google Sheets.

**Funciones principales:**
- `get_turnos_disponibles(fecha)` - Obtiene horarios disponibles
- `get_turnos_usuario(telefono)` - Obtiene turnos de un usuario
- `get_proximos_viernes(cantidad)` - Calcula próximos viernes
- `guardar_turno(...)` - Guarda nuevo turno
- `cancelar_turno(...)` - Elimina un turno

### **2. `bot_logic.py`** (Modificado)
Lógica del bot con integración de turnos.

**Cambios:**
- Importa funciones de `sheets_manager`
- Flujo completo de reserva de turnos (pasos 1-5)
- Consulta de turnos desde Google Sheets

### **3. `GUIA_GOOGLE_SHEETS_SETUP.md`** (Nuevo)
Guía paso a paso para configurar Google Sheets API.

**Incluye:**
- Crear Google Sheet
- Configurar Google Cloud Console
- Crear cuenta de servicio
- Obtener credenciales JSON
- Configurar variables de entorno

---

## ⚙️ Configuración Necesaria

### **Variables de entorno requeridas:**

#### **Railway (WhatsApp Bot):**
```
GOOGLE_SHEET_ID = "id_de_tu_sheet_aqui"
GOOGLE_SHEETS_CREDENTIALS = {"type":"service_account",...}
```

#### **Streamlit Cloud (Web Bot):**
```toml
[google_sheets]
sheet_id = "id_de_tu_sheet_aqui"
credentials = '''
{
  "type": "service_account",
  ...
}
'''
```

---

## 📋 Horarios Disponibles

**Turnos con psiquiatra:**
- 📅 **Día:** Viernes
- ⏰ **Horarios:**
  - 09:00
  - 09:30
  - 10:00
  - 10:30
  - 11:00
  - 11:30
  - 12:00

**Total:** 7 turnos por viernes

---

## 💡 Ventajas del Sistema

### **1. Gestión desde Google Sheets**
✅ Podés ver todos los turnos en una sola vista  
✅ Filtrar por fecha, nombre, teléfono  
✅ Exportar a Excel para reportes  
✅ Compartir con otros profesionales del CDC  

### **2. Actualización en Tiempo Real**
✅ Cuando alguien reserva, se actualiza instantáneamente  
✅ El bot siempre muestra horarios actualizados  
✅ No hay riesgo de sobreturnar  

### **3. Sincronización Automática**
✅ No necesitás hacer nada manualmente  
✅ El bot se encarga de todo  
✅ Si editás el sheet, el bot lo refleja inmediatamente  

### **4. Respaldo y Seguridad**
✅ Todos los datos están en la nube (Google Drive)  
✅ Historial completo de turnos  
✅ Recuperación ante errores  

---

## 🆘 Troubleshooting

### **Problema: "Sistema de turnos temporalmente no disponible"**

**Causas posibles:**
1. Variables de entorno no configuradas
2. Credenciales incorrectas
3. Sheet no compartido con la cuenta de servicio

**Solución:**
- Verificar que `GOOGLE_SHEET_ID` esté configurado
- Verificar que `GOOGLE_SHEETS_CREDENTIALS` esté correcto
- Verificar que el sheet esté compartido con el email de la cuenta de servicio

---

### **Problema: "No hay horarios disponibles"**

**Causas posibles:**
1. Todos los horarios de ese viernes están ocupados
2. Error al leer el sheet

**Solución:**
- Revisar Google Sheets manualmente
- Eliminar turnos viejos o cancelados
- Elegir otra fecha

---

### **Problema: "Error al guardar el turno"**

**Causas posibles:**
1. Permisos insuficientes en el sheet
2. Sheet eliminado o renombrado

**Solución:**
- Verificar que el sheet existe
- Verificar que la cuenta de servicio tiene permisos de "Editor"

---

## 📊 Reportes y Estadísticas

### **Desde Google Sheets podés:**

**1. Ver cantidad de turnos por día:**
```
=COUNTIF(E:E, "2025-11-22")
```

**2. Ver usuarios únicos:**
```
=UNIQUE(B:B)
```

**3. Ver motivos más frecuentes:**
```
=COUNTIF(D:D, "Primera consulta")
```

**4. Exportar a Excel** para análisis más complejos

---

## 🔐 Seguridad y Privacidad

### **Datos protegidos:**
✅ Credenciales guardadas como variables de entorno (no en código)  
✅ Sheet solo accesible con cuenta de servicio  
✅ No se expone información sensible en logs  

### **Recomendaciones:**
⚠️ **NO compartir** el archivo JSON de credenciales  
⚠️ **NO subir** credenciales a GitHub  
⚠️ **Limitar acceso** al Google Sheet solo a personal autorizado  

---

## 🚀 Próximas Mejoras Posibles

### **Funcionalidades adicionales:**
- [ ] Cancelar turnos desde el bot
- [ ] Recordatorios automáticos por WhatsApp (24 hs antes)
- [ ] Reprogramar turnos
- [ ] Ver historial de turnos pasados
- [ ] Estadísticas en tiempo real

---

## 📞 Soporte

Si tenés problemas con el sistema de turnos:
1. Revisar logs en Railway
2. Verificar configuración en Google Cloud Console
3. Revisar permisos del Google Sheet
4. Contactar para asistencia

---

**Fecha:** 17 de noviembre de 2025  
**Versión:** 1.0  
**Commit:** `24f62ba` - "Agregar integración con Google Sheets para sistema de turnos completo"

