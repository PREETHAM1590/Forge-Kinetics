import { NextResponse } from "next/server";

type Params = { params: { id: string } };

export async function POST(request: Request, { params }: Params) {
	const payload = await request.json().catch(() => ({}));
	const reason = typeof payload?.reason === "string" ? payload.reason : "No reason provided";

	return NextResponse.json({
		projectId: params.id,
		hitlStatus: "rejected",
		reason,
		rejectedAt: new Date().toISOString(),
	});
}
