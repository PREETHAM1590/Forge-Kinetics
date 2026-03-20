# SKILL: REST CRUD API — Next.js Route Handlers + Supabase
> v1.0 | Category: api | Stack: Next.js 15 App Router + Supabase

## What This Skill Does
Complete REST CRUD API using Next.js Route Handlers + Supabase.
Auth guards, Zod input validation, consistent error format, RLS-safe.
Pattern reusable for any resource (posts, products, users, etc.)

## Prerequisites
- [ ] Supabase table exists with RLS enabled
- [ ] Auth set up (Supabase or Clerk)
- [ ] `npm install zod`

## Steps
1. Create `lib/validations/[resource].ts` — Zod schemas
2. Create `app/api/[resource]/route.ts` — GET (list) + POST (create)
3. Create `app/api/[resource]/[id]/route.ts` — GET + PUT + DELETE
4. Add auth guard at top of EVERY handler
5. Add Zod validation before any DB write
6. Return consistent error shape: `{ error: string, code: string }`
7. Add pagination to list endpoint (limit + offset query params)
8. Test all 5 endpoints with valid + invalid inputs

## Route Pattern
```typescript
// app/api/posts/route.ts
export async function GET(req: Request) {
  const supabase = await createClient()
  const { userId } = await auth()
  if (!userId) return Response.json({ error: 'Unauthorized' }, { status: 401 })
  const { searchParams } = new URL(req.url)
  const limit = Number(searchParams.get('limit') ?? 20)
  const offset = Number(searchParams.get('offset') ?? 0)
  const { data, error } = await supabase
    .from('posts').select('*').range(offset, offset + limit - 1)
  if (error) return Response.json({ error: error.message }, { status: 500 })
  return Response.json(data)
}

export async function POST(req: Request) {
  const { userId } = await auth()
  if (!userId) return Response.json({ error: 'Unauthorized' }, { status: 401 })
  const body = await req.json()
  const parsed = createPostSchema.safeParse(body)
  if (!parsed.success) return Response.json({ error: parsed.error }, { status: 400 })
  const supabase = await createClient()
  const { data, error } = await supabase.from('posts')
    .insert({ ...parsed.data, user_id: userId }).select().single()
  if (error) return Response.json({ error: error.message }, { status: 500 })
  return Response.json(data, { status: 201 })
}
```

## Validation
- [ ] GET returns paginated list
- [ ] POST creates + returns 201
- [ ] PUT updates + returns updated record
- [ ] DELETE removes + returns 204
- [ ] Unauthenticated → 401
- [ ] Invalid input → 400 with Zod error details
- [ ] RLS prevents cross-user data access

## Common Errors & Fixes
| Error | Fix |
|---|---|
| RLS violation on insert | Ensure `user_id: userId` is passed in insert body |
| `cookies()` in route handler | Use `createServerClient` with `cookies()` from `next/headers` |
| Zod error not readable | Use `parsed.error.flatten()` for cleaner error output |
