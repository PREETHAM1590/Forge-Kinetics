import Stripe from "stripe";

export function getStripeClient() {
	const secretKey = process.env.STRIPE_SECRET_KEY ?? "";
	return new Stripe(secretKey);
}
