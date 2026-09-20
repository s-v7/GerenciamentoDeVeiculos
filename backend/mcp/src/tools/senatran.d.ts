import * as z from "zod/v4";
export declare const getFleetByStateSchema: z.ZodObject<{
    uf: z.ZodPipe<z.ZodString, z.ZodTransform<string, string>>;
}, z.core.$strip>;
export declare function getFleetByState(uf: string): Promise<Record<string, string>>;
//# sourceMappingURL=senatran.d.ts.map