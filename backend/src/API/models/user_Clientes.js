// export default function (cliente) {
const Sequelize = require("sequelize");
const banco = require("../configs/conexao_Db.js");

const Clientes = banco.define(
  "cliente",
  {
    id_user: {
      type: Sequelize.INTEGER,
      allowNull: false,
      primaryKey: true,
      autoIncrement: true
    },
    nome: {
      type: Sequelize.STRING(35),
      allowNull: false
    },
    idade: {
      type: Sequelize.STRING(35),
      allowNull: false
    },
    cidade: {
      type: Sequelize.STRING(45),
      allowNull: false
    },
    estado: {
      type: Sequelize.INTEGER,
      allowNull: false
    },
    profissao: {
      type: Sequelize.STRING(20),
      allowNull: false
    },
    objeto: {
      type: Sequelize.STRING(35),
      allowNull: true
    }
  },
  {
    freezeTableName: true,
    timestamps: false
  }
);

module.exports = Clientes;
