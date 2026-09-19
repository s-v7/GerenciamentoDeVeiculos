const AppError = require('./AppError');

class BadGatewayError extends AppError {
  constructor(message = "Falha na comunicação com serviço externo", details = null) {
    super(message, 502, details);
  }
}

module.exports = BadGatewayError;
