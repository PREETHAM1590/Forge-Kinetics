import { NextResponse } from "next/server";

type Params = { params: { id: string } };

export async function GET(_: Request, { params }: Params) {
	const project = {
		id: params.id,
		name: "Forge Project",
		status: "in_progress",
		hitlStatus: "pending",
		updatedAt: new Date().toISOString(),
	};

	return NextResponse.json({ project });
}

export async function PATCH(request: Request, { params }: Params) {
	const payload = await request.json().catch(() => ({}));
	return NextResponse.json({
		project: {
			id: params.id,
			...payload,
			updatedAt: new Date().toISOString(),
		},
	});
}

export async function DELETE(_: Request, { params }: Params) {
	return NextResponse.json({ deleted: true, id: params.id });
}
