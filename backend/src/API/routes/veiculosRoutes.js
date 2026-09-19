const express = require("express");
const veiculosController = require("../controllers/veiculosController");
const mlController = require("../controllers/mlController");
const authMiddleware = require("../middlewares/authMiddleware");
const validate = require("../middlewares/validate");
const { predictVeiculoSchema } = require("../schemas/veiculoSchema");

const router = express.Router();

router.use(authMiddleware);

/**
 * @openapi
 * /api/veiculos/predict:
 *   post:
 *     summary: Predição de preço do veículo via Inteligência Artificial (TensorFlow)
 *     tags:
 *       - Predição & ML
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/PredictVeiculoInput'
 *     responses:
 *       200:
 *         description: Estimativa calculada com sucesso.
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/PredictResponse'
 *       400:
 *         description: Dados de entrada inválidos (Falha de validação do Zod).
 *       502:
 *         description: Serviço de Machine Learning fora do ar ou inacessível.
 *       504:
 *         description: Tempo limite excedido ao consultar o modelo de ML.
 */
router.post("/predict", validate(predictVeiculoSchema), mlController.predictPrice);

/**
 * @openapi
 * /api/veiculos/cars:
 *   get:
 *     summary: Lista todos os veículos cadastrados
 *     tags:
 *       - Veículos
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Lista de veículos retornada com sucesso.
 *   post:
 *     summary: Cadastra um novo veículo
 *     tags:
 *       - Veículos
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       201:
 *         description: Veículo cadastrado com sucesso.
 */
router.get("/cars", veiculosController.findAll);
router.post("/cars", veiculosController.create);

/**
 * @openapi
 * /api/veiculos/cars/{id}:
 *   get:
 *     summary: Busca veículo por ID
 *     tags:
 *       - Veículos
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *     responses:
 *       200:
 *         description: Dados do veículo.
 *       404:
 *         description: Veículo não encontrado.
 *   put:
 *     summary: Atualiza veículo por ID
 *     tags:
 *       - Veículos
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *     responses:
 *       200:
 *         description: Veículo atualizado.
 *       404:
 *         description: Veículo não encontrado para atualização.
 *   delete:
 *     summary: Remove veículo por ID
 *     tags:
 *       - Veículos
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *     responses:
 *       200:
 *         description: Veículo removido.
 *       404:
 *         description: Veículo não encontrado para remoção.
 */
router.get("/cars/:id", veiculosController.find);
router.put("/cars/:id", veiculosController.update);
router.delete("/cars/:id", veiculosController.delete);

module.exports = router;
