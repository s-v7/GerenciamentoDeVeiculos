const AppError = require('../errors/AppError');

const errorHandler = (err, req, res, next) => {
  if (process.env.NODE_ENV !== 'test') {
    console.error("Erro capturado:", err.stack);
  }

  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: err.message,
      ...(err.details && { detalhes: err.details })
    });
  }

  if (err.name === 'TypeError' && err.message.includes('fetch')) {
    return res.status(502).json({
      error: "Serviço de Machine Learning indisponível ou fora do ar.",
      detalhes: err.message
    });
  }

  if (err.name === 'AbortError') {
    return res.status(504).json({
      error: "Tempo limite de resposta do serviço de Machine Learning excedido."
    });
  }
  return res.status(500).json({ error: "Erro interno no servidor." });
};

module.exports = errorHandler;
