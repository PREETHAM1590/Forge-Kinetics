# SKILL: Clerk Auth — Drop-in Authentication
> v1.0 | Category: auth | Stack: Next.js 15 + Clerk

## What This Skill Does
Complete auth with Clerk: signup, login, OAuth, MFA, user management dashboard,
organization support. Faster to set up than Supabase Auth. Best for apps that
need social auth or organizations out of the box.

## Prerequisites
- [ ] Next.js 15 App Router project
- [ ] Clerk account + application created
- [ ] ENV: NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY, CLERK_SECRET_KEY,
      NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in, NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up

## Steps
1. `npm install @clerk/nextjs`
2. Wrap `app/layout.tsx` root with `<ClerkProvider>`
3. Create `middleware.ts` — `clerkMiddleware()` with `createRouteMatcher`
4. Create `app/sign-in/[[...sign-in]]/page.tsx` — `<SignIn />` component
5. Create `app/sign-up/[[...sign-up]]/page.tsx` — `<SignUp />` component
6. Add `<UserButton />` to navbar for user menu + logout
7. Use `auth()` in server components, `useAuth()` in client components
8. Set public routes in middleware matcher (marketing pages)
9. Test: signup → login → protected route → user button → sign out

## Validation
- [ ] Sign-up creates user in Clerk dashboard
- [ ] Google OAuth works (if configured)
- [ ] Protected routes redirect to /sign-in when unauthenticated
- [ ] `<UserButton />` shows avatar + dropdown
- [ ] `auth().userId` returns user ID in server components

## Common Errors & Fixes
| Error | Fix |
|---|---|
| `auth() was called but Clerk can't detect the middleware` | Ensure middleware.ts is at root, not in /app |
| Redirect loop | Add sign-in/sign-up URLs to `isPublicRoute` in middleware |
| `useAuth` in server component | Use `auth()` from `@clerk/nextjs/server` instead |

## When to use Clerk vs Supabase Auth
- Use Clerk: need OAuth + org support quickly, don't need RLS on auth
- Use Supabase Auth: need deep Supabase RLS integration, lower cost at scale
