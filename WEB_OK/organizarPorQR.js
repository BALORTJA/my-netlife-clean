const fs = require("fs");
const path = require("path");
const Jimp = require("jimp").default;
const QrCode = require("qrcode-reader");

const carpetaFotos = path.join(__dirname, "public", "fotos");

async function leerQR(ruta) {
  try {
    const image = await Jimp.read(ruta);

    return new Promise((resolve) => {
      const qr = new QrCode();

      qr.callback = (err, value) => {
        if (err || !value) return resolve(null);
        resolve(value.result);
      };

      qr.decode(image.bitmap);
    });

  } catch (error) {
    return null;
  }
}

async function procesar() {
  const archivos = fs.readdirSync(carpetaFotos);

  let alumnoActual = null;

  for (const archivo of archivos) {
    const ruta = path.join(carpetaFotos, archivo);

    if (!archivo.match(/\.(jpg|jpeg|png)$/i)) continue;

    console.log("Procesando:", archivo);

    const qr = await leerQR(ruta);

    if (qr) {
      console.log("QR detectado:", qr);

      alumnoActual = qr.replace(/[^a-z0-9]/gi, "_");

      const carpetaAlumno = path.join(carpetaFotos, alumnoActual);

      if (!fs.existsSync(carpetaAlumno)) {
        fs.mkdirSync(carpetaAlumno);
      }

      // ❌ eliminar QR
      fs.unlinkSync(ruta);
      continue;
    }

    if (alumnoActual) {
      const destino = path.join(carpetaFotos, alumnoActual, archivo);
      fs.renameSync(ruta, destino);
      console.log("Movida a:", alumnoActual);
    } else {
      console.log("⚠️ Foto sin QR previo:", archivo);
    }
  }

  console.log("✅ PROCESO TERMINADO");
}

procesar();