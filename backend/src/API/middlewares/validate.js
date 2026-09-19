const validate = (schema) => (req, res, next) => {
  if (!req.body) {
    return res.status(400).json({
      error: "Corpo da requisição ausente ou JSON inválido."
    });
  }

  const result = schema.safeParse(req.body);

  if (!result.success) {
    const issues = result.error.issues || result.error.errors || [];
    
    const errors = issues.map(issue => ({
      campo: issue.path.join('.'),
      mensagem: issue.message
    }));

    return res.status(400).json({
      error: "Falha na validação dos dados de entrada",
      detalhes: errors
    });
  }

  req.body = result.data;
  next();
};

module.exports = validate;
