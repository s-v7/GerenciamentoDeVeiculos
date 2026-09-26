const { Sequelize } = require("sequelize");
require("dotenv").config();

const connDb = new Sequelize(
  process.env.DB_DATABASE || "veiculos_db",
  process.env.DB_USER || "postgres",
  process.env.DB_PASSWORD || "silasvc07",
  {
    host: process.env.DB_HOST || "localhost",
    port: parseInt(process.env.DB_PORT, 10) || 5432,
    dialect: process.env.DB_DIALECT || "postgres",
    logging: false,
    pool: {
      max: 10,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
  }
);

module.exports = connDb;
