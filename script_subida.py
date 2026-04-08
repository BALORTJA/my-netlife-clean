import os
import cv2
from pyzbar.pyzbar import decode
from supabase import create_client

# CONFIG
SUPABASE_URL = "https://yrgwrrqekropjnlycxfb.supabase.co"
SUPABASE_KEY = "sb_publishable_atpzyLUPdoHRrh0b4EkDtg_DqQDxUMy"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

FOTOS_FOLDER = "fotos"

print("🚀 INICIO")

current_student = None

for archivo in os.listdir(FOTOS_FOLDER):
    ruta = os.path.join(FOTOS_FOLDER, archivo)

    img = cv2.imread(ruta)
    codigos = decode(img)

    print("\nProcesando:", archivo)

    # Detectar QR
    if codigos:
        current_student = codigos[0].data.decode("utf-8")
        print("🎯 Alumno detectado:", current_student)
        continue

    # Subir foto si hay alumno
    if current_student:
        try:
            with open(ruta, "rb") as f:
                file_bytes = f.read()

            file_name = f"{current_student}/{archivo}"

            supabase.storage.from_("photos").upload(
                file_name,
                file_bytes
            )

            print("✅ Foto subida para:", current_student)

        except Exception as e:
            print("❌ Error subiendo:", e)