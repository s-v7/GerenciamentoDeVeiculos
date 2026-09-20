import { McpServer } from "@modelcontextprotocol/server";
import { serveStdio } from "@modelcontextprotocol/server/stdio";
import { senatranUfResource, readSenatranUf } from "./resources/senatran.js";
function createServer() {
    const server = new McpServer({
        name: "vehicle-mcp-server",
        version: "1.0.0"
    });
    server.registerResource("senatran-uf", senatranUfResource, {
        title: "SENATRAN — Frota por UF",
        description: "Dados da frota de veículos da SENATRAN por unidade federativa.",
        mimeType: "application/json"
    }, readSenatranUf);
    return server;
}
serveStdio(createServer);
//# sourceMappingURL=server.js.map