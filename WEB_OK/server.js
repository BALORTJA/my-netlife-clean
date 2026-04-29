require("dotenv").config();

const express = require("express");
const fs = require("fs");
const path = require("path");
const stripe = require("stripe")(process.env.STRIPE_SECRET_KEY);

const app = express();
app.use(express.json());
app.use(express.static("public"));

/* DEBUG */
console.log("PRICE DIGITAL:", process.env.PRICE_DIGITAL);
console.log("PRICE IMPRESA:", process.env.PRICE_IMPRESA);

/* FOTOS (RUTA LIMPIA Y SEGURA) */
app.get("/fotos", (req, res) => {
  const dir = path.join(__dirname, "public", "fotos");

  fs.readdir(dir, (err, files) => {
    if (err) return res.json([]);

    const fotos = files.map(f => "/fotos/" + encodeURIComponent(f));

    res.json(fotos);
  });
});

/* CHECKOUT */
app.post("/crear-checkout", async (req, res) => {
  try {
    const items = req.body.items;

    let line_items = [];

    items.forEach(i => {
      let priceId = i.tipo === "digital"
        ? process.env.PRICE_DIGITAL
        : process.env.PRICE_IMPRESA;

      line_items.push({
        price: priceId,
        quantity: i.cantidad
      });
    });

    /* ENVÍO */
    line_items.push({
      price_data: {
        currency: "eur",
        product_data: { name: "Gastos de envío" },
        unit_amount: 590
      },
      quantity: 1
    });

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ["card"],
      mode: "payment",
      line_items,
      success_url: "http://localhost:3000/success.html",
      cancel_url: "http://localhost:3000/cancel.html"
    });

    res.json({ url: session.url });

  } catch (e) {
    console.log("ERROR:", e);
    res.status(500).send("Error");
  }
});

app.listen(3000, () => {
  console.log("Servidor en http://localhost:3000");
});