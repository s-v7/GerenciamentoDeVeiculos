## Inteligência Artificial

A camada de IA oferece análise de dados e previsão de preços de veículos por meio de um pipeline de Machine Learning e de uma API FastAPI.

---

### Visão geral

```text
Dataset → Preparação → Feature Engineering → Modelos ML → Avaliação
                                                     ↓
                                           ML API (FastAPI)
                                                     ↓
                                            Node.js / Express
```

---

## Machine Learning

### Dados e features

O dataset sintético inicial possui 1.500 registros, com atributos de marca, ano, cilindrada, quilometragem, portas, combustível, câmbio, carroceria, estado e preço.

O pipeline também calcula:

- `vehicle_age`: idade do veículo;
- `km_per_year`: quilometragem média anual.

Variáveis numéricas são normalizadas e variáveis categóricas são convertidas com One-Hot Encoding.

### Modelos e resultados

Foram avaliados Random Forest e uma rede neural com TensorFlow/Keras:

| Modelo | MAE | RMSE | R² |
| --- | ---: | ---: | ---: |
| Random Forest | R$ 4.629,40 | R$ 5.875,47 | 0,9706 |
| TensorFlow | R$ 3.957,03 | R$ 4.993,59 | 0,9787 |

> Os resultados foram obtidos em um dataset sintético e não representam diretamente preços reais de mercado.

---

### Interpretabilidade

As análises incluem:

- Permutation Importance;
- análise de erros e de erros por faixa de preço;
- comparação entre valores previstos e observados;
- avaliação do comportamento do modelo.

---

## Dados da SENATRAN

O projeto possui ingestão e análise dos dados públicos da SENATRAN:

```text
SENATRAN → Ingestion → Parsing → Validação → Classificação
                                           ↓
                    Agregação por UF / município → Features → Analytics / ML
```

A classificação utiliza categorias oficiais, como `CARRO`, `MOTO`, `PESADO`, `IMPLEMENTO`, `OUTRO` e `NAO_CLASSIFICADO`.

Os dados brutos, devido ao tamanho, permanecem fora do versionamento do Git.

---

### Integração com o ML

Foi avaliado se características agregadas da frota estadual poderiam melhorar a previsão individual. Como o dataset de treinamento não possui município, o experimento utiliza apenas contexto estadual.

No dataset sintético, a inclusão dos dados da SENATRAN não produziu melhoria relevante. O experimento foi mantido para validar a arquitetura de dados.

---

## ML API

A previsão está disponível por uma API FastAPI que executa o pipeline de features e o modelo TensorFlow.

### Execução

```bash
uvicorn ai.api.main:app --host 0.0.0.0 --port 8002
```

A API utiliza a porta `8002`.

### Health check

`GET /health` verifica a disponibilidade da API e o carregamento do modelo e do pipeline.

```bash
curl http://localhost:8002/health
```

### Previsão
`POST /predict` — `Content-Type: application/json`
```json
{
  "make": "Toyota",
  "year": 2023,
  "engine_cc": 2000,
  "mileage_km": 25000,
  "doors": 4,
  "fuel_type": "flex",
  "transmission": "automatico",
  "body_type": "sedan",
  "state": "SP"
}
```

Resposta:
```json
{
  "predicted_price": 102355.78,
  "model": "tensorflow"
}
```
Dados, modelos e componentes MCP serão mantidos reutilizáveis para futuras interfaces de chat, dashboards, gráficos, mapas e agentes.
# Detalhamento técnico

Camada de Inteligência Artificial da **Vehicle Intelligence Platform**, responsável por ingestão e preparação de dados, engenharia de features, treinamento, avaliação e disponibilização de modelos de Machine Learning.

A camada também contém experimentos de integração com dados públicos da SENATRAN e uma API FastAPI para inferência do modelo de previsão de preços.

---

## Visão geral detalhada

```text
Data Sources
     ↓
Ingestion
     ↓
Preprocessing
     ↓
Feature Engineering
     ↓
Training
     ↓
Model Evaluation
     ↓
TensorFlow Model
     ↓
FastAPI ML API
     ↓
Node.js / Express
```

A estrutura foi organizada para separar:

- ingestão de dados;
- preparação e transformação;
- engenharia de features;
- treinamento;
- avaliação;
- modelos e artefatos;
- exposição da inferência através de API.

---

## Dataset

### Variáveis

O dataset inicial utilizado para o experimento de previsão de preços possui 1.500 registros sintéticos.

As variáveis incluem:

```text
make
year
engine_cc
mileage_km
doors
fuel_type
transmission
body_type
state
price
```

O dataset é utilizado como base para experimentação e desenvolvimento da pipeline de Machine Learning.

Os resultados apresentados neste projeto foram obtidos sobre dados sintéticos e não representam diretamente preços reais de mercado.

## Feature Engineering

A pipeline adiciona variáveis derivadas para representar características relevantes dos veículos.

---

### Features numéricas

```text
year
engine_cc
mileage_km
doors
vehicle_age
km_per_year
```

---

### Features categóricas

```text
make
fuel_type
transmission
body_type
state
```

---

### Features derivadas

**vehicle_age** representa a idade estimada do veículo.

**km_per_year** representa a quilometragem média anual.

O pipeline aplica:

```text
Numerical Features
        ↓
Normalization

Categorical Features
        ↓
One-Hot Encoding
```

O pipeline processado é persistido em: ai/models/feature_pipeline.pkl

## Machine Learning

Foram avaliados diferentes modelos para a tarefa de regressão de preço.

Atualmente o projeto possui:

- Random Forest;
- TensorFlow / Keras.

Fluxo de treinamento:
```text
Dataset
   ↓
Preprocessing
   ↓
Feature Engineering
   ↓
Train / Validation
   ↓
Model Training
   ↓
Evaluation
   ↓
Model Artifact
```

---

### TensorFlow Model

O modelo principal de previsão utiliza TensorFlow/Keras.

Arquitetura:
```text
Input
  ↓
Dense(64, ReLU)
  ↓
Dense(32, ReLU)
  ↓
Dense(1)
```
Configuração principal:

Optimizer: Adam
Learning Rate: 0.001
Loss: MSE
Metric: MAE
Early Stopping: enabled
Validation Split: 20%

O modelo treinado é armazenado em: **ai/models/car_price_tensorflow.keras**
## Model Evaluation

A camada de avaliação contém scripts para analisar diferentes aspectos do comportamento dos modelos.
```text
Evaluation
├── Metrics
├── Error Analysis
├── Feature Importance
├── Model Behavior
├── Model Comparison
└── SENATRAN Experiments
```

Entre as análises realizadas:

MAE;
RMSE;
R²;
análise de erros;
erros por faixa de preço;
comparação entre modelos;
importância das features;
comportamento das previsões.
### Model Comparison

Resultados registrados durante os experimentos:

| Modelo | MAE | RMSE | R² |
| --- | ---: | ---: | ---: |
| Random Forest | R$ 4.629,40 | R$ 5.875,47 | 0,9706 |
| TensorFlow | R$ 3.957,03 | R$ 4.993,59 | 0,9787 |

Os resultados são específicos do dataset experimental utilizado e não devem ser interpretados como avaliação de desempenho em dados reais de mercado.

---

## SENATRAN Data Engineering

A camada de dados também possui pipelines para ingestão e análise de dados públicos da SENATRAN.
```text
SENATRAN
   ↓
Ingestion
   ↓
Parsing
   ↓
Validation
   ↓
Classification
   ↓
Aggregation
   ↓
Feature Engineering
   ↓
Analytics
```
---

### Vehicle Classification

As categorias utilizadas incluem:

- `CARRO`
- `MOTO`
- `PESADO`
- `IMPLEMENTO`
- `NAO_CLASSIFICADO`
- `OUTRO`

---

### SENATRAN Aggregation

Os dados podem ser processados em diferentes níveis:
```text
SENATRAN
   │
   ├── UF
   │
   └── Município
```
Os pipelines existentes incluem:

agregação por UF;
agregação por município;
classificação de veículos;
distribuição da frota;
geração de features;
análise de qualidade;
experimentos de integração com Machine Learning.

---

### SENATRAN + Machine Learning

Foi realizado um experimento para avaliar se características agregadas da frota estadual poderiam contribuir para a previsão individual de preços.

Fluxo experimental:
```text
SENATRAN
    ↓
State Fleet Aggregation
    ↓
Feature Engineering
    ↓
Vehicle Dataset
    ↓
ML Model
    ↓
Evaluation
```
Como o dataset de treinamento não possui município associado aos veículos, o experimento utiliza contexto estadual.

Nos experimentos realizados com o dataset sintético, a inclusão das características agregadas da SENATRAN não produziu melhoria relevante na previsão.

O experimento foi mantido como parte da investigação arquitetural e da validação da integração entre Data Engineering e Machine Learning.

---

## ML API

A inferência do modelo TensorFlow é disponibilizada através de uma API FastAPI.

### Run
```text
A partir da raiz do projeto:

uvicorn ai.api.main:app --host 0.0.0.0 --port 8003
```

A API fica disponível em:http://localhost:8003

---

### Health Check:  `GET /health`

**Exemplo: curl http://localhost:8003/health**

A resposta confirma a disponibilidade da API e dos componentes necessários para inferência.

### Prediction
```json
POST /predict

Content-Type: application/json
Exemplo:
{
  "make": "Toyota",
  "year": 2023,
  "engine_cc": 2000,
  "mileage_km": 25000,
  "doors": 4,
  "fuel_type": "flex",
  "transmission": "automatico",
  "body_type": "sedan",
  "state": "SP"
}

Resposta:
{
  "predicted_price": 102355.78,
  "model": "tensorflow"
}
```

---

## Integration
A ML API pode ser consumida pelo backend Node.js.
```text
React
  ↓
Node.js / Express
  ↓
ML API
  ↓
FastAPI
  ↓
Feature Pipeline
  ↓
TensorFlow
  ↓
Prediction
```
---

Também existe integração através do MCP Server:
```text
MCP Tool
   ↓
predict_vehicle_price
   ↓
ML API
   ↓
TensorFlow
   ↓
Prediction
```
Essa separação mantém o modelo independente das camadas de aplicação e de integração.

---

## Model Artifacts

Os principais artefatos utilizados pela API são:
```text
ai/models/
├── car_price_tensorflow.keras
├── car_price_model.pkl
└── feature_pipeline.pkl
```
O feature_pipeline.pkl garante que as mesmas transformações utilizadas durante o treinamento sejam aplicadas durante a inferência.

---

## Tests

Os testes relacionados à pipeline de dados estão em: tests/

Execute: pytest

---

## Development

O ambiente Python deve possuir as dependências necessárias para:

- Pandas;
- NumPy;
- Scikit-learn;
- TensorFlow;
- FastAPI;
- Pydantic;
- Joblib.

A versão dos artefatos de Machine Learning deve permanecer compatível com o ambiente utilizado para treinamento e inferência.

---

## Data Versioning

Os dados brutos da SENATRAN possuem grande volume e permanecem fora do versionamento Git.
```text
Raw Data
   ↓
Local / External Storage
   ↓
Processing
   ↓
Processed Data
   ↓
Features / Analytics
```
Artefatos processados pequenos e relevantes para análise podem ser versionados no repositório.

---

## Future Integration

A camada de IA foi projetada para permanecer independente e reutilizável por diferentes interfaces.

Possíveis consumidores futuros:
```text
Web Application
      │
      ├── Dashboard
      ├── Charts
      ├── Maps
      └── Chat Interface
              │
              ▼
          Agent / LLM
              │
              ▼
             MCP
              │
              ▼
        AI Capabilities
```
A integração com LLM, Agents e RAG faz parte do roadmap da plataforma e não representa componentes já implementados nesta camada.

---

## Related Documentation

- `../README.md` — visão geral da Vehicle Intelligence Platform
- `../backend/` — Backend Node.js / Express
- `../frontend/` — Frontend React
- `../backend/mcp/` — MCP Server

## Author: **Silas Vasconcelos Cruz**
**Full Stack Engineer | Enterprise Modernization | DevSecOps | Applied AI**
