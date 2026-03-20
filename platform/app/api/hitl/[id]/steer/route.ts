import { NextResponse } from "next/server";

type Params = { params: { id: string } };

export async function POST(request: Request, { params }: Params) {
	const payload = await request.json().catch(() => ({}));
	const instructions =
		typeof payload?.instructions === "string"
			? payload.instructions
			: "No steering instructions provided";

	return NextResponse.json({
		projectId: params.id,
		action: "steer",
		instructions,
		status: "queued",
		queuedAt: new Date().toISOString(),
	});
}
