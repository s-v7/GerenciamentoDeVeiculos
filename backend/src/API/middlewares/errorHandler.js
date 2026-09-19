const AppError = require('../errors/AppError');

const errorHandler = (err, req, res, next) => {
  console.error("Erro capturado:", err.stack);
  if(err instanceof AppError) {
    return res.status(err.statusCode).json({
	error: err.message,
	...(err.details && { detalhes: err.details })
    });
  }
  if (err.name === 'TypeError' || err.name === 'AboutError') {
    return res.status(502).json({
	error: "Serviços de Machine Learning indisponível ou fora do ar",
	details: err.message
    });
  }
  console.error("Erro inesperado:", err);

  res.status(err.status || 500).json({
    error: err.message || "Erro interno do servidor",
    status: err.status || 500
  });
};

module.exports = errorHandler;
