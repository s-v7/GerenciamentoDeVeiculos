import * as z from "zod/v4";
export declare const getFleetByStateSchema: z.ZodObject<{
    uf: z.ZodPipe<z.ZodString, z.ZodTransform<string, string>>;
}, z.core.$strip>;
export declare const getVehicleDistributionSchema: z.ZodObject<{
    uf: z.ZodPipe<z.ZodString, z.ZodTransform<string, string>>;
}, z.core.$strip>;
export declare const compareStatesSchema: z.ZodObject<{
    uf_a: z.ZodPipe<z.ZodString, z.ZodTransform<string, string>>;
    uf_b: z.ZodPipe<z.ZodString, z.ZodTransform<string, string>>;
}, z.core.$strip>;
export declare function getFleetByState(uf: string): Promise<import("../data/senatranRepository.js").SenatranUf>;
export declare function compareStates(ufA: string, ufB: string): Promise<{
    state_a: string;
    state_b: string;
    total_fleet: {
        a: number;
        b: number;
        difference: number;
    };
    categories: {
        CARRO: {
            a: number;
            b: number;
            difference: number;
        };
        MOTO: {
            a: number;
            b: number;
            difference: number;
        };
        PESADO: {
            a: number;
            b: number;
            difference: number;
        };
        IMPLEMENTO: {
            a: number;
            b: number;
            difference: number;
        };
        NAO_CLASSIFICADO: {
            a: number;
            b: number;
            difference: number;
        };
        OUTRO: {
            a: number;
            b: number;
            difference: number;
        };
    };
}>;
export declare function getVehicleDistribution(uf: string): Promise<{
    state: string;
    total_fleet: number;
    distribution: {
        CARRO: number;
        MOTO: number;
        PESADO: number;
        IMPLEMENTO: number;
        NAO_CLASSIFICADO: number;
        OUTRO: number;
    };
}>;
//# sourceMappingURL=senatran.d.ts.map