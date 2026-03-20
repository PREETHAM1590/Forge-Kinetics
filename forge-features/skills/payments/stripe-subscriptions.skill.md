# SKILL: Stripe Subscriptions — Recurring Billing
> v1.0 | Category: payments | Stack: Next.js 15 + Supabase + Stripe

## What This Skill Does
Complete recurring billing: pricing page, checkout session, webhook sync,
subscription management (upgrade/downgrade/cancel), billing portal,
Supabase subscriptions table synced with Stripe.

## Prerequisites
- [ ] Supabase auth set up (supabase-auth.skill.md first)
- [ ] Stripe account with Products + Prices created
- [ ] ENV: STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY

## Steps
1. `npm install stripe @stripe/stripe-js`
2. Create `lib/stripe.ts` — server Stripe client
3. Run Supabase migration (SQL in Resources section)
4. Create `app/api/stripe/create-checkout/route.ts`
5. Create `app/api/stripe/create-portal/route.ts`
6. Create `app/api/webhooks/stripe/route.ts` — handle all lifecycle events
7. Handle: `checkout.session.completed`, `customer.subscription.updated`,
   `customer.subscription.deleted`, `invoice.payment_failed`
8. Create `app/(app)/pricing/page.tsx` — plan cards with checkout CTA
9. Create `app/(app)/billing/page.tsx` — current plan + portal link
10. Add subscription guard to middleware (block `past_due` users)
11. Test: checkout → webhook fires → Supabase row created → portal → cancel

## Supabase Migration SQL
```sql
create table subscriptions (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references auth.users not null,
  stripe_customer_id text unique,
  stripe_subscription_id text unique,
  stripe_price_id text,
  status text,
  current_period_end timestamptz,
  cancel_at_period_end boolean default false,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
alter table subscriptions enable row level security;
create policy "Users view own sub" on subscriptions for select using (auth.uid() = user_id);
```

## Validation
- [ ] Checkout creates Stripe session with correct price
- [ ] Webhook receives `checkout.session.completed`
- [ ] Supabase `subscriptions` row created post-checkout
- [ ] Billing portal opens + shows current plan
- [ ] Cancel updates `cancel_at_period_end = true`
- [ ] `invoice.payment_failed` → status = `past_due`
- [ ] `past_due` users blocked by middleware

## Common Errors & Fixes
| Error | Fix |
|---|---|
| Webhook 400 signature mismatch | Use CLI secret for local dev, dashboard secret for prod |
| `raw body` error | Use `request.text()` not `request.json()` in webhook route |
| Customer not found | Create Stripe customer before checkout if not exists |
| Status not updating | Handle ALL subscription lifecycle webhook events |

## Known Edge Cases
- `cancel_at_period_end = true` ≠ cancelled — still active until period end
- Test card: 4242 4242 4242 4242, any future date, any CVC
- Webhook must be re-registered after deploying to new URL
