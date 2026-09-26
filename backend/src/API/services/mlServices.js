const crypto = require("crypto");
const redis = require("../configs/redis");
const BadGatewayError = require('../errors/BadGatewayError');

const ML_API_URL = process.env.ML_API_URL || "http://localhost:8003";
const TIMEOUT_MS = parseInt(process.env.ML_TIMEOUT_MS, 10) || 5000;
const CACHE_TTL_SECONDS = 3600; 
const mlService = {};

const generateCacheKey = (vehicle) => {
  const sortedPayload = JSON.stringify(vehicle, Object.keys(vehicle).sort());
  const hash = crypto.createHash("md5").update(sortedPayload).digest("hex");
  return `ml:predict:${hash}`;
};

mlService.predictPrice = async (vehicle) => {
  const cacheKey = generateCacheKey(vehicle);
  try {
     const cachedData = await redis.get(cacheKey);
     if(cachedData) {
	return { ...JSON.parse(cachedData), cache: true };
     }
  } catch (err) { 

  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

  const rs = await fetch(`${ML_API_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(vehicle),
    signal: controller.signal
  });

  clearTimeout(timeoutId);
  if(!rs.ok){
    const errTxt = await rs.text();
    throw new BadGatewayError(`Serviço de ML API respondeu com erro  ${rs.status}: ${errTxt}`);
  }
  const result = await rs.json();
  try {
     await redis.set(cacheKey, JSON.stringify(result), "EX", CACHE_TTL_SECONDS);
  } catch (err) {
  }
  return { ...result, cached: false };

};

module.exports = mlService;
