import type { SenatranUf } from "../data/senatranRepository.js";

export function calculateFleetDistribution(data: SenatranUf) {
  const total = data.total_fleet;

  if (total <= 0) {
    throw new Error(`Frota inválida para o estado: ${data.state}`);
  }

  return {
    CARRO: Number(((data.CARRO / total) * 100).toFixed(2)),
    MOTO: Number(((data.MOTO / total) * 100).toFixed(2)),
    PESADO: Number(((data.PESADO / total) * 100).toFixed(2)),
    IMPLEMENTO: Number(((data.IMPLEMENTO / total) * 100).toFixed(2)),
    NAO_CLASSIFICADO: Number(
      ((data.NAO_CLASSIFICADO / total) * 100).toFixed(2),
    ),
    OUTRO: Number(((data.OUTRO / total) * 100).toFixed(2)),
  };
}

export function compareFleet(
  dataA: SenatranUf,
  dataB: SenatranUf,
) {
  return {
    state_a: dataA.state,
    state_b: dataB.state,

    total_fleet: {
      a: dataA.total_fleet,
      b: dataB.total_fleet,
      difference: dataB.total_fleet - dataA.total_fleet,
    },

    categories: {
      CARRO: {
        a: dataA.CARRO,
        b: dataB.CARRO,
        difference: dataB.CARRO - dataA.CARRO,
      },
      MOTO: {
        a: dataA.MOTO,
        b: dataB.MOTO,
        difference: dataB.MOTO - dataA.MOTO,
      },
      PESADO: {
        a: dataA.PESADO,
        b: dataB.PESADO,
        difference: dataB.PESADO - dataA.PESADO,
      },
      IMPLEMENTO: {
        a: dataA.IMPLEMENTO,
        b: dataB.IMPLEMENTO,
        difference: dataB.IMPLEMENTO - dataA.IMPLEMENTO,
      },
      NAO_CLASSIFICADO: {
        a: dataA.NAO_CLASSIFICADO,
        b: dataB.NAO_CLASSIFICADO,
        difference: dataB.NAO_CLASSIFICADO - dataA.NAO_CLASSIFICADO,
      },
      OUTRO: {
        a: dataA.OUTRO,
        b: dataB.OUTRO,
        difference: dataB.OUTRO - dataA.OUTRO,
      },
    },
  };
}

export function calculateFleetSummary(data: SenatranUf) {
  const distribution = calculateFleetDistribution(data);

  return {
    state: data.state,
    total_fleet: data.total_fleet,
    distribution,
  };
}
