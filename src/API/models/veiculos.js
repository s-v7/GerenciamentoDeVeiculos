// export default function (Carros) {
const Sequelize = require("sequelize");
const db = require("../configs/conexao_Db.js");
/**definindo um Modelo (Tabela) */
const Carros = db.define(
  "veiculo",
  {
    id_veiculo: {
      type: Sequelize.INTEGER,
      allowNull: false,
      primaryKey: true,
      autoIncrement: true
    },
    modelo: {
      //{title}
      type: Sequelize.STRING(35),
      allowNull: false
    },
    marca: {
      type: Sequelize.STRING(35),
      allowNull: false
    },
    anoVeiculo: {
      type: Sequelize.timestamps,
      allowNull: false
    },
    placa: {
      type: Sequelize.INTEGER,
      allowNull: false
    },
    tipoCombustivel: {
      type: Sequelize.STRING(20),
      allowNull: true
    },
    corVeiculo: {
      type: Sequelize.STRING(35),
      allowNull: true
    }
  },
  {
    id_Cliente: {
      type: Sequelize.INTEGER,
      allowNull: false,
      references: {
        model: "user_Clientes",
        key: "idCliente"
      }
    }
  },
  {
    freezeTableName: true,
    timestamps: false
  }
);

module.exports = Carros;
