import * as z from "zod/v4";
import { findByState } from "../data/senatranRepository.js";
import { 
  calculateFleetDistribution,
  compareFleet,
  calculateFleetSummary
} from "../analytics/fleetAnalytics.js";

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

function resolveState(uf: string): string {
  const state = UF_TO_STATE[uf.toUpperCase()];

  if (!state) {
    throw new Error(`UF inválida: ${uf}`);
  }

  return state;
}

export const getFleetByStateSchema = z.object({
  uf: z
    .string()
    .length(2)
    .transform((value) => value.toUpperCase())
    .describe("Sigla da unidade federativa, por exemplo PI ou SP"),
});

export const getVehicleDistributionSchema = z.object({
  uf: z
    .string()
    .length(2)
    .transform((value) => value.toUpperCase())
    .describe("Sigla da unidade federativa, por ex: PI ou SP"),
});

export const compareStatesSchema = z.object({
  uf_a: z
    .string()
    .length(2)
    .transform((value) => value.toUpperCase())
    .describe("Primeira UF da comparação"),

  uf_b: z
    .string()
    .length(2)
    .transform((value) => value.toUpperCase())
    .describe("Segunda UF da comparação"),
});

export async function getFleetByState(uf: string) {
  const state = resolveState(uf);
  const data = await findByState(state);

  if (!data) {
    throw new Error(`Estado não encontrado no dataset: ${state}`);
  }
  return calculateFleetSummary(data);
}

export async function compareStates(ufA: string, ufB: string) {
  const stateA = resolveState(ufA);
  const stateB = resolveState(ufB);

  const dataA = await findByState(stateA);
  const dataB = await findByState(stateB);

  if (!dataA) {
    throw new Error(`Estado não encontrado no dataset: ${stateA}`);
  }

  if (!dataB) {
    throw new Error(`Estado não encontrado no dataset: ${stateB}`);
  }
  return compareFleet(dataA, dataB);
}

export async function getVehicleDistribution(uf: string) {
  const state = resolveState(uf);
  const data = await findByState(state);

  if (!data) {
    throw new Error(`Estado não encontrado no dataset: ${state}`);
  }

  return {
    state: data.state,
    total_fleet: data.total_fleet,
    distribution: calculateFleetDistribution(data),
  };
}
