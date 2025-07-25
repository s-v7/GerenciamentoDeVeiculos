const veiculo = require("../models/veiculos");

const veiculosController = {};

// Buscar todos
veiculosController.findAll = async (req, res) => {
  try {
    const data = await veiculo.findAll({ raw: true });
    res.status(200).json(data);
  } catch (err) {
    res.status(500).send("Erro ao listar veículos: " + err.message);
  }
};

// Buscar por ID
veiculosController.find = async (req, res) => {
  try {
    const data = await veiculo.findOne({
      raw: true,
      where: { id_veiculo: req.params.id },
    });

    if (!data) return res.status(404).send("Veículo não encontrado");

    res.status(200).json(data);
  } catch (err) {
    res.status(500).send("Erro ao buscar veículo: " + err.message);
  }
};

// Criar novo
veiculosController.create = async (req, res) => {
  try {
    const novoVeiculo = await veiculo.create({
      modelo: req.body.modeloVeiculo,
      marca: req.body.fabricante,
      anoVeiculo: req.body.anoVeiculo,
      placa: req.body.placa,
      corVeiculo: req.body.corVeiculo,
    });

    res.status(201).json(novoVeiculo);
  } catch (err) {
    res.status(500).send("Erro ao criar veículo: " + err.message);
  }
};

// Atualizar
veiculosController.update = async (req, res) => {
  try {
    const result = await veiculo.update(
      {
        modelo: req.body.modeloVeiculo,
        marca: req.body.fabricante,
        anoVeiculo: req.body.anoVeiculo,
        placa: req.body.placa,
        corVeiculo: req.body.corVeiculo,
      },
      { where: { id_veiculo: req.params.id } }
    );

    res.status(200).send("Veículo atualizado com sucesso");
  } catch (err) {
    res.status(500).send("Erro ao atualizar veículo: " + err.message);
  }
};

// Deletar
veiculosController.delete = async (req, res) => {
  try {
    const deleted = await veiculo.destroy({
      where: { id_veiculo: req.params.id },
    });

    if (!deleted) return res.status(404).send("Veículo não encontrado");

    res.status(200).send("Veículo removido com sucesso");
  } catch (err) {
    res.status(500).send("Erro ao apagar veículo: " + err.message);
  }
};

module.exports = veiculosController;
