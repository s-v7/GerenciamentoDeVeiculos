cat <<EOF > README.md
# Gerenciamento de Veículos

Sistema completo com frontend em **React + Vite** e backend em **Node.js + Express + Sequelize** conectado ao banco **PostgreSQL**.

## Tecnologias

- **Frontend:** React 19, Vite, Axios, TailwindCSS
- **Backend:** Node.js, Express, Sequelize ORM
- **Banco:** PostgreSQL
- **Autenticação:** JWT

---

## Como executar o projeto

### Backend

\`\`\`bash
cd backend
npm install
npm start
\`\`\`

Crie um \`.env\` com:

\`\`\`env
DB_HOST=localhost
DB_PORT=5432
DB_USER=sv7_user
DB_PASSWORD=silasvc07x
DB_DATABASE=gerenciamento_veiculos
DB_DIALECT=postgres
JWT_SECRET=seu_token_secreto
\`\`\`

### Frontend

\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

---

## Login de exemplo

- **Email:** silas@email.com  
- **Senha:** (a definida com hash no banco)

---

## Funcionalidades

- [x] Login com JWT
- [x] Listagem de veículos
- [x] Cadastro e edição
- [x] Exclusão de veículos
- [ ] Upload de imagem (em breve)

---

## Estrutura

\`\`\`bash
GerenciamentoDeVeiculos/
├── backend/
│   └── src/API/...   # API Express com Sequelize
├── frontend/
│   └── src/...       # React com Vite
├── .env              # (ignorado)
├── .gitignore
└── README.md
\`\`\`

---

## Licença

MIT © Silas Vieira
EOF
