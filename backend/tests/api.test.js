require("dotenv").config();
const request = require("supertest");
const express = require("express");
const errorHandler = require("../src/API/middlewares/errorHandler");
const authRoutes = require("../src/API/routes/authRoutes");
const connDb = require("../src/API/configs/conexaoDb");

const app = express();
app.use(express.json());
app.use("/api/auth", authRoutes);
app.use(errorHandler);

describe("Testes de Integração - Autenticação & Tratamento de Erros", () => {

  afterAll(async () => {
    await connDb.close(); 
  });
  
  test("POST /api/auth/login - Deve rejeitar login com usuário inexistente (HTTP 404)", async () => {
    const res = await request(app)
      .post("/api/auth/login")
      .send({ email: "usuario_inexistente@email.com", senha: "123" });

    expect(res.statusCode).toBe(404);
    expect(res.body).toHaveProperty("error");
  });

  test("POST /api/auth/login - Deve rejeitar senha inválida (HTTP 401)", async () => {
    const res = await request(app)
      .post("/api/auth/login")
      .send({ email: "admin@email.com", senha: "senha_errada" });

    expect(res.statusCode).toBe(401);
    expect(res.body).toHaveProperty("error", "Credenciais inválidas.");
  });

  test("POST /api/auth/login - Deve aceitar credenciais válidas e retornar JWT (HTTP 200)", async () => {
    const res = await request(app)
      .post("/api/auth/login")
      .send({ email: "admin@email.com", senha: "123456" });

    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty("token");
    expect(res.body).toHaveProperty("message", "Login realizado com sucesso");
  });

});
