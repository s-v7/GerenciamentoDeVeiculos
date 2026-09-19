const { z } = require('zod');

const predictVeiculoSchema = z.object({
  make: z.string({ required_error: "O campo 'make' é obrigatório." }),
  year: z.number({ required_error: "O campo 'year' é obrigatório." })
         .int()
         .min(1900)
         .max(new Date().getFullYear() + 1),
  engine_cc: z.number().positive(),
  mileage_km: z.number().nonnegative(),
  doors: z.number().int().min(2).max(5),
  fuel_type: z.string(),
  transmission: z.string(),
  body_type: z.string(),
  state: z.string().length(2, "O estado deve ter 2 letras (ex: SP)"),
});

const createVeiculoSchema = z.object({
  modelo: z.string({ required_error: "O campo 'modelo' é obrigatório." }),
  marca: z.string({ required_error: "O campo 'marca' é obrigatório." }),
  ano: z.number().int().min(1900),
  placa: z.string().min(7).max(8),
  valor: z.number().positive({ message: "O valor deve ser positivo." }),
});

module.exports = { predictVeiculoSchema, createVeiculoSchema };
