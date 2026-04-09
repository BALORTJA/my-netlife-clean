import pandas as pd
import json

# archivo generado antes
archivo_excel = "alumnos_con_id.xlsx"

df = pd.read_excel(archivo_excel)

usuarios = {}

for _, row in df.iterrows():
    usuarios[row["Usuario"]] = row["Password"]

# guardar json
with open("WEB_OK/usuarios.json", "w") as f:
    json.dump(usuarios, f)

print("✅ usuarios.json creado")