const express = require("express");
const routes = require("./routes/userRoutes");
const server = express();
const PORT = 80;

server.use(express.urlencoded({ extended: true }));
server.use(routes);

server.listen(PORT, () => {
  console.log("Servidor http rodando na porta " + PORT + "...");
});
