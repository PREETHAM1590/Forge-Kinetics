import { NextResponse } from "next/server";

const sampleProjects = [
	{
		id: "proj_hyperlane",
		name: "Hyperlane Commerce",
		status: "in_progress",
		hitlStatus: "not_started",
		updatedAt: new Date().toISOString(),
	},
	{
		id: "proj_nova",
		name: "Nova CRM Portal",
		status: "paused",
		hitlStatus: "pending",
		updatedAt: new Date().toISOString(),
	},
];

export async function GET() {
	return NextResponse.json({ projects: sampleProjects });
}

export async function POST(request: Request) {
	const payload = await request.json().catch(() => ({}));
	const project = {
		id: `proj_${Date.now()}`,
		name: typeof payload?.name === "string" ? payload.name : "Untitled Project",
		status: "queued",
		hitlStatus: "not_started",
		createdAt: new Date().toISOString(),
	};

	return NextResponse.json({ project }, { status: 201 });
}
