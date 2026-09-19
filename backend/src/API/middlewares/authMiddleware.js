const jwt = require("jsonwebtoken");

const authMiddleware = (req, res, next) => {
  const authHeader = req.headers.authorization;

  if (!authHeader) {
    return res
      .status(401)
      .json({ error: "Token de autenticação não fornecido." });
  }

  const parts = authHeader.split(" ");
  if (parts.length !== 2 || parts[0] !== "Bearer") {
    return res.status(401).json({ error: "Formato do token inválido." });
  }

  const token = parts[1];

  try {
    const secret = process.env.JWT_SECRET || "chave_secreta_sv7";
    const decoded = jwt.verify(token, secret);

    req.userId = decoded.id;
    req.user = decoded;

    return next();
  } catch (err) {
    return res.status(401).json({ error: "Token inválido ou expirado." });
  }
};

module.exports = authMiddleware;
