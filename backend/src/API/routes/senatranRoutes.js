const express = require("express");
const senatranController = require("../controllers/senatranController");
const authMiddleware = require("../middlewares/authMiddleware");

const router = express.Router();

router.use(authMiddleware);

/**
 * @openapi
 * /api/senatran/marcas:
 *   get:
 *     summary: Lista marcas oficiais cadastradas no SENATRAN
 *     tags:
 *       - SENATRAN
 *     security:
 *       - bearerAuth: []
 */
router.get("/marcas", senatranController.listMarcas);

/**
 * @openapi
 * /api/senatran/modelos:
 *   get:
 *     summary: Lista modelos oficiais de uma marca cadastrada no SENATRAN
 *     tags:
 *       - SENATRAN
 *     security:
 *       - bearerAuth: []
 */
router.get("/modelos", senatranController.listModelos);


router.get("/mapa/frota-uf", senatranController.getFrotaPorUF);


router.get("/mapa/frota-municipios", senatranController.getFrotaPorMunicipio);

module.exports = router;
