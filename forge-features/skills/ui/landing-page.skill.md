# SKILL: Landing Page — Marketing Homepage
> v1.0 | Category: ui | Stack: Next.js 15 + Tailwind

## What This Skill Does
Complete SaaS landing page: hero, features grid, pricing table, testimonials,
FAQ accordion, CTA sections, footer. Responsive. Dark/light mode. Fast.

## Prerequisites
- [ ] Next.js 15 + Tailwind
- [ ] shadcn/ui initialized
- [ ] Design tokens from Design Agent (or use defaults)

## Steps
1. `npx shadcn@latest add accordion card badge button`
2. Create `app/(marketing)/page.tsx` — landing page route
3. Create `app/(marketing)/layout.tsx` — marketing layout (different from app layout)
4. Build sections in order: Navbar → Hero → Social proof → Features → Pricing → FAQ → CTA → Footer
5. Navbar: logo left, nav links center, CTA button right. Sticky on scroll.
6. Hero: headline + subheadline + 2 CTAs (primary: get started, secondary: demo)
7. Features: 3-column grid, icon + title + description per card
8. Pricing: 3 plan cards, middle card highlighted as "most popular"
9. FAQ: shadcn Accordion component, 6–8 questions
10. Footer: logo + links grid + social icons + copyright
11. Add smooth scroll, subtle animations (Tailwind animate)
12. Test all responsive breakpoints

## Validation
- [ ] All sections render without overflow at 320px, 768px, 1440px
- [ ] CTA buttons link to sign-up page
- [ ] Pricing "Get Started" triggers checkout or sign-up
- [ ] FAQ accordion opens/closes correctly
- [ ] No horizontal scroll on any breakpoint
- [ ] Lighthouse performance ≥90

## Common Errors & Fixes
| Error | Fix |
|---|---|
| Horizontal scroll on mobile | Add `overflow-x-hidden` to body |
| Pricing cards different heights | Use `h-full` on card + `flex flex-col` + `mt-auto` on CTA button |
