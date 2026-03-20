import { z } from "zod";

export const hitlDecisionSchema = z.object({
	projectId: z.string().min(1),
	approverId: z.string().min(1),
	decision: z.enum(["approved", "rejected"]),
	reason: z.string().max(2000).optional(),
});

export const hitlSteerSchema = z.object({
	projectId: z.string().min(1),
	instructions: z.string().min(1).max(4000),
});

export type HitlDecisionInput = z.infer<typeof hitlDecisionSchema>;
export type HitlSteerInput = z.infer<typeof hitlSteerSchema>;
