import qrcode

dato = "alumno_001"

img = qrcode.make(dato)
img.save("alumno_001.png")

print("QR creado")