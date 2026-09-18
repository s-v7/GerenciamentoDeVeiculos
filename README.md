## Inteligência Artificial

A camada de IA oferece análise de dados e previsão de preços de veículos por meio de um pipeline de Machine Learning e de uma API FastAPI.

### Visão geral

```text
Dataset → Preparação → Feature Engineering → Modelos ML → Avaliação
                                                     ↓
                                           ML API (FastAPI)
                                                     ↓
                                            Node.js / Express
```

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

### Interpretabilidade

As análises incluem:

- Permutation Importance;
- análise de erros e de erros por faixa de preço;
- comparação entre valores previstos e observados;
- avaliação do comportamento do modelo.

## Dados da SENATRAN

O projeto possui ingestão e análise dos dados públicos da SENATRAN:

```text
SENATRAN → Ingestion → Parsing → Validação → Classificação
                                           ↓
                    Agregação por UF / município → Features → Analytics / ML
```

A classificação utiliza categorias oficiais, como `CARRO`, `MOTO`, `PESADO`, `IMPLEMENTO`, `OUTRO` e `NAO_CLASSIFICADO`.

Os dados brutos, devido ao tamanho, permanecem fora do versionamento do Git.

### Integração com o ML

Foi avaliado se características agregadas da frota estadual poderiam melhorar a previsão individual. Como o dataset de treinamento não possui município, o experimento utiliza apenas contexto estadual.

No dataset sintético, a inclusão dos dados da SENATRAN não produziu melhoria relevante. O experimento foi mantido para validar a arquitetura de dados.

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
