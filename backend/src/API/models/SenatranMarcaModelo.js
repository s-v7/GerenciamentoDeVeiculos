const { DataTypes } = require("sequelize");
const connDb = require("../configs/conexaoDb");

const SenatranMarcaModelo = connDb.define("SenatranMarcaModelo", {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  uf: {
    type: DataTypes.STRING(50), 
    allowNull: false
  },
  municipio: {
    type: DataTypes.STRING(150),
    allowNull: false
  },
  marca: {
    type: DataTypes.STRING(100),
    allowNull: false
  },
  modelo: {
    type: DataTypes.STRING(150),
    allowNull: false
  },
  anoFabricacao: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  quantidade: {
    type: DataTypes.INTEGER,
    defaultValue: 1
  }
}, {
  tableName: "senatran_marca_modelos",
  timestamps: false,
  indexes: [
    { fields: ["marca"] },
    { fields: ["marca", "modelo"] },
    { fields: ["uf"] }
  ]
});

module.exports = SenatranMarcaModelo;
