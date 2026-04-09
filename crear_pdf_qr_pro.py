from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Image, Spacer, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
import os

# 📁 CONFIG
CARPETA_QR = "qr"
PDF_SALIDA = "QR_PRO_IMPRIMIR.pdf"

doc = SimpleDocTemplate(PDF_SALIDA, pagesize=A4)

styles = getSampleStyleSheet()

elementos = []

qr_files = sorted(os.listdir(CARPETA_QR))

contador = 0

for archivo in qr_files:
    if not archivo.lower().endswith(".png"):
        continue

    ruta = os.path.join(CARPETA_QR, archivo)

    # 🧾 Nombre limpio (sin .png)
    nombre = archivo.replace(".png", "").replace("_", " ")

    # 🖼️ QR grande
    img = Image(ruta)
    img.drawHeight = 8 * cm
    img.drawWidth = 8 * cm

    # 🏷️ Texto
    texto = Paragraph(f"<b>{nombre}</b>", styles["Title"])

    # 📦 Bloque QR
    elementos.append(Spacer(1, 1*cm))
    elementos.append(texto)
    elementos.append(Spacer(1, 0.5*cm))
    elementos.append(img)
    elementos.append(Spacer(1, 2*cm))

    contador += 1

    # 📄 salto cada 2 QR
    if contador % 2 == 0:
        elementos.append(PageBreak())

# construir PDF
doc.build(elementos)

print("✅ PDF PRO creado:", PDF_SALIDA)