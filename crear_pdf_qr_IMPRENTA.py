from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from PIL import Image as PILImage
import os

# 🏫 CONFIG
COLEGIO = "MARISTAS"
CARPETA_QR = "qr"
PDF_SALIDA = f"QR_{COLEGIO}.pdf"

styles = getSampleStyleSheet()

# ✂️ línea de corte
def linea_corte(canvas, doc):
    width, height = A4
    canvas.setLineWidth(1)
    canvas.line(width * 0.2, height / 2, width * 0.8, height / 2)

# 📄 documento
doc = SimpleDocTemplate(
    PDF_SALIDA,
    pagesize=A4,
    topMargin=1*cm,
    bottomMargin=1*cm
)

elementos = []

qr_files = sorted(os.listdir(CARPETA_QR))

contador = 0

for archivo in qr_files:
    if not archivo.lower().endswith(".png"):
        continue

    ruta = os.path.join(CARPETA_QR, archivo)

    # 🔥 asegurar proporción correcta
    pil_img = PILImage.open(ruta)
    w, h = pil_img.size
    aspect = h / w

    ancho = 7 * cm
    alto = ancho * aspect

    img = Image(ruta, width=ancho, height=alto)

    # 🏷️ nombre limpio
    nombre = archivo.replace(".png", "").replace("_", " ")

    texto = Paragraph(f"<b>{nombre}</b>", styles["Normal"])

    # 📦 bloque compacto
    elementos.append(texto)
    elementos.append(Spacer(1, 0.3*cm))
    elementos.append(img)
    elementos.append(Spacer(1, 0.8*cm))

    contador += 1

    # 📄 cada 2 → nueva página
    if contador % 2 == 0:
        elementos.append(PageBreak())

# construir PDF
doc.build(elementos, onFirstPage=linea_corte, onLaterPages=linea_corte)

print(f"🔥 PDF creado correctamente: {PDF_SALIDA}")