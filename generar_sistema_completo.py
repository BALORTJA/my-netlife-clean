import pandas as pd
import qrcode
import os
import random
import string

# CONFIG
COLEGIO = "MARISTAS"
URL_BASE = "https://deluxe-tiramisu-fec1f9.netlify.app"

ARCHIVO_EXCEL = "alumnos.xlsx"
CARPETA_QR = "qr"
CARPETA_SALIDA = "salida"

os.makedirs(CARPETA_QR, exist_ok=True)
os.makedirs(CARPETA_SALIDA, exist_ok=True)

# generar contraseña segura
def generar_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

df = pd.read_excel(ARCHIVO_EXCEL)

usuarios = []

for i, row in df.iterrows():
    nombre = row["Nombre"]
    clase = row["Clase"]

    # usuario único
    usuario = f"{clase}_{i+1}"

    password = generar_password()

    # 🔗 QR con usuario (NO contraseña)
    url = f"{URL_BASE}/?id={usuario}"

    qr = qrcode.make(url)

    nombre_archivo = f"{usuario}.png"
    qr.save(os.path.join(CARPETA_QR, nombre_archivo))

    usuarios.append({
        "Nombre": nombre,
        "Clase": clase,
        "Usuario": usuario,
        "Password": password
    })

# guardar excel final
df_final = pd.DataFrame(usuarios)

archivo_salida = os.path.join(CARPETA_SALIDA, f"{COLEGIO}_usuarios.xlsx")
df_final.to_excel(archivo_salida, index=False)

print("✅ SISTEMA GENERADO")