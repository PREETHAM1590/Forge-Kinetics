# SKILL: Webhook Handler — Secure Inbound Webhooks
> v1.0 | Category: api | Stack: Next.js 15 App Router

## What This Skill Does
Secure webhook endpoint: signature verification, idempotency (no duplicate processing),
event routing, background processing, retry handling. Works for Stripe, GitHub,
Clerk, or any HMAC-signed webhook.

## Prerequisites
- [ ] Webhook provider account + secret key
- [ ] `npm install svix` (for Clerk) OR use built-in crypto for HMAC

## Steps
1. Create `app/api/webhooks/[provider]/route.ts`
2. Get raw body BEFORE parsing: `const rawBody = await req.text()`
3. Verify signature using provider's SDK or manual HMAC
4. Parse event type from verified payload
5. Create event router: `switch (event.type) { case "...": ... }`
6. Add idempotency: check `processed_webhooks` table before processing
7. Process in background if heavy (don't block the 200 response)
8. Return 200 IMMEDIATELY after verification — process async
9. Add `processed_webhooks` table to Supabase (SQL below)
10. Test with provider's webhook replay / CLI tool

## Idempotency Table SQL
```sql
create table processed_webhooks (
  id text primary key,     -- webhook event ID from provider
  provider text not null,
  processed_at timestamptz default now()
);
```

## Webhook Pattern
```typescript
// app/api/webhooks/stripe/route.ts
import Stripe from 'stripe'
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

export async function POST(req: Request) {
  const rawBody = await req.text()  // MUST use text(), not json()
  const signature = req.headers.get('stripe-signature')!

  let event: Stripe.Event
  try {
    event = stripe.webhooks.constructEvent(rawBody, signature, process.env.STRIPE_WEBHOOK_SECRET!)
  } catch (err) {
    return Response.json({ error: 'Invalid signature' }, { status: 400 })
  }

  // Idempotency check
  const supabase = await createClient()
  const { data: existing } = await supabase
    .from('processed_webhooks').select('id').eq('id', event.id).single()
  if (existing) return Response.json({ received: true })  // already processed

  // Mark as processed
  await supabase.from('processed_webhooks').insert({ id: event.id, provider: 'stripe' })

  // Route event (process async to return 200 fast)
  switch (event.type) {
    case 'checkout.session.completed':
      await handleCheckoutComplete(event.data.object as Stripe.Checkout.Session)
      break
    case 'customer.subscription.deleted':
      await handleSubscriptionDeleted(event.data.object as Stripe.Subscription)
      break
  }

  return Response.json({ received: true })
}
```

## Validation
- [ ] Valid signature → 200
- [ ] Invalid signature → 400
- [ ] Duplicate event → 200 (not processed twice)
- [ ] Each event type routes to correct handler
- [ ] 200 returned in <500ms (processing is async)
- [ ] Test with: `stripe listen --forward-to localhost:3000/api/webhooks/stripe`

## Common Errors & Fixes
| Error | Fix |
|---|---|
| Signature mismatch | Using `req.json()` instead of `req.text()` — body already consumed |
| Duplicate processing | Add idempotency table check before processing |
| Timeout on heavy processing | Offload to BullMQ queue, return 200 immediately |
| Wrong webhook secret | Local dev uses `stripe listen` CLI secret, prod uses dashboard secret |
