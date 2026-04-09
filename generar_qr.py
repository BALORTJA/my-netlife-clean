import pandas as pd
import qrcode
import os
import uuid
from PIL import Image, ImageDraw, ImageFont
import textwrap

BASE_URL = "https://sweet-flan-9d5184.netlify.app"
# crear carpetas base
os.makedirs("qr", exist_ok=True)
os.makedirs("fotos", exist_ok=True)

# leer Excel
df = pd.read_excel("alumnos.xlsx")
df = df.dropna(subset=["Nombre"])

ids = []

for index, row in df.iterrows():

    # =========================
    # 🧠 DATOS LIMPIOS
    # =========================
    colegio = str(row["Colegio"]).strip().upper()
    etapa = str(row["Etapa"]).strip()

    curso_val = row["Curso"]
    letra_val = row["Letra"]

    if pd.isna(curso_val):
        curso = ""
    else:
        curso = str(int(float(curso_val)))

    letra = "" if pd.isna(letra_val) else str(letra_val).strip().upper()

    nombre_archivo = f"{row['Nombre']}_{row['Apellidos']}".replace(" ", "_")

    # =========================
    # 📁 CREAR CARPETAS
    # =========================
    ruta_carpeta = f"fotos/{colegio}/{etapa}/{curso}{letra}"
    os.makedirs(ruta_carpeta, exist_ok=True)

    # =========================
    # 🆔 ID + URL
    # =========================
    alumno_id = str(uuid.uuid4())[:8]
    ids.append(alumno_id)

    url = f"{BASE_URL}?colegio={colegio}&id={alumno_id}"

    # =========================
    # 🔳 GENERAR QR
    # =========================
    qr = qrcode.make(url)
    qr = qr.convert("RGB")

    width, height = qr.size

    new_img = Image.new("RGB", (width, height + 260), "white")
    new_img.paste(qr, (0, 0))

    draw = ImageDraw.Draw(new_img)

    # =========================
    # 🧠 TEXTO NOMBRE
    # =========================
    nombre_completo = f"{row['Nombre']} {row['Apellidos']}"

    lineas_nombre = textwrap.wrap(nombre_completo, width=22)
    lineas_nombre = lineas_nombre[:2]

    # =========================
    # 🔤 FUENTES
    # =========================
    try:
        font_big = ImageFont.truetype("arial.ttf", 34)
        font_small = ImageFont.truetype("arial.ttf", 30)
    except:
        font_big = None
        font_small = None

    # =========================
    # 🧾 TEXTO FINAL
    # =========================
    linea_curso = f"{etapa} - {curso}º{letra}"
    linea_colegio = colegio

    # =========================
    # ✏️ DIBUJAR TEXTO
    # =========================
    y = height + 20

    for linea in lineas_nombre:
        bbox = draw.textbbox((0, 0), linea, font=font_big)
        w = bbox[2] - bbox[0]
        x = (width - w) // 2

        draw.text((x, y), linea, fill="black", font=font_big)
        y += 45

    # curso
    bbox2 = draw.textbbox((0, 0), linea_curso, font=font_small)
    w2 = bbox2[2] - bbox2[0]
    x2 = (width - w2) // 2

    draw.text((x2, y + 10), linea_curso, fill="black", font=font_small)

    # colegio
    bbox3 = draw.textbbox((0, 0), linea_colegio, font=font_small)
    w3 = bbox3[2] - bbox3[0]
    x3 = (width - w3) // 2

    draw.text((x3, y + 60), linea_colegio, fill="gray", font=font_small)

    # =========================
    # 💾 GUARDAR QR
    # =========================
    qr_filename = f"qr/{nombre_archivo}_{alumno_id}.png"
    new_img.save(qr_filename)

    # 👉 TAMBIÉN GUARDAR COPIA EN SU CARPETA
    foto_filename = f"{ruta_carpeta}/{nombre_archivo}_{alumno_id}.png"
    new_img.save(foto_filename)

# =========================
# 📊 GUARDAR EXCEL
# =========================
df["id"] = ids
df.to_excel("alumnos_con_id.xlsx", index=False)

print("✅ TODO LISTO: QRs + carpetas organizadas 🔥")