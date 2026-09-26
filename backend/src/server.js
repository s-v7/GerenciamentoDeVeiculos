require("dotenv").config();
const express = require("express");
const cors = require("cors");
const helmet = require("helmet");
const rateLimit = require("express-rate-limit");

const connDb = require("./API/configs/conexaoDb");
const errorHandler = require("./API/middlewares/errorHandler");

const authRoutes = require("./API/routes/authRoutes");
const veiculosRoutes = require("./API/routes/veiculosRoutes");
const userRoutes = require("./API/routes/userRoutes");
const senatranRoutes = require("./API/routes/senatranRoutes");

const swaggerUi = require("swagger-ui-express");
const swaggerSpec = require("./API/configs/swagger");

const app = express();
app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerSpec));
app.use(helmet());
app.use(cors({
  origin: process.env.CORS_ORIGIN || "*",
  methods: ["GET", "POST", "PUT", "DELETE"],
  allowedHeaders: ["Content-Type", "Authorization"]
}));

app.use(express.json({ limit: "10Kb" }));
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: "Muitas requisições originadas deste IP. Tente novamente mais tarde." }
});

app.use("/api", limiter);

app.get("/", (req, res) => {
  res.send("API Gerenciamento de Veículos está rodando!");
});

app.get("/health", (req, res) => {
  res.status(200).json({ status: "OK", timestamp: new Date() });
});

app.use("/api/auth", authRoutes);
app.use("/api/veiculos", veiculosRoutes);
app.use("/api/usuarios", userRoutes);

app.use("/api/senatran", senatranRoutes);

app.use(errorHandler);

const PORT = process.env.PORT || 3000;
let server;

connDb
  .authenticate()
  .then(() => {
    console.log("Banco de Dados autenticado via Sequelize Poll!");
    server = app.listen(PORT, () => {
      console.log(`API rodando e escutando na porta ${PORT}`);
    });
  })
  .catch((err) => {
    console.error("Erro fatal ao conectar no banco de dados:", err);
  });

process.on("SIGINT", () => {
  if (server) {
    server.close(() => {
      console.log("Servidor encerrado com sucesso.");
      process.exit(0);
    });
  }
});
