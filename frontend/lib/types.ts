import { z } from "zod";

const MAX_MESSAGE_LENGTH = Number(process.env.NEXT_PUBLIC_MAX_MESSAGE_LENGTH) || 10000;

// Request Schemas
export const ActionSchema = z.enum(["encrypt", "decrypt", "hack"]);

export const EndpointSchema = ActionSchema.transform((action): "encrypt" | "decrypt" => 
  action === "hack" ? "decrypt" : action
);

export const ApiRequestSchema = z.object({
    text: z.string().min(1).max(MAX_MESSAGE_LENGTH),
    key: z.number().int().optional(),
    keepSpaces: z.boolean().default(true),
    keepPunctuation: z.boolean().default(true),
    transformCase: z.enum(["lowercase", "uppercase", "keep_case"]).default("keep_case")
})

// Response Schemas
export const ErrorDetailSchema = z.object({
    code: z.string(),
    message: z.string(),
    errorId: z.string().optional()
});
  
export const MetadataSchema = z.object({
    action: z.enum(["encrypt", "decrypt", "hack"]),
    key: z.number(),
    confidenceLevel: z.enum(["low", "medium", "high"]).nullable(),
    analysisLength: z.number().nullable()
});

export const ApiSolutionSchema = z.object({
    key: z.number(),
    text: z.string(),
    chiSquaredTotal: z.number().optional()
})

export const ApiTextSchema = z.object({
    text: z.string()
})

export const ApiResponseSchema = z.object({
    success: z.boolean(),
    data: z.union([
        z.array(ApiSolutionSchema),
        z.array(ApiTextSchema)
    ]).optional(),
    error: ErrorDetailSchema.nullable(),
    metadata: MetadataSchema.optional()
})

// Form Schema
const emptyTextMsg = `Text cannot be empty`
const tooManyCharactersMsg = `Text cannot exceed ${MAX_MESSAGE_LENGTH} characters`

export const FormSchema = z.discriminatedUnion('action', [
    z.object({
      action: z.literal(ActionSchema.enum.encrypt),
      ...ApiRequestSchema.shape,
      text: z.string()
        .min(1, { message: emptyTextMsg })
        .max(10000, { message: tooManyCharactersMsg }),
      key: z.optional(z.number().int({ message: "Key must be a whole number" }))
    }),
    z.object({
      action: z.literal(ActionSchema.enum.decrypt),
      ...ApiRequestSchema.shape,
      text: z.string()
        .min(1, { message: emptyTextMsg })
        .max(10000, { message: tooManyCharactersMsg }),
      key: z.number().int({ message: "Key is required for decryption" })
    }),
    z.object({
      action: z.literal(ActionSchema.enum.hack),
      ...ApiRequestSchema.shape,
      text: z.string()
        .min(1, { message: emptyTextMsg })
        .max(10000, { message: tooManyCharactersMsg }),
      key: z.undefined({ message: "Hacking ciphertext does not involve a key" })
    })
]);

// Export types
export type Action = z.infer<typeof ActionSchema>;
export type Endpoint = z.infer<typeof EndpointSchema>
export type ApiRequest = z.infer<typeof ApiRequestSchema>
export type ErrorDetail = z.infer<typeof ErrorDetailSchema>
export type Metadata = z.infer<typeof MetadataSchema>
export type ApiSolution = z.infer<typeof ApiSolutionSchema>
export type ApiText = z.infer<typeof ApiTextSchema>
export type ApiResponse = z.infer<typeof ApiResponseSchema>
export type FormData = z.infer<typeof FormSchema>;
