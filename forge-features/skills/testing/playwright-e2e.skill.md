# SKILL: Playwright E2E Testing — Full User Flow Tests
> v1.0 | Category: testing | Stack: Next.js + Playwright + E2B sandbox

## What This Skill Does
Full end-to-end test suite covering all critical user flows: auth, core features,
payments, edge cases. Runs inside E2B sandbox. Uses Evaluator-Optimizer pattern —
writes failing tests first, then forces Frontend/Backend agents to fix until all pass.

## Prerequisites
- [ ] App running in E2B sandbox on localhost:3000
- [ ] `npm install -D @playwright/test`
- [ ] `npx playwright install chromium`
- [ ] Test user credentials available

## Steps
1. Create `playwright.config.ts` — baseURL, timeout, retries, reporters
2. Create `tests/auth.spec.ts` — signup, login, logout, password reset
3. Create `tests/core-flow.spec.ts` — primary user journey end-to-end
4. Create `tests/crud.spec.ts` — create, read, update, delete for main resources
5. Create `tests/payments.spec.ts` — checkout flow with Stripe test card
6. Create `tests/responsive.spec.ts` — viewport tests at 375px, 768px, 1440px
7. Create `tests/helpers/auth.ts` — reusable login helper
8. Run: `npx playwright test --reporter=html`
9. Fix failures (Evaluator-Optimizer: Testing Agent sends findings back to build agents)
10. Repeat until ALL tests pass

## Evaluator-Optimizer Pattern
```typescript
// Testing Agent runs this loop (ADK LoopAgent)
for (let i = 0; i < 5; i++) {
  const results = await runPlaywrightTests()
  if (results.failed === 0) break  // all pass → exit loop
  // Send failures back to Frontend/Backend agent to fix
  await notifyBuildAgent(results.failures)
  await waitForFix()  // build agent fixes → re-runs
}
```

## Core Test Pattern
```typescript
// tests/auth.spec.ts
import { test, expect } from '@playwright/test'

test('user can sign up and login', async ({ page }) => {
  await page.goto('/sign-up')
  await page.fill('[name="email"]', 'test@example.com')
  await page.fill('[name="password"]', 'SecurePass123!')
  await page.click('[type="submit"]')
  await expect(page).toHaveURL('/dashboard')
  await expect(page.locator('[data-testid="user-nav"]')).toBeVisible()
})

test('unauthenticated user redirected to login', async ({ page }) => {
  await page.goto('/dashboard')
  await expect(page).toHaveURL('/sign-in')
})
```

## Validation
- [ ] All auth flows pass
- [ ] Core user journey completes without errors
- [ ] CRUD operations verified
- [ ] Payment flow reaches success page
- [ ] No console errors during any test
- [ ] Coverage report generated
- [ ] All tests pass in E2B sandbox

## Common Errors & Fixes
| Error | Fix |
|---|---|
| Flaky tests | Add `await page.waitForLoadState('networkidle')` before assertions |
| Auth state not persisting between tests | Use `storageState` in playwright.config.ts |
| Stripe checkout not loading | Use `page.waitForURL('**/checkout**')` with longer timeout |
| Selector not found | Use `data-testid` attributes, add them to components |
