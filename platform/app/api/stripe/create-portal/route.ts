import { NextResponse } from "next/server";

export async function POST() {
	return NextResponse.json({
		url: "https://billing.stripe.com/p/session/mock-portal",
	});
}
