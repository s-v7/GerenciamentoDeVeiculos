# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versioning Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-09-19

### Adicionado
- **Autenticação JWT**: Proteção de rotas com `authMiddleware` e geração de token no endpoint `/api/auth/login`.
- **Segurança e Criptografia**: Hash de senhas com `bcryptjs`.
- **Validação de Dados**: Middleware de validação genérico utilizando esquemas do `Zod` (`predictVeiculoSchema`, `createVeiculoSchema`).
- **CRUD de Veículos**: Endpoints protegidos para listagem, criação, atualização e remoção de veículos em `/api/veiculos/cars`.
- **Integração com ML**: Rota `POST /api/veiculos/predict` conectada via Fetch API ao microserviço de predição em Python/FastAPI (TensorFlow).
- **Tratamento Global de Erros**: Middleware `errorHandler` para captura centralizada de exceções.

### Corrigido
- **Gerenciamento do Event Loop**: Resolução do encerramento prematuro do processo Node.js ajustando o ciclo de conexão e autenticação do pool do Sequelize.
- **Sincronização de Chaves JWT**: Uniformização do `JWT_SECRET` e correção de referências de variáveis no `authMiddleware.js`.
- **Refatoração Estrutural**: Mapeamento e separação clara de responsabilidades entre `controllers`, `services`, `routes` e `schemas`.
