import pandas as pd
import json
import os
import random
import string

# 📂 Archivo Excel
archivo_excel = "alumnos.xlsx"

# 📂 Carpeta salida
carpeta_salida = "WEB_OK"

# 🔐 Generador de contraseña
def generar_password():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

# 📖 Leer Excel
df = pd.read_excel(archivo_excel)

usuarios = {}

for i, fila in df.iterrows():
    usuario = str(fila["ALUMNO"]).strip().upper()

    # Puedes cambiar esto si quieres contraseñas simples
    password = usuario
    # password = usuario  ← (opción fácil)

    usuarios[usuario] = {
        "password": password
    }

# 📁 Crear carpeta si no existe
os.makedirs(carpeta_salida, exist_ok=True)

# 💾 Guardar JSON
ruta_json = os.path.join(carpeta_salida, "usuarios.json")

with open(ruta_json, "w", encoding="utf-8") as f:
    json.dump(usuarios, f, indent=2)

print("✅ usuarios.json generado correctamente")