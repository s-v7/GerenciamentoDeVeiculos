
const { DataTypes } = require('sequilze');
const Conexao_Db = require('../configs/conexao_Db');

const User = Conexao_Db.define('User', {
	id: {
		type: DataTypes.INTEGER,
		autoIncrement: true,
		primaryKey: true
	},
	nome: {
		type: DataTypes.STRING,
		allowNull: false
	},
	email: {
		type: DataTypes.STRING,
		allowNull: false,
		unique: true,
		validate: {
			isEmail: true
		}
	},
	senha: {
		type: DataTypes.STRING,
		allowNull: false
	},
}, {
	tableName: 'usuarios', 
	timestamps: true
});

module.exports = User;
