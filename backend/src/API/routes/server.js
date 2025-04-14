
require('dotenv').config();
const express = require('express')
const cors = require('cors')
const appVeiculos = express();

//Importando as Rotas
const userRoutes = require('./userRoutes');
const authRoutes = require('./authRoutes');


// Middleware para aceitar JSON
appVeiculos.use(express.json());

// Middleware para liberar CORS (acesso entre Front e Back)
appVeiculos.use(cors());

// Importar Rotas
const userRoutes = require('./userRoutes'); // Ajustar o caminho se necessário


// Usar rotas
appVeiculos.use('/api/usuarios', userRoutes);
appVeiculos.use('/api/', authRoutes);
// Rota raiz só para teste
appVeiculos.get('/', (req, res) => {
	res.send(' API Gerenciamento de Véiculos está rodando!');
});

//Definir a porta do servidor
const PORT = process.env.PORT || 3000;

appVeiculos.listen(PORT, () => {
	console.log(`Servidor rodando na porta ${PORT}`);
});
