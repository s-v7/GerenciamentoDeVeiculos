import { McpServer } from "@modelcontextprotocol/server";
import { serveStdio } from "@modelcontextprotocol/server/stdio";
import { senatranUfResource, readSenatranUf } from "./resources/senatran.js";
import * as z from "zod/v4";
import {
  compareStates,
  compareStatesSchema,
  getFleetByState,
  getFleetByStateSchema,
  getVehicleDistribution,
  getVehicleDistributionSchema,
} from "./tools/senatran.js";
import { 
  predictVehiclePrice,
  predictVehiclePriceSchema
} from "./tools/vehiclePrice.js";


function createServer() {
  const server = new McpServer({
    name: "vehicle-mcp-server",
    version: "1.0.0",
  });

  server.registerResource(
    "senatran-uf",
    senatranUfResource,
    {
      title: "SENATRAN — Frota por UF",
      description:
        "Dados da frota de veículos da SENATRAN por unidade federativa.",
      mimeType: "application/json",
    },
    readSenatranUf,
  );

  server.registerTool(
    "get_fleet_by_state",
    {
      title: "Frota por UF",
      description:
        "Consulta a frota de veículos da SENATRAN por unidade federativa.",
      inputSchema: getFleetByStateSchema,
    },
    async ({ uf }) => {
      try {
        const data = await getFleetByState(uf);

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(data),
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text",
              text:
                error instanceof Error
                  ? error.message
                  : "Erro ao consultar a frota.",
            },
          ],
          isError: true,
        };
      }
    },
  );

  server.registerTool(
    "compare_states",
    {
      title: "Comparar frotas estaduais",
      description:
        "Compara a frota de veículos da SENATRAN entre duas unidades federativas.",
      inputSchema: compareStatesSchema,
    },
    async ({ uf_a, uf_b }) => {
      try {
        const data = await compareStates(uf_a, uf_b);

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(data),
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text",
              text:
                error instanceof Error
                  ? error.message
                  : "Erro ao comparar as frotas.",
            },
          ],
          isError: true,
        };
      }
    },
  );

  server.registerTool(
    "get_vehicle_distribution",
    {
      title: "Distribuição da frota por categoria",
      description:
        "Calcula a distribuição percentual da frota de veículos da SENATRAN por categoria para uma unidade federativa.",
      inputSchema: getVehicleDistributionSchema,
    },
    async ({ uf }) => {
      try {
        const data = await getVehicleDistribution(uf);

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(data),
            },
          ],
        };
      } catch (error) {
        return {
          content: [
            {
              type: "text",
              text:
                error instanceof Error
                  ? error.message
                  : "Erro ao calcular a distribuição da frota.",
            },
          ],
          isError: true,
        };
      }
    },
  );

  server.registerTool(
    "predict_vehicle_price",
    {
      title: "Prever o preço do veículo",
      description:
	"Estima o preço de um veículo utilizando o modelo de Machine Learning.",
      inputSchema: predictVehiclePriceSchema
    },
    async (input) => {
      try {
	const data = await predictVehiclePrice(input);

	return {
	  content: [
	    {
	      type: "text",
	      text: JSON.stringify(data)
	    }
	  ]
	};
      } catch (error) {
        return {
	  content: [
	    {
	      type: "text",
	      text: error instanceof Error ? error.message : "Erro ao prever o preço do veículo."
	    }
	  ],
	  isError: true
	};
      }
    }
  );

  return server;
}

serveStdio(createServer);
