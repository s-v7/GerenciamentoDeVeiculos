const ML_API_URL = process.env.ML_API_URL || "http://localhost:8003";
const TIMEOUT_MS = parseInt(process.env.ML_TIMEOUT_MS, 10) || 5000;
const BadGatewayError = require('../errors/BadGatewayError');

const mlService = {};

mlService.predictPrice = async (vehicle) => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

  const rs = await fetch(`${ML_API_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(vehicle),
    signal: controller.signal
  });

  clearTimeout(timeoutId);
  if(!rs.ok){
    const errTxt = await rs.text();
    throw new BadGatewayError(`Serviço de ML API respondeu com erro  ${rs.status}: ${errTxt}`);
  }
  return rs.json();
};

module.exports = mlService;
