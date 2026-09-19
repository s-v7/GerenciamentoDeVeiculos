const AppError = require('./AppError');

class NotFoundError extends AppError {
  constructor(message = "Recurso não encontrado"){
    super(message, 404);
  }
}

module.exports = NotFoundError;
