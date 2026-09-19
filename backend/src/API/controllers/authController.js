const UserLogin = require("../models/UserLogin");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const asyncHandler = require("../utils/asyncHandler");
const NotFoundError = require("../errors/NotFoundError");
const UnauthorizedError = require("../errors/UnauthorizedError");

exports.login = asyncHandler(async (req, res) => {
  const { email, senha } = req.body;

  const user = await UserLogin.findOne({ where: { email } });
  if (!user) {
    throw new NotFoundError("Usuário não encontrado.");
  }

  const senhaValida = await bcrypt.compare(senha, user.senha);
  if (!senhaValida) {
    throw new UnauthorizedError("Credenciais inválidas.");
  }

  const secret = process.env.JWT_SECRET || "chave_secreta_sv7";
  const token = jwt.sign(
    { id: user.id, email: user.email },
    secret,
    { expiresIn: "1d" }
  );

  return res.status(200).json({
    message: "Login realizado com sucesso",
    token,
    user: {
      id: user.id,
      nome: user.nome,
      email: user.email,
    },
  });
});
