# SKILL: Supabase Auth — Complete Auth Flow
> v1.0 | Category: auth | Stack: Next.js 15 + Supabase | Success rate: seed

## What This Skill Does
Complete auth: signup, email confirmation, login, logout, password reset,
session management (server + client), route protection middleware.

## Prerequisites
- [ ] Next.js 15 App Router project initialized
- [ ] Supabase project created
- [ ] ENV: NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY

## Steps
1. `npm install @supabase/supabase-js @supabase/ssr`
2. Create `lib/supabase/client.ts` — browser client
3. Create `lib/supabase/server.ts` — server client (cookies)
4. Create `middleware.ts` — session refresh on every request
5. Create `app/auth/callback/route.ts` — OAuth + email confirmation handler
6. Create `app/(auth)/login/page.tsx` — login form (email + password)
7. Create `app/(auth)/signup/page.tsx` — signup form
8. Create `app/(auth)/reset-password/page.tsx` — password reset request
9. Create `app/(auth)/layout.tsx` — centered auth layout
10. Add route protection: redirect unauthenticated users from /dashboard → /login
11. Create `components/auth/user-nav.tsx` — user avatar + logout button
12. Test full flow: signup → confirm email → login → dashboard → logout

## Validation
- [ ] `npm run build` — no errors
- [ ] Signup creates user in Supabase Auth dashboard
- [ ] Email confirmation works
- [ ] Login redirects to /dashboard
- [ ] Unauthenticated /dashboard → redirects to /login
- [ ] Logout clears session + redirects to /login
- [ ] Password reset email received

## Common Errors & Fixes
| Error | Fix |
|---|---|
| `AuthSessionMissingError` | Use `createServerClient` from `@supabase/ssr`, not browser client |
| Redirect loop | Check middleware `matcher` — ensure /auth routes are excluded |
| `cookies()` error | Import from `next/headers` |
| Session not persisting | Ensure `middleware.ts` calls `supabase.auth.getUser()` |

## Known Edge Cases
- OAuth (Google/GitHub): add callback URL in Supabase Auth → URL Configuration
- Email confirmation must be enabled in Supabase Auth settings
- Free tier: 4 signups/hour rate limit
