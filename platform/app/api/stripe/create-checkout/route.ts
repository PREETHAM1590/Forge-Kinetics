import { NextResponse } from "next/server";

export async function POST() {
	return NextResponse.json({
		url: "https://checkout.stripe.com/pay/mock-session",
		sessionId: `cs_test_${Date.now()}`,
	});
}
