const express = require("express");
const veiculosController = require("../controllers/veiculosController");

const router = express.Router();

router.get("/cars", veiculosController.findAll);
router.get("/cars/:id", veiculosController.find);
router.post("/cars", veiculosController.create);
router.put("/cars/:id", veiculosController.update);
router.delete("/cars/:id", veiculosController.delete);

module.exports = router;
