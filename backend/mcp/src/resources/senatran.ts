import { readFile } from "node:fs/promises";
import { ResourceTemplate } from "@modelcontextprotocol/server";

const DATA_FILE = "../../ai/data/processed/senatran/senatran_uf_2026-07.csv";

const UF_TO_STATE: Record<string, string> = {
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
  TO: "TOCANTINS",
};
export const senatranUfResource = new ResourceTemplate("senatran://uf/{uf}", {
  list: undefined,
});

export async function readSenatranUf(
  uri: URL,
  variables: Record<string, string | string[]>,
) {
  const v = variables.uf;
  const uf = Array.isArray(v) ? v[0]?.toUpperCase() : v?.toUpperCase();

  if (!uf) {
    throw new Error("UF não informada");
  }

  const state = UF_TO_STATE[uf];

  if (!state) {
    throw new Error(`UF inválida: ${uf}`);
  }

  const csv = await readFile(DATA_FILE, "utf-8");

  const lines = csv.trim().split("\n");
  const header = lines[0]?.split(",");

  const row = lines
    .slice(1)
    .map((line) => line.split(","))
    .find((columns) => columns[0] === state);

  if (!row || !header) {
    throw new Error(`UF não encontrada: ${uf}`);
  }

  const data: Record<string, string> = {};

  header.forEach((column, index) => {
    data[column] = row[index] ?? "";
  });

  return {
    contents: [
      {
        uri: uri.href,
        mimeType: "application/json",
        text: JSON.stringify(data),
      },
    ],
  };
}
