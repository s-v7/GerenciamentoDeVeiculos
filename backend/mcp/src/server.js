import { McpServer } from "@modelcontextprotocol/server";
import { serveStdio } from "@modelcontextprotocol/server/stdio";
import { senatranUfResource, readSenatranUf } from "./resources/senatran.js";
import * as z from "zod/v4";
import { compareStates, compareStatesSchema, getFleetByState, getFleetByStateSchema, } from "./tools/senatran.js";
function createServer() {
    const server = new McpServer({
        name: "vehicle-mcp-server",
        version: "1.0.0",
    });
    server.registerResource("senatran-uf", senatranUfResource, {
        title: "SENATRAN — Frota por UF",
        description: "Dados da frota de veículos da SENATRAN por unidade federativa.",
        mimeType: "application/json",
    }, readSenatranUf);
    server.registerTool("get_fleet_by_state", {
        title: "Frota por UF",
        description: "Consulta a frota de veículos da SENATRAN por unidade federativa.",
        inputSchema: getFleetByStateSchema,
    }, async ({ uf }) => {
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
        }
        catch (error) {
            return {
                content: [
                    {
                        type: "text",
                        text: error instanceof Error
                            ? error.message
                            : "Erro ao consultar a frota.",
                    },
                ],
                isError: true,
            };
        }
    });
    server.registerTool("compare_states", {
        title: "Comparar frotas estaduais",
        description: "Compara a frota de veículos da SENATRAN entre duas unidades federativas.",
        inputSchema: compareStatesSchema,
    }, async ({ uf_a, uf_b }) => {
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
        }
        catch (error) {
            return {
                content: [
                    {
                        type: "text",
                        text: error instanceof Error
                            ? error.message
                            : "Erro ao comparar as frotas.",
                    },
                ],
                isError: true,
            };
        }
    });
    return server;
}
serveStdio(createServer);
//# sourceMappingURL=server.js.map