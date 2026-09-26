const { Sequelize, Op } = require("sequelize");
const SenatranMarcaModelo = require("../models/SenatranMarcaModelo");
const asyncHandler = require("../utils/asyncHandler");

const senatranController = {};

senatranController.listMarcas = asyncHandler(async (req, res) => {
  const { q } = req.query;
  const where = q ? { marca: { [Op.iLike]: `${q}%` } } : {};

  const marcas = await SenatranMarcaModelo.findAll({
    attributes: [[Sequelize.fn("DISTINCT", Sequelize.col("marca")), "marca"]],
    where,
    order: [["marca", "ASC"]],
    limit: 50,
    raw: true
  });

  return res.status(200).json(marcas.map(m => m.marca));
});

senatranController.listModelos = asyncHandler(async (req, res) => {
  const { marca, q } = req.query;
  if (!marca) {
    return res.status(400).json({ error: "O parâmetro 'marca' é obrigatório." });
  }

  const where = { marca: marca.toUpperCase() };
  if (q) where.modelo = { [Op.iLike]: `%${q}%` };

  const modelos = await SenatranMarcaModelo.findAll({
    attributes: [[Sequelize.fn("DISTINCT", Sequelize.col("modelo")), "modelo"]],
    where,
    order: [["modelo", "ASC"]],
    limit: 50,
    raw: true
  });

  return res.status(200).json(modelos.map(m => m.modelo));
});

senatranController.getFrotaPorUF = asyncHandler(async (req, res) => {
  const { marca, modelo } = req.query;
  const where = {};

  if (marca) where.marca = marca.toUpperCase();
  if (modelo) where.modelo = { [Op.iLike]: `%${modelo.toUpperCase()}%` };

  const dadosUF = await SenatranMarcaModelo.findAll({
    attributes: [
      "uf",
      [Sequelize.fn("SUM", Sequelize.col("quantidade")), "totalVeiculos"]
    ],
    where,
    group: ["uf"],
    order: [[Sequelize.literal('"totalVeiculos"'), "DESC"]],
    raw: true
  });

  return res.status(200).json(dadosUF);
});

senatranController.getFrotaPorMunicipio = asyncHandler(async (req, res) => {
  const { uf, marca, limit = 20 } = req.query;
  const where = {};

  if (uf) {
    const ufClean = decodeURIComponent(uf)
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toUpperCase();

    where.uf = { [Op.iLike]: `%${ufClean}%` };
  }

  if (marca) where.marca = marca.toUpperCase();

  const dadosMunicipios = await SenatranMarcaModelo.findAll({
    attributes: [
      "uf",
      "municipio",
      [Sequelize.fn("SUM", Sequelize.col("quantidade")), "totalVeiculos"]
    ],
    where,
    group: ["uf", "municipio"],
    order: [[Sequelize.literal('"totalVeiculos"'), "DESC"]],
    limit: parseInt(limit, 10),
    raw: true
  });

  return res.status(200).json(dadosMunicipios);
});

module.exports = senatranController;
