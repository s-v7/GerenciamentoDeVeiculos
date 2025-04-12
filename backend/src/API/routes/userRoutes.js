
const express = require("express");
const veiculosController = require("../controllers/veiculosController");

const routes = express.Router();

routes.get("/cars", veiculosController.findAll);
routes.post("/cars", veiculosController.create);
routes.get("/cars/:{id}", veiculosController.find);
routes.put("/cars/:id", veiculosController.update);
routes.delete("/cars/:{id}", veiculosController.delete);


module.exports = routes;
