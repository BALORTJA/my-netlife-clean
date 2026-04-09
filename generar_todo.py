import pandas as pd
import json
import random
import string

# archivo original
archivo_excel = "alumnos_con_id.xlsx"

df = pd.read_excel(archivo_excel)

# función para contraseña
def generar_password(longitud=6):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

usuarios = {}

# crear columnas nuevas
usuarios_lista = []
passwords_lista = []

for i, row in df.iterrows():
    usuario = f"ALUMNO{i+1}"   # puedes cambiar formato si quieres
    password = generar_password()

    usuarios_lista.append(usuario)
    passwords_lista.append(password)

    usuarios[usuario] = password

# añadir al excel
df["Usuario"] = usuarios_lista
df["Password"] = passwords_lista

# guardar nuevo excel
df.to_excel("alumnos_final.xlsx", index=False)

# guardar json para la web
with open("WEB_OK/usuarios.json", "w") as f:
    json.dump(usuarios, f)

print("✅ Excel + JSON creados")