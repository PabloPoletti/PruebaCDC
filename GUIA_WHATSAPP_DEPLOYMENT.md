# 📱 Guía para Conectar el Bot a WhatsApp

## 🎯 Objetivo
Conectar el bot del CDC a WhatsApp para atender 500-1000 consultas diarias de forma gratuita o económica.

---

## 📊 Análisis de Volumen

**Tu caso:**
- 500-1000 consultas/día
- ~15,000-30,000 consultas/mes
- Organización sin fines de lucro (CDC - Salud Mental)

---

## 🆓 OPCIÓN 1: WhatsApp Business API (GRATIS) - **RECOMENDADA**

### ✅ **Meta for Developers + WhatsApp Business Platform**

**Costo:** 
- ✅ **GRATIS** las primeras 1,000 conversaciones/mes
- ✅ Después: ~$0.05-0.10 USD por conversación
- ✅ Para tu volumen (1000 consultas/día): ~$1,500-3,000 USD/mes SI superas el límite gratuito

**¿Cómo funciona el límite gratuito?**
- Meta cuenta "conversaciones de servicio" de 24 horas
- Si un usuario te escribe y respondes en 24hs, cuenta como 1 conversación
- Si el mismo usuario vuelve a escribir después de 24hs, es otra conversación
- Las 1,000 primeras conversaciones/mes son GRATIS

**Requisitos:**
1. ✅ Número de teléfono dedicado (puede ser prepago o postpago)
2. ✅ Cuenta de Facebook Business
3. ✅ Verificación de la organización
4. ✅ Hosting para tu bot (Streamlit Cloud es GRATIS pero tiene limitaciones)

**Ventajas:**
- ✅ API oficial de Meta
- ✅ 1,000 conversaciones gratis/mes
- ✅ Sin límite de mensajes por conversación
- ✅ Marca verificada (check verde)
- ✅ Escalable
- ✅ Soporte oficial

**Desventajas:**
- ❌ Requiere servidor activo 24/7
- ❌ Proceso de aprobación puede tardar
- ❌ Si superas 1,000 conversaciones/mes, se vuelve costoso

**Para tu caso:**
Si tienes ~500 consultas/día y cada usuario consulta 1 vez por semana:
- ~2,000 conversaciones únicas/mes
- Costo: (2,000 - 1,000) × $0.08 = **$80 USD/mes**

---

## 🌟 OPCIÓN 2: Twilio + WhatsApp Business API - **MÁS FLEXIBLE**

### ✅ **Twilio WhatsApp Business API**

**Costo:**
- ✅ Cuenta gratuita de prueba con crédito inicial
- ✅ Después: ~$0.005 USD por mensaje enviado
- ✅ Para tu volumen: ~$75-150 USD/mes

**Cálculo para tu caso:**
- 1,000 consultas/día × 30 días = 30,000 mensajes/mes
- Asumiendo 2 mensajes por conversación (1 del usuario, 1 del bot):
- 30,000 × 2 × $0.005 = **$300 USD/mes**

**Ventajas:**
- ✅ Más control y flexibilidad
- ✅ Documentación excelente
- ✅ API muy completa
- ✅ Crédito de prueba inicial
- ✅ Pago por uso (más predecible)

**Desventajas:**
- ❌ No es tan barato como la API directa de Meta
- ❌ Requiere número verificado
- ❌ Capa intermedia (Twilio)

---

## 💚 OPCIÓN 3: Soluciones Gratuitas/Económicas para ONGs

### ✅ **Meta for Good + WhatsApp Business API**

**¿Qué es?**
Meta ofrece servicios gratuitos o con descuento para organizaciones sin fines de lucro.

**Costo:**
- ✅ Potencialmente **GRATIS** o con descuento del 50-80%
- ✅ Requiere ser ONG registrada

**Requisitos:**
1. ✅ ONG registrada (el CDC califica como salud mental/adicciones)
2. ✅ Aplicar al programa Meta for Good
3. ✅ Documentación de la organización

**Cómo aplicar:**
1. Ir a: https://www.facebook.com/business/nonprofits
2. Crear cuenta de Facebook Business
3. Aplicar al programa de ONGs
4. Esperar aprobación (2-4 semanas)

**Ventajas:**
- ✅ **GRATIS o muy económico**
- ✅ Soporte prioritario
- ✅ Créditos de publicidad en Facebook/Instagram
- ✅ Herramientas adicionales

**Desventajas:**
- ❌ Proceso de aprobación más largo
- ❌ Requiere documentación formal

---

## 🚀 OPCIÓN 4: WhatsApp Business App (Limitada) - **NO RECOMENDADA**

### ❌ **WhatsApp Business App (Gratis pero limitada)**

**Costo:**
- ✅ **GRATIS**

**Desventajas CRÍTICAS:**
- ❌ Solo 1 dispositivo conectado
- ❌ Sin API (no puedes conectar tu bot)
- ❌ Respuestas automáticas muy básicas
- ❌ No escalable
- ❌ No sirve para 500-1000 consultas/día

**Conclusión:** No sirve para tu caso.

---

## 🏆 MI RECOMENDACIÓN: Plan en 3 Fases

### 📅 **FASE 1: Prueba Gratis (1-3 meses)**

**Usar:** WhatsApp Business API + Meta for Developers

**Pasos:**
1. ✅ Obtener número prepago (movistar/claro/personal)
2. ✅ Crear cuenta Facebook Business
3. ✅ Aplicar a WhatsApp Business API
4. ✅ Hosting del bot en Railway/Render (gratis)
5. ✅ Probar con las 1,000 conversaciones gratis/mes

**Costo Fase 1:** 
- Número prepago: $500-1,000 ARS inicial + $500-1,000 ARS/mes
- Hosting: GRATIS (Railway/Render tier gratuito)
- API: GRATIS (primeras 1,000 conversaciones)
- **TOTAL: ~$1,500-2,000 ARS/mes**

---

### 📅 **FASE 2: Aplicar a Meta for Good (mes 2-4)**

**Mientras pruebas, aplicar a Meta for Good:**

**Pasos:**
1. ✅ Preparar documentación del CDC
2. ✅ Aplicar al programa de ONGs
3. ✅ Esperar aprobación (2-4 semanas)
4. ✅ Si aprueban: API GRATIS o con descuento 80%

**Documentación necesaria:**
- Estatuto del CDC
- Personería jurídica (si tiene)
- Carta de la municipalidad
- Documentación de SEDRONAR
- Prueba de trabajo en salud mental

---

### 📅 **FASE 3: Producción Escalada (mes 4+)**

**Si Meta for Good aprueba:**
- ✅ API GRATIS o muy económica
- ✅ Escalar sin problemas

**Si NO aprueba:**
- Plan A: Quedarse con 1,000 conversaciones gratis/mes y optimizar
- Plan B: Buscar sponsor/donante para cubrir costos
- Plan C: Migrar a modelo híbrido (web + WhatsApp limitado)

---

## 📱 Número de Teléfono: ¿Prepago o Postpago?

### ✅ **RECOMENDACIÓN: POSTPAGO (Plan Básico)**

**¿Por qué?**
- ✅ No se queda sin saldo
- ✅ Más estable
- ✅ Mejor para servicios críticos (salud mental)
- ✅ Factura mensual predecible

**Costo en Argentina (2025):**
- Plan básico: $3,000-5,000 ARS/mes
- Incluye: datos, minutos, SMS
- No necesitas mucho, solo que esté activo

**Operadores recomendados:**
1. **Personal**: Mejor cobertura en zonas rurales
2. **Movistar**: Buenos planes para empresas/ONGs
3. **Claro**: Económico

### ⚠️ **Si usas PREPAGO:**

**Ventajas:**
- ✅ Más económico inicialmente
- ✅ Control total del gasto

**Desventajas:**
- ❌ Tienes que cargar todos los meses
- ❌ Si se queda sin saldo, el servicio cae
- ❌ Menos estable para servicios críticos

**Si vas por prepago:**
- Cargar $1,500-2,500 ARS/mes
- Activar recarga automática si es posible
- Tener alerta de saldo bajo

---

## 🛠️ Stack Tecnológico Recomendado

### **Para conectar tu bot actual a WhatsApp:**

```
┌─────────────────────────────────────────┐
│  WhatsApp (Usuario)                     │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│  WhatsApp Business API (Meta)           │
│  - Recibe mensajes                      │
│  - Envía respuestas                     │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│  Webhook en tu servidor                 │
│  (Railway/Render/Heroku)                │
│  - Python + FastAPI                     │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│  Tu bot actual (app.py)                 │
│  - Groq API                             │
│  - LangChain                            │
│  - ChromaDB                             │
└─────────────────────────────────────────┘
```

---

## 💻 Servicios de Hosting Recomendados (GRATIS o Económicos)

### **1. Railway.app** - **RECOMENDADO #1**

**Costo:**
- ✅ Tier gratuito: $5 USD de crédito/mes (suficiente para proyectos pequeños)
- ✅ Después: ~$5-10 USD/mes

**Ventajas:**
- ✅ Deploy automático desde GitHub
- ✅ Soporte para Python
- ✅ Base de datos integrada
- ✅ Muy fácil de usar
- ✅ Siempre activo (no se duerme)

---

### **2. Render.com** - **RECOMENDADO #2**

**Costo:**
- ✅ Tier gratuito: Servicios básicos GRATIS
- ✅ Después: ~$7 USD/mes

**Ventajas:**
- ✅ Deploy automático
- ✅ Fácil configuración
- ✅ Buen soporte

**Desventajas:**
- ⚠️ El tier gratuito "se duerme" después de 15 min de inactividad

---

### **3. Heroku** - **Ya NO es gratis**

**Costo:**
- ❌ Desde $7 USD/mes (ya no tiene tier gratuito)

---

## 📋 Pasos Concretos para Empezar

### **SEMANA 1-2: Preparación**

1. ✅ Decidir número (prepago vs postpago)
2. ✅ Comprar chip y activar número
3. ✅ Crear cuenta Facebook Business
4. ✅ Preparar documentación del CDC

### **SEMANA 3-4: Setup Técnico**

1. ✅ Aplicar a WhatsApp Business API
2. ✅ Configurar Railway/Render
3. ✅ Adaptar tu bot para webhooks
4. ✅ Testear en ambiente de desarrollo

### **SEMANA 5-6: Producción**

1. ✅ Deploy a producción
2. ✅ Configurar número en WhatsApp Business API
3. ✅ Testear con usuarios reales
4. ✅ Monitorear conversaciones

### **SEMANA 7-8: Optimización**

1. ✅ Aplicar a Meta for Good
2. ✅ Optimizar respuestas
3. ✅ Documentar proceso

---

## 💰 Resumen de Costos Proyectados

### **Escenario ÓPTIMO (Con Meta for Good):**

| Item | Costo Mensual |
|------|---------------|
| Número postpago | $3,000-5,000 ARS |
| Hosting (Railway) | GRATIS (tier gratis) |
| WhatsApp API | GRATIS (Meta for Good) |
| Groq API | GRATIS (14,400 requests/día) |
| **TOTAL** | **$3,000-5,000 ARS/mes** |
| **USD** | **~$3-5 USD/mes** |

---

### **Escenario REALISTA (Sin Meta for Good):**

| Item | Costo Mensual |
|------|---------------|
| Número postpago | $3,000-5,000 ARS |
| Hosting (Railway) | $5 USD (crédito gratis) |
| WhatsApp API | $0-80 USD (1,000 gratis + excedente) |
| Groq API | GRATIS |
| **TOTAL** | **$3,000-5,000 ARS + $5-85 USD/mes** |
| **ARS** | **~$8,000-15,000 ARS/mes** |

---

### **Escenario MÁXIMO (Alto volumen sin descuentos):**

| Item | Costo Mensual |
|------|---------------|
| Número postpago | $5,000 ARS |
| Hosting (Railway Pro) | $10 USD |
| WhatsApp API | $150 USD (30,000 conv/mes) |
| Groq API | GRATIS |
| **TOTAL** | **$5,000 ARS + $160 USD/mes** |
| **ARS** | **~$45,000 ARS/mes** |

---

## 🎯 MI RECOMENDACIÓN FINAL

### **Para el CDC de 25 de Mayo:**

1. ✅ **Empezar con:** WhatsApp Business API + Railway (GRATIS por 1-2 meses)
2. ✅ **Número:** Postpago básico ($3,000-5,000 ARS/mes)
3. ✅ **Aplicar inmediatamente a:** Meta for Good
4. ✅ **Presupuesto inicial:** $5,000-10,000 ARS/mes
5. ✅ **Objetivo:** Conseguir aprobación Meta for Good = GRATIS permanente

---

## 📚 Recursos Útiles

### **Documentación:**
- WhatsApp Business API: https://developers.facebook.com/docs/whatsapp
- Meta for Good: https://www.facebook.com/business/nonprofits
- Railway: https://railway.app
- Render: https://render.com

### **Tutoriales:**
- Conectar bot a WhatsApp: https://developers.facebook.com/docs/whatsapp/cloud-api/get-started
- Python + WhatsApp: https://github.com/tabulon-ext/python-whatsapp-bot

---

## 🤝 ¿Necesitas Ayuda?

Si decides ir por este camino, puedo ayudarte con:
1. ✅ Adaptar tu bot actual para WhatsApp
2. ✅ Configurar webhooks en Railway/Render
3. ✅ Documentar el proceso
4. ✅ Preparar documentación para Meta for Good

---

**💚 ¡El CDC merece tener un bot en WhatsApp accesible para toda la comunidad!**

*Última actualización: Noviembre 2025*

