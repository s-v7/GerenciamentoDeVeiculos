# Vehicle Intelligence Platform

Plataforma experimental para gerenciamento, análise e inteligência aplicada a dados de veículos.

O projeto evoluiu de um sistema CRUD tradicional para uma arquitetura que integra:

- Backend Node.js / Express
- React
- PostgreSQL
- Data Engineering
- Dados da SENATRAN
- Machine Learning com TensorFlow
- ML API com FastAPI
- Model Evaluation
- Model Comparison
- MCP Server
- Integração MCP → ML

O objetivo é explorar uma arquitetura na qual dados, análises e modelos de Machine Learning possam futuramente ser expostos como capacidades para sistemas baseados em LLM e Agents.

---

## Arquitetura

```text
                         ┌─────────────────────┐
                         │       React         │
                         │     Frontend        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Node.js / Express │
                         │       Backend       │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
                    ▼               ▼                ▼
             ┌────────────┐  ┌────────────┐  ┌────────────┐
             │ PostgreSQL │  │   ML API   │  │ MCP Server │
             │            │  │  FastAPI   │  │ TypeScript │
             └────────────┘  └─────┬──────┘  └─────┬──────┘
                                   │               │
                                   ▼               │
                              ┌──────────┐         │
                              │TensorFlow│         │
                              └──────────┘         │
                                                   │
                                   ┌───────────────┘
                                   │
                                   ▼
                            Future Agent / LLM

## Backend

Backend desenvolvido com:

- Node.js
- Express
- Sequelize
- PostgreSQL
- JWT
- Zod
- Helmet
- Rate Limiting
- Swagger

O backend fornece a API principal da aplicação e integra o serviço de Machine Learning.

## Machine Learning

O projeto possui uma pipeline de Machine Learning para estimativa de preço de veículos.

### Pipeline
```text
Raw Data
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
FastAPI
```
### Features utilizadas
- `year`
- `engine_cc`
- `mileage_km`
- `doors`
- `vehicle_age`
- `km_per_year`

- `make`
- `fuel_type`
- `transmission`
- `body_type`
- `state`

### TensorFlow Model

Modelo de regressão desenvolvido com TensorFlow/Keras.

Arquitetura principal:

```text
Input
  ↓
Dense(64, ReLU)
  ↓
Dense(32, ReLU)
  ↓
Dense(1)
```

Treinamento com:

- Adam
- Learning rate: `0.001`
- MSE loss
- MAE metric
- Early Stopping
- Validation split

## SENATRAN Data Engineering

O projeto utiliza dados públicos da SENATRAN para análise da frota brasileira.

### Pipeline

SENATRAN
   ↓
Ingestion
   ↓
Cleaning
   ↓
Classification
   ↓
Aggregation
   ↓
Feature Engineering
   ↓
Analytics
```

### Categorias utilizadas

- `CARRO`
- `MOTO`
- `PESADO`
- `IMPLEMENTO`
- `NAO_CLASSIFICADO`
- `OUTRO`

Também existem pipelines para:

- agregação por UF
- agregação por município
- classificação de veículos
- distribuição da frota
- geração de features
- experimentos de integração com Machine Learning

## ML API

A previsão de preço é disponibilizada através de uma API FastAPI.

Endpoint:

`POST /predict`

Exemplo:

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

## MCP Server

O projeto possui um MCP Server desenvolvido em TypeScript.

O objetivo do MCP é transformar dados e capacidades do sistema em ferramentas estruturadas que possam futuramente ser utilizadas por Agents.

### MCP Resources

Atualmente:

senatran://uf/{uf}

Exemplo:

senatran://uf/PI
### MCP Tools

#### `get_fleet_by_state`

Consulta a frota de veículos de uma UF.

get_fleet_by_state("PI")
#### `compare_states`

Compara a frota de duas UFs.

compare_states("PI", "SP")
#### `get_vehicle_distribution`

Calcula a distribuição percentual da frota.

get_vehicle_distribution("PI")
#### `predict_vehicle_price`

Utiliza o modelo de Machine Learning através da ML API.

predict_vehicle_price(...)

Fluxo:

MCP Client
    ↓
MCP Server
    ↓
predict_vehicle_price
    ↓
FastAPI
    ↓
TensorFlow
    ↓
Prediction
## MCP + Machine Learning

Um dos objetivos arquiteturais do projeto é separar responsabilidades:

```text
MCP
 └── Exposição de capacidades

Analytics
 └── Análise dos dados

ML
 └── Predições

LLM / Agent
 └── Orquestração futura
```

Dessa forma, o modelo de Machine Learning não fica acoplado diretamente ao Agent.

O Agent poderá futuramente decidir quando utilizar:

Vehicle Data
Fleet Analytics
ML Prediction
External Data

através das capacidades expostas pelo MCP.

## Testing

Testes automatizados e scripts de validação estão disponíveis em:

tests/

Exemplo:

pytest
## Running the Project

### Backend
```bash
cd backend
npm install
npm run dev
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### ML API
No ambiente Python configurado:

```bash
uvicorn ai.api.main:app --host 0.0.0.0 --port 8003
```

Health check:

```bash
curl http://localhost:8003/health
```

### MCP Server
```bash
cd backend/mcp

npm install
npm run dev
```

O servidor utiliza STDIO para comunicação MCP.

Para inspeção e testes:

npx @modelcontextprotocol/inspector

## Tech Stack

| Área | Tecnologias |
| --- | --- |
| Backend | Node.js, Express, Sequelize, PostgreSQL, Zod, JWT |
| Frontend | React, Vite |
| Data & ML | Python, Pandas, Scikit-learn, TensorFlow, FastAPI, Joblib |
| AI Integration | Model Context Protocol, TypeScript, MCP Inspector |
| Data Sources | SENATRAN, FIPE, IBGE |


Este projeto é um laboratório de arquitetura para explorar a evolução de uma aplicação tradicional para uma plataforma orientada a dados e inteligência.

O foco não é apenas prever preços.

A proposta é construir uma arquitetura na qual:

Data
 ↓
Analytics
 ↓
Machine Learning
 ↓
MCP
 ↓
LLM
 ↓
Agent

possa ser utilizada de forma modular e evolutiva.

Author: Silas Vasconcelos Cruz

Full Stack Engineer | Enterprise Modernization | DevSecOps | Applied AI
Experimental engineering project focused on Data Engineering, Machine Learning, MCP and Agentic AI architecture.