import * as z from "zod/v4";
const ML_API_URL = process.env.ML_API_URL ?? "http://localhost:8003";
export const predictVehiclePriceSchema = z.object({
    make: z.string().min(1),
    year: z.number().int(),
    engine_cc: z.number().positive(),
    mileage_km: z.number().nonnegative(),
    doors: z.number().int().positive(),
    fuel_type: z.string().min(1),
    transmission: z.string().min(1),
    body_type: z.string().min(1),
    state: z.string().length(2).transform((value) => value.toUpperCase())
});
export async function predictVehiclePrice(input) {
    const rs = await fetch(`${ML_API_URL}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(input)
    });
    if (!rs.ok) {
        const body = await rs.text();
        throw new Error(`ML API retornou HTTP ${rs.status}: ${body}`);
    }
    const data = await rs.json();
    return {
        predicted_price: data.predicted_price,
        model: data.model
    };
}
//# sourceMappingURL=vehiclePrice.js.map