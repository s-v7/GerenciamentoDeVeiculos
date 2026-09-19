const Veiculo = require("../models/Veiculo");
const asyncHandler = require("../utils/asyncHandler");
const NotFoundError = require("../errors/NotFoundError");

const veiculosController = {};

veiculosController.findAll = asyncHandler(async (req, res) => {
  const dt = await Veiculo.findAll({ raw: true });
  return res.status(200).json(dt);
});

veiculosController.find = asyncHandler(async (req, res) => {
  const dt = await Veiculo.findOne({ where: { id_veiculo: req.params.id } });
  if (!dt) throw new NotFoundError("Veículo não encontrado.");
  
  return res.status(200).json(dt);
});

veiculosController.create = asyncHandler(async (req, res) => {
  const newVeiculo = await Veiculo.create(req.body);
  return res.status(201).json(newVeiculo);
});

veiculosController.update = asyncHandler(async (req, res) => {
  const [affectedRows] = await Veiculo.update(req.body, { where: { id_veiculo: req.params.id } });
  if (affectedRows === 0) throw new NotFoundError("Veículo não encontrado para atualização.");

  return res.status(200).json({ message: "Veículo atualizado com sucesso." });
});

veiculosController.delete = asyncHandler(async (req, res) => {
  const deleted = await Veiculo.destroy({ where: { id_veiculo: req.params.id } });
  if (deleted === 0) throw new NotFoundError("Veículo não encontrado para remoção.");

  return res.status(200).json({ message: "Veículo removido com sucesso." });
});

module.exports = veiculosController;
