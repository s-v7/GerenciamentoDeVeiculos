class BadRequestError extends Error {
  constructor(message = "Requisição inválida.") {
    super(message);
    this.name = "BadRequestError";
    this.statusCode = 400;
  }
}

module.exports = BadRequestError;
