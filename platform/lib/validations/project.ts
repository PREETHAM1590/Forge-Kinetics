import { z } from "zod";

export const projectStatusSchema = z.enum([
	"queued",
	"in_progress",
	"paused",
	"completed",
	"failed",
]);

export const projectCreateSchema = z.object({
	name: z.string().min(1).max(120),
	description: z.string().max(2000).optional(),
	budgetCredits: z.number().int().positive().max(10_000_000).optional(),
});

export const projectUpdateSchema = z.object({
	name: z.string().min(1).max(120).optional(),
	description: z.string().max(2000).optional(),
	status: projectStatusSchema.optional(),
	hitlStatus: z.enum(["not_started", "pending", "approved", "rejected"]).optional(),
});

export type ProjectCreateInput = z.infer<typeof projectCreateSchema>;
export type ProjectUpdateInput = z.infer<typeof projectUpdateSchema>;
