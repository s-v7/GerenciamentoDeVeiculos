const { Sequelize } = require("sequelize");
require("dotenv").config();

const Conexao_Db = new Sequelize(
  process.env.DB_DATABASE,
  process.env.DB_USER,
  process.env.DB_PASSWORD,
  {
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    dialect: process.env.DB_DIALECT,
    logging: false,
  }
);

// Testar conexão
Conexao_Db.authenticate()
  .then(() => {
    console.log("Banco de Dados conectado com sucesso!");
  })
  .catch((err) => {
    console.error("Erro ao conectar ao Banco de Dados:", err);
  });

module.exports = Conexao_Db;
