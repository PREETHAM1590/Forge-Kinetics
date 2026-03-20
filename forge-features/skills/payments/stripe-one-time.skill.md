# SKILL: Stripe One-Time Payments
> v1.0 | Category: payments | Stack: Next.js 15 + Supabase + Stripe

## What This Skill Does
One-time payment checkout (not subscriptions): product purchase, payment confirmation,
order record in Supabase, email receipt via Stripe, webhook fulfillment.

## Prerequisites
- [ ] Stripe account with Products created (or use dynamic price)
- [ ] ENV: STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY

## Steps
1. `npm install stripe`
2. Create `lib/stripe.ts`
3. Create `orders` table in Supabase (SQL in resources)
4. Create `app/api/stripe/checkout/route.ts` — mode: "payment"
5. Create `app/api/webhooks/stripe/route.ts` — handle `payment_intent.succeeded`
6. Create `app/(app)/checkout/success/page.tsx` — success page
7. Create `app/(app)/checkout/cancel/page.tsx` — cancel/back page
8. On `payment_intent.succeeded` → create order record in Supabase
9. Test: click buy → Stripe checkout → webhook → order in DB → success page

## Validation
- [ ] Checkout session created with `mode: "payment"`
- [ ] Redirect to Stripe hosted checkout page
- [ ] Webhook fires on successful payment
- [ ] Order created in Supabase after payment
- [ ] Success page shows confirmation

## Common Errors & Fixes
| Error | Fix |
|---|---|
| Using subscription webhook events | Use `payment_intent.succeeded` not `checkout.session.completed` for one-time |
| Order created before payment confirmed | Only create order in webhook, not in success page |
