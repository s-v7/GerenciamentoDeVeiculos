import { readFile } from "node:fs/promises";
const DATA_FILE = "../../ai/data/processed/senatran/senatran_uf_2026-07.csv";
export async function findByState(state) {
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
        return null;
    }
    return {
        state: row[0] ?? "",
        total_fleet: Number(row[1] ?? 0),
        CARRO: Number(row[2] ?? 0),
        MOTO: Number(row[3] ?? 0),
        PESADO: Number(row[4] ?? 0),
        IMPLEMENTO: Number(row[5] ?? 0),
        NAO_CLASSIFICADO: Number(row[6] ?? 0),
        OUTRO: Number(row[7] ?? 0)
    };
}
//# sourceMappingURL=senatranRepository.js.map