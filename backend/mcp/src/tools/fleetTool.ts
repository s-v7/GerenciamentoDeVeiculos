import { z } from "zod";

export const fleetInputSchema = {
  uf: z.string().length(2)
};
