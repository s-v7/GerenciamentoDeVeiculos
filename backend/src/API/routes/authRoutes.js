const express = require("express");
const authController = require("../controllers/authController");

const router = express.Router();

/**
 * @openapi
 * /api/auth/login:
 *   post:
 *     summary: Autentica o usuário e gera o token JWT
 *     tags:
 *       - Autenticação
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - email
 *               - senha
 *             properties:
 *               email:
 *                 type: string
 *                 example: admin@email.com
 *               senha:
 *                 type: string
 *                 example: "123456"
 *     responses:
 *       200:
 *         description: Login realizado com sucesso.
 *       401:
 *         description: Credenciais inválidas.
 *       404:
 *         description: Usuário não encontrado.
 */
router.post("/login", authController.login);

module.exports = router;
