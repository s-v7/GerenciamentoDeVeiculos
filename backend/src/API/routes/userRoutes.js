const express = require("express");
const authMiddleware = require("../middlewares/authMiddleware");
const asyncHandler = require("../utils/asyncHandler");
const UserLogin = require("../models/UserLogin");
const NotFoundError = require("../errors/NotFoundError");

const r = express.Router();

r.use(authMiddleware);

r.get("/me", asyncHandler(async (req, res) => {
  const user = await UserLogin.findByPk(req.user.id, {
    attributes: ["id", "nome", "email", "createdAt"]
  });
  
  if (!user) {
    throw new NotFoundError("Usuário não encontrado.");
  }

  return res.status(200).json(user);
}));

module.exports = r;
