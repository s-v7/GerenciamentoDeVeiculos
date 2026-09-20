import * as z from "zod/v4";
export declare const predictVehiclePriceSchema: z.ZodObject<{
    make: z.ZodString;
    year: z.ZodNumber;
    engine_cc: z.ZodNumber;
    mileage_km: z.ZodNumber;
    doors: z.ZodNumber;
    fuel_type: z.ZodString;
    transmission: z.ZodString;
    body_type: z.ZodString;
    state: z.ZodPipe<z.ZodString, z.ZodTransform<string, string>>;
}, z.core.$strip>;
export declare function predictVehiclePrice(input: {
    make: string;
    year: number;
    engine_cc: number;
    mileage_km: number;
    doors: number;
    fuel_type: string;
    transmission: string;
    body_type: string;
    state: string;
}): Promise<{
    predicted_price: any;
    model: any;
}>;
//# sourceMappingURL=vehiclePrice.d.ts.map