/****Script para implementação Conexão DataBase */
export default function (conexao_Db) {
  /**Conectando com o DataBase  */
  const Sequelize = require("sequelize");
  /**Parametros passados => {("NomeDoBanco", "Usuário", "Senha") an ObjetcJson => {
   * Key: "Value"
   * host: "MáquinaLocal || ....",
   * dialect: "NameTypeToDataBase"}}
   * */
  const Conexao_Db = new Sequelize("clientesVeiculos", "root", "uvwhrst", {
    host: "localhost",
    dialect: "mysql"
  });
  Conexao_Db.authenticate()
    .then(() => {
      console.log("Conectado ao banco de dados");
    })
    .catch((err) => {
      console.log("Erro ao se conectar com banco de dados! " + err);
    });
}

//module.exports = db;
