
const Redis = require("ioredis");

const REDIS_HOST = process.env.REDIS_HOST || "127.0.0.1";
const REDIS_PORT = parseInt(process.env.REDIS_PORT, 10) || 6379;

const redis = new Redis({
  host: REDIS_HOST,
  port: REDIS_PORT,
  lazyConnect: true,
  maxRetriesPerRequest: 1,
  enableOfflineQueue: false
});

redis.on("error", (err) => {

});

module.exports = redis;
