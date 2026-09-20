export interface SenatranUf {
    state: string;
    total_fleet: number;
    CARRO: number;
    MOTO: number;
    PESADO: number;
    IMPLEMENTO: number;
    NAO_CLASSIFICADO: number;
    OUTRO: number;
}
export declare function findByState(state: string): Promise<SenatranUf | null>;
//# sourceMappingURL=senatranRepository.d.ts.map