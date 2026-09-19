# Guia de Contribuição

Obrigado pelo interesse em contribuir para o **Gerenciamento de Veículos API**! Estas diretrizes ajudam a manter o código consistente, seguro e pronto para produção.

---

## Como começar

1. Faça um **fork** do repositório.
2. Crie uma branch para sua funcionalidade ou correção:

   ```bash
   git checkout -b feature/nome-da-sua-feature
   ```

3. Instale as dependências:

   ```bash
   npm install
   ```

4. Crie o arquivo `.env` com base no arquivo de exemplo ou configure as variáveis mínimas:

   ```dotenv
   PORT=3000
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   DB_DATABASE=seu_banco
   DB_DIALECT=postgres
   JWT_SECRET=sua_chave_secreta
   ML_API_URL=http://localhost:8003
   ```

## Padrões de código e arquitetura

### Arquitetura em camadas

- `routes/`: define as rotas e aplica middlewares (`authMiddleware`, `validate`).
- `controllers/`: gerencia requisições e respostas HTTP e chama os serviços/modelos.
- `services/`: contém integrações externas, como chamadas HTTP ao serviço de ML.
- `schemas/`: contém as regras de validação com Zod.
- `models/`: mapeia o banco de dados via Sequelize.

### Validação com Zod

Nenhuma requisição com corpo (`req.body`) deve chegar ao controller sem passar por um schema do Zod via middleware `validate`.

### Segurança e JWT

Todas as rotas privadas de veículos devem utilizar o `authMiddleware`, exigindo o cabeçalho `Authorization: Bearer <TOKEN>`.

## Como testar suas alterações

Antes de abrir um Pull Request, certifique-se de que:

- O servidor Node inicia e permanece ativo sem cair: `npm start`.
- As rotas continuam respondendo corretamente com o Bearer Token ativado.
- Os cenários de erro do Zod foram testados com dados fora do padrão.

## Mensagens de commit

Utilize mensagens claras e objetivas no padrão **Conventional Commits**:

- `feat`: nova funcionalidade
- `fix`: correção de bug
- `docs`: alterações na documentação
- `refactor`: refatoração de código sem alterar regra de negócio
- `test`: adição ou correção de testes

## Enviando um Pull Request

- Garanta que o `CHANGELOG.md` foi atualizado com suas mudanças se for uma nova versão.
- Abra o Pull Request descrevendo o que foi feito e como testar.
