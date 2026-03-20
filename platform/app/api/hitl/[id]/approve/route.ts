import { NextResponse } from "next/server";

type Params = { params: { id: string } };

export async function POST(request: Request, { params }: Params) {
	const payload = await request.json().catch(() => ({}));
	const approverId =
		typeof payload?.approverId === "string" ? payload.approverId : "unknown-approver";

	return NextResponse.json({
		projectId: params.id,
		hitlStatus: "approved",
		approverId,
		approvedAt: new Date().toISOString(),
		token: `approval_${params.id}_${Date.now()}`,
	});
}
