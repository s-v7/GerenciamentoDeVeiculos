import { readFile } from "node:fs/promises";
import * as z from "zod/v4";
const DATA_FILE = "../../ai/data/processed/senatran/senatran_uf_2026-07.csv";
const UF_TO_STATE = {
    AC: "ACRE",
    AL: "ALAGOAS",
    AP: "AMAPA",
    AM: "AMAZONAS",
    BA: "BAHIA",
    CE: "CEARA",
    DF: "DISTRITO FEDERAL",
    ES: "ESPIRITO SANTO",
    GO: "GOIAS",
    MA: "MARANHAO",
    MT: "MATO GROSSO",
    MS: "MATO GROSSO DO SUL",
    MG: "MINAS GERAIS",
    PA: "PARA",
    PB: "PARAIBA",
    PR: "PARANA",
    PE: "PERNAMBUCO",
    PI: "PIAUI",
    RJ: "RIO DE JANEIRO",
    RN: "RIO GRANDE DO NORTE",
    RS: "RIO GRANDE DO SUL",
    RO: "RONDONIA",
    RR: "RORAIMA",
    SC: "SANTA CATARINA",
    SP: "SAO PAULO",
    SE: "SERGIPE",
    TO: "TOCANTINS"
};
export const getFleetByStateSchema = z.object({
    uf: z
        .string()
        .length(2)
        .transform((value) => value.toUpperCase())
        .describe("Sigla da unidade federativa, por exemplo PI ou SP")
});
export async function getFleetByState(uf) {
    const state = UF_TO_STATE[uf];
    if (!state) {
        throw new Error(`UF inválida: ${uf}`);
    }
    const csv = await readFile(DATA_FILE, "utf-8");
    const lines = csv.trim().split("\n");
    const header = lines[0]?.split(",");
    if (!header) {
        throw new Error("Cabeçalho do dataset não encontrado");
    }
    const row = lines
        .slice(1)
        .map((line) => line.split(","))
        .find((columns) => columns[0] === state);
    if (!row) {
        throw new Error(`Estado não encontrado no dataset: ${state}`);
    }
    const data = {};
    header.forEach((column, index) => {
        data[column] = row[index] ?? "";
    });
    return data;
}
//# sourceMappingURL=senatran.js.map