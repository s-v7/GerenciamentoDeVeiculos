const mlService = require("../services/mlServices");
const asyncHandler = require('../utils/asyncHandler');

const mlController = {};

mlController.predictPrice = asyncHandler(async (req, res) => {
  try {
    const prediction = await mlService.predictPrice(req.body);
    res.status(200).json(prediction);
  } catch (err) {
    res.status(502).json({
      error: "Erro ao consultar o serviço de Machine Learning",
      message: err.message,
    });
  }
});

module.exports = mlController;
