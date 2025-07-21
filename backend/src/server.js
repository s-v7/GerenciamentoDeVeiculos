require("dotenv").config();
const express = require("express");
const cors = require("cors");

const app = express();

// Middlewares
app.use(cors());
app.use(express.json());

// Rotas
const authRoutes = require("./API/routes/authRoutes");
const veiculosRoutes = require("./API/routes/veiculosRoutes");
const userRoutes = require("./API/routes/userRoutes");

app.use("/api/auth", authRoutes);
app.use("/api/veiculos", veiculosRoutes);
app.use("/api/usuarios", userRoutes);

app.get("/", (req, res) => {
  res.send("API Gerenciamento de Veículos está rodando!");
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`API rodando na porta ${PORT}`));
