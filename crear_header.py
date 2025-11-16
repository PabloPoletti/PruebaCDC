"""
Script para crear la imagen del header combinando los logos institucionales
con el texto del Centro de Día Comunitario
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Cargar la imagen de logos institucionales
logos_path = "images/logos_institucionales.jpg"
output_path = "images/header_cdc.jpg"

if not os.path.exists(logos_path):
    print(f"Error: No se encuentra la imagen {logos_path}")
    exit(1)

# Abrir la imagen
img = Image.open(logos_path)
width, height = img.size

print(f"Dimensiones originales: {width}x{height}")

# Crear una nueva imagen con área verde reducida (la mitad del área celeste)
verde_height = height // 2  # Área verde = mitad del área celeste
new_height = height + verde_height  # Altura total = logos + área verde
new_img = Image.new('RGB', (width, new_height), color='#3b9b8f')  # Color verde CDC

# Pegar la imagen de logos en la parte inferior
new_img.paste(img, (0, verde_height))

# Crear objeto para dibujar
draw = ImageDraw.Draw(new_img)

# Intentar usar fuentes del sistema (si no están disponibles, usar la por defecto)
try:
    # Fuente MUCHO más grande para el título principal
    font_title = ImageFont.truetype("arial.ttf", 120)
    # Fuente grande para el subtítulo
    font_subtitle = ImageFont.truetype("arial.ttf", 80)
except:
    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 120)
        font_subtitle = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 80)
    except:
        print("Usando fuente por defecto")
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()

# Texto a agregar (sin emojis para evitar problemas)
title = "Centro de Dia Comunitario"
subtitle = "25 de Mayo - La Pampa"

# Calcular posiciones para centrar el texto en el área verde (más pequeña)
# Para el título
bbox_title = draw.textbbox((0, 0), title, font=font_title)
title_width = bbox_title[2] - bbox_title[0]
title_height = bbox_title[3] - bbox_title[1]
title_x = (width - title_width) // 2

# Calcular altura total de los dos textos con espacio
bbox_subtitle = draw.textbbox((0, 0), subtitle, font=font_subtitle)
subtitle_width = bbox_subtitle[2] - bbox_subtitle[0]
subtitle_height = bbox_subtitle[3] - bbox_subtitle[1]
total_text_height = title_height + 30 + subtitle_height  # 30px de espacio entre textos

# Centrar verticalmente todo el bloque de texto en el área verde
title_y = (verde_height - total_text_height) // 2

# Para el subtítulo
subtitle_x = (width - subtitle_width) // 2
subtitle_y = title_y + title_height + 30  # Debajo del título con espacio

# Dibujar el texto en blanco
draw.text((title_x, title_y), title, fill='white', font=font_title)
draw.text((subtitle_x, subtitle_y), subtitle, fill='white', font=font_subtitle)

# Guardar la imagen
new_img.save(output_path, quality=95)

print(f"Header creado exitosamente: {output_path}")
print(f"Dimensiones finales: {width}x{new_height}")
print(f"")
print(f"Ahora puedes:")
print(f"   1. Verificar la imagen en: {output_path}")
print(f"   2. Subir los cambios con: git add images/header_cdc.jpg")
print(f"   3. Hacer commit: git commit -m 'Agregar header con logos y texto'")
print(f"   4. Push: git push")

