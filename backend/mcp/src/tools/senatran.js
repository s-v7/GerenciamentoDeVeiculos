import * as z from "zod/v4";
import { findByState } from "../data/senatranRepository.js";
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
function resolveState(uf) {
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
        .describe("Sigla da unidade federativa, por exemplo PI ou SP")
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
        .describe("Segunda UF da comparação")
});
export async function getFleetByState(uf) {
    const state = resolveState(uf);
    const data = await findByState(state);
    if (!data) {
        throw new Error(`Estado não encontrado no dataset: ${state}`);
    }
    return data;
}
export async function compareStates(ufA, ufB) {
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
    return {
        state_a: dataA.state,
        state_b: dataB.state,
        total_fleet: {
            a: dataA.total_fleet,
            b: dataB.total_fleet,
            difference: dataB.total_fleet - dataA.total_fleet
        },
        categories: {
            CARRO: {
                a: dataA.CARRO,
                b: dataB.CARRO,
                difference: dataB.CARRO - dataA.CARRO
            },
            MOTO: {
                a: dataA.MOTO,
                b: dataB.MOTO,
                difference: dataB.MOTO - dataA.MOTO
            },
            PESADO: {
                a: dataA.PESADO,
                b: dataB.PESADO,
                difference: dataB.PESADO - dataA.PESADO
            },
            IMPLEMENTO: {
                a: dataA.IMPLEMENTO,
                b: dataB.IMPLEMENTO,
                difference: dataB.IMPLEMENTO - dataA.IMPLEMENTO
            },
            NAO_CLASSIFICADO: {
                a: dataA.NAO_CLASSIFICADO,
                b: dataB.NAO_CLASSIFICADO,
                difference: dataB.NAO_CLASSIFICADO - dataA.NAO_CLASSIFICADO
            },
            OUTRO: {
                a: dataA.OUTRO,
                b: dataB.OUTRO,
                difference: dataB.OUTRO - dataA.OUTRO
            }
        }
    };
}
//# sourceMappingURL=senatran.js.map