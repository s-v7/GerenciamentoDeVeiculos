const veiculo = require("../models/veiculos.js");

const veiculosController = {};

//Método buscar todos os Elementos
veiculosController.findAll = function (req, res) {
  veiculo
    .findAll({
      raw: true
    })
    .then(function (data) {
      res.status(200).send(data);
    })
    .catch(function (err) {
      res.status(500).send("Erro ao listar users: " + err);
    });
};

//Método para buscar um Elemento
veiculosController.find = (req, res) => {
  veiculo
    .findOne({
      raw: true,
      where: {
        id_veiculo: req.params.id
      }
    })
    .then((data) => {
      res.status(200).send(data);
    })
    .catch((err) => {
      res.status(500).send("Erro ao buscar um Elemento!");
    });
};
//Método para criar um ELemento
veiculosController.create = (req, res) => {
  veiculo
    .create({
      modelo: req.body.modeloVeiculo,
      marca: req.body.fabricante,
      anoVeiculo: req.body.anoVeiculo,
      placa: req.body.placa,
      corVeiculo: req.params.corVeiculo
    })
    .then((data) => {
      res.sendStatus(200);
    })
    .catch((err) => {
      res.status(500).send("Erro ao criar user: " + err);
    });
};

//Método para Atualizar um Elemento
veiculosController.update = (req, res) => {
  veiculo
    .update(
      {
        modelo: req.body.modeloVeiculo,
        marca: req.body.fabricante,
        anoVeiculo: req.body.anoVeiculo,
        placa: req.body.placa,
        corVeiculo: req.params.corVeiculo
      },
      {
        where: { id_veiculo: req.params.id }
      }
    )
    .then((data) => {
      res.sendStatus(200);
    })
    .catch((err) => {
      res.status(500).send("Erro ao atualizar user: " + err);
    });
};

//Método para Excluir um Elemento
veiculosController.delete = (req, res) => {
  veiculo
    .destroy({
      where: { id_veiculo: req.params.id }
    })
    .then((data) => {
      res.sendStatus(200);
    })
    .catch((err) => {
      res.status(500).send("Erro ao apagar user: " + err);
    });
};
module.exports = veiculosController;
