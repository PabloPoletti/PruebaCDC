# 📝 Actualización de Información del CDC

## 🎯 Resumen de Cambios

Se actualizó toda la información del bot (Streamlit y WhatsApp) con los datos oficiales más recientes del Centro de Día Comunitario – 25 de Mayo.

---

## 📋 Cambios Implementados

### 1️⃣ **Nombre Oficial del Centro**

**Antes:**
- Centro de Día Comunitario de 25 de Mayo

**Ahora:**
- **Centro de Día Comunitario – 25 de Mayo** (con guion)

---

### 2️⃣ **Horarios Actualizados (VERANO)**

**Antes:**
```
Lunes a Viernes:
• Mañana: 9:00 a 13:00 hs
• Tarde: 15:00 a 18:30 hs
```

**Ahora:**
```
HORARIOS DE VERANO:
• Lunes a viernes (mañana): 9:00 a 12:00 hs
• Lunes, miércoles y jueves (tarde): 16:00 a 19:00 hs
• Martes y viernes (tarde): 17:00 a 20:00 hs
```

**📌 Nota:** Los horarios ahora son diferenciados por día y muestran explícitamente que son horarios de verano.

---

### 3️⃣ **Edad Mínima para Atención**

**Agregado:**
```
¿Quiénes pueden asistir?
Personas mayores de 13 años que necesiten acompañamiento, 
contención y espacios terapéuticos.
```

---

### 4️⃣ **Ingreso al Centro de Día**

**Agregado:**
```
Para participar de las actividades se realiza una PRIMERA ESCUCHA 
con el equipo profesional.

Luego de esta entrevista inicial se asignan turnos según disponibilidad para:
- Psicoterapia individual
- Talleres terapéuticos
- Dispositivos grupales
- Acompañamiento en salud mental comunitaria
```

---

### 5️⃣ **Dispositivos Disponibles (NUEVO)**

**Agregado:**
```
- Acompañamiento para personas en situación de consumos problemáticos
- Dispositivo grupal quincenal para familiares de personas con consumos
- Talleres con modalidad terapéutica
- Espacios grupales de salud mental
- Psicoterapia individual según evaluación y disponibilidad
```

---

### 6️⃣ **Acompañamiento Psiquiátrico (DETALLADO)**

**Agregado:**
```
El psiquiatra del Centro de Día realiza el seguimiento y acompañamiento 
farmacológico de quienes lo necesitan.

La interconsulta psiquiátrica es solicitada por el psicólogo/a del Centro, 
para trabajar de manera articulada en espacios individuales, grupales o talleres.

Atención: Viernes por la mañana (requiere turno previo)
```

---

### 7️⃣ **Columna Radial (HORARIO ESPECÍFICO)**

**Antes:**
```
Columna Radial: Difusión en salud mental
```

**Ahora:**
```
Columna Radial:
📅 Todos los lunes a las 11:00 hs
📻 Radio municipal de 25 de Mayo

Temas:
• Salud mental
• Promoción de salud comunitaria
• Consumos problemáticos
• Actividades del CDC
```

---

### 8️⃣ **Taller de Huerta (DETALLES ADICIONALES)**

**Agregado:**
```
El taller es gratuito. Como parte del circuito productivo, 
el grupo vende lo que produce (plantas y aromáticas) con fines 
formativos e integradores.
```

---

### 9️⃣ **Preguntas Frecuentes Nuevas**

#### **¿Puedo asistir con compañía o con mi hijo si no tengo con quién dejarlo?**
```
👉 Sí. Podés asistir acompañado/a. Entendemos las situaciones 
familiares y buscamos facilitar el acceso.
```

#### **¿Las actividades tienen costo?**
```
👉 No. Todas las actividades del Centro de Día son gratuitas.
```

---

## 📂 Archivos Modificados

### 1. **`data/info_cdc.txt`**
- ✅ Nombre oficial del centro
- ✅ Horarios de verano
- ✅ Edad mínima (13 años)
- ✅ Ingreso al centro (primera escucha)
- ✅ Dispositivos disponibles
- ✅ Acompañamiento psiquiátrico detallado
- ✅ Columna radial con horario

### 2. **`data/preguntas_frecuentes.txt`**
- ✅ Horarios de verano
- ✅ Edad mínima
- ✅ Pregunta sobre asistir acompañado
- ✅ Detalles del taller de huerta
- ✅ Pregunta sobre columna radial

### 3. **`bot_logic.py`** (Bot WhatsApp)
- ✅ Constantes `INFO_CENTRO` y `HORARIOS` actualizadas
- ✅ `DOC_TEXTS` con nueva información
- ✅ Respuesta del menú opción 3 (Servicios) actualizada
- ✅ Información detallada de talleres
- ✅ Columna Radial con horario específico

### 4. **`app.py`** (Bot Streamlit)
- ✅ `HORARIOS` actualizado con horarios de verano

---

## 🔍 Cómo Verificar los Cambios

### **En Streamlit (Web):**
1. Ir a: https://pruebacdc.streamlit.app/
2. Escribir `2` → Ver horarios de verano actualizados
3. Escribir `3` → Ver dispositivos disponibles
4. Escribir `4` → Ver talleres con información detallada

### **En WhatsApp (Bot):**
1. Enviar mensaje al bot de Twilio
2. Escribir `2` → Ver horarios de verano
3. Escribir `3` → Ver servicios y dispositivos actualizados
4. Escribir `4` luego `5` → Ver Columna Radial con horario
5. Escribir `7` y preguntar: "¿Desde qué edad puedo asistir?" → Debería responder "mayores de 13 años"

---

## 📊 Impacto de los Cambios

### **Información Más Precisa:**
- ✅ Horarios diferenciados por día
- ✅ Edad mínima claramente especificada
- ✅ Proceso de ingreso explicado

### **Servicios Mejor Descritos:**
- ✅ Dispositivos disponibles listados
- ✅ Acompañamiento psiquiátrico detallado
- ✅ Columna radial con horario exacto

### **Preguntas Frecuentes Ampliadas:**
- ✅ Más información sobre flexibilidad (asistir acompañado)
- ✅ Detalles sobre el taller de huerta
- ✅ Información de la columna de radio

---

## 🚀 Próximos Pasos Recomendados

### **1. Validación con el CDC**
- [ ] Verificar que los horarios de verano sean correctos
- [ ] Confirmar que la edad mínima es 13 años
- [ ] Validar información de dispositivos

### **2. Actualizaciones Futuras**
- [ ] Agregar horarios de invierno cuando corresponda
- [ ] Actualizar información de talleres si cambian
- [ ] Agregar más preguntas frecuentes según consultas reales

### **3. Monitoreo**
- [ ] Revisar logs de consultas del bot
- [ ] Identificar preguntas no respondidas correctamente
- [ ] Ajustar RAG según feedback de usuarios

---

## 📞 Contacto

Si necesitás actualizar más información o tenés dudas sobre los cambios, contactame.

---

**Fecha de actualización:** 17 de noviembre de 2025  
**Versión:** 2.0  
**Commit:** `d5528f6` - "Actualizar información del CDC: horarios de verano, dispositivos, edad mínima y detalles de servicios"

