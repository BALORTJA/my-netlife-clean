import os
import cv2
from pyzbar.pyzbar import decode
import shutil

# 🏫 CONFIG
COLEGIO = "MARISTAS"

CARPETA_FOTOS = "fotos"
CARPETA_PROCESADO = f"procesado_{COLEGIO}"
CARPETA_WEB = "WEB_OK/fotos"

os.makedirs(CARPETA_PROCESADO, exist_ok=True)
os.makedirs(CARPETA_WEB, exist_ok=True)

alumno_actual = None

print("🚀 PROCESO AUTOMÁTICO INICIADO...\n")

archivos = sorted(os.listdir(CARPETA_FOTOS))

for archivo in archivos:
    ruta = os.path.join(CARPETA_FOTOS, archivo)

    if not archivo.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    print(f"📂 Procesando: {archivo}")

    img = cv2.imread(ruta)

    if img is None:
        print("❌ Error leyendo imagen")
        continue

    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    codigos = decode(gris)

    # 📌 DETECTA QR
    if codigos:
        alumno_actual = codigos[0].data.decode("utf-8").strip()

        print(f"🎯 QR detectado → {alumno_actual}")

        # crear carpeta alumno en procesado
        carpeta_alumno = os.path.join(CARPETA_PROCESADO, alumno_actual)
        os.makedirs(carpeta_alumno, exist_ok=True)

        # crear carpeta en web
        carpeta_web = os.path.join(CARPETA_WEB, alumno_actual)
        os.makedirs(carpeta_web, exist_ok=True)

        continue

    # 📸 FOTO NORMAL
    if alumno_actual:
        destino1 = os.path.join(CARPETA_PROCESADO, alumno_actual, archivo)
        destino2 = os.path.join(CARPETA_WEB, alumno_actual, archivo)

        shutil.copy(ruta, destino1)
        shutil.copy(ruta, destino2)

        print(f"✅ Foto → {alumno_actual}")

    else:
        print("⚠️ Foto sin QR previo")

print("\n🎉 TODO LISTO (PROCESADO + WEB)")