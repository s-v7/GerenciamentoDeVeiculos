const swaggerJSDoc = require("swagger-jsdoc");

const options = {
  definition: {
    openapi: "3.0.0",
    info: {
      title: "Gerenciamento de Veículos & Predição de Preços API",
      version: "1.0.0",
      description:
        "API RESTful para gestão de veículos, autenticação JWT e inteligência artificial para estimativa de preços via microserviço TensorFlow.",
      contact: {
        name: "Suporte Técnico",
        email: "admin@email.com",
      },
    },
    servers: [
      {
        url: "http://localhost:3000",
        description: "Servidor de Desenvolvimento Local",
      },
    ],
    components: {
      securitySchemes: {
        bearerAuth: {
          type: "http",
          scheme: "bearer",
          bearerFormat: "JWT",
          description: "Insira o token JWT gerado na rota /api/auth/login",
        },
      },
      schemas: {
        PredictVeiculoInput: {
          type: "object",
          required: [
            "make",
            "year",
            "engine_cc",
            "mileage_km",
            "doors",
            "fuel_type",
            "transmission",
            "body_type",
            "state",
          ],
          properties: {
            make: { type: "string", example: "Toyota" },
            year: { type: "integer", example: 2023 },
            engine_cc: { type: "integer", example: 2000 },
            mileage_km: { type: "integer", example: 25000 },
            doors: { type: "integer", example: 4 },
            fuel_type: { type: "string", example: "flex" },
            transmission: { type: "string", example: "automatico" },
            body_type: { type: "string", example: "sedan" },
            state: { type: "string", example: "SP" },
          },
        },
        PredictResponse: {
          type: "object",
          properties: {
            predicted_price: { type: "number", example: 102355.78 },
            model: { type: "string", example: "tensorflow" },
          },
        },
        ErrorResponse: {
          type: "object",
          properties: {
            error: { type: "string", example: "Mensagem detalhada do erro" },
            detalhes: { type: "string", example: "Contexto adicional do erro" },
          },
        },
      },
    },
  },
  apis: ["./src/API/routes/*.js"], // Mapeia as anotações JSDoc dentro dos arquivos de rotas
};

const swaggerSpec = swaggerJSDoc(options);

module.exports = swaggerSpec;
