# SKILL: Dashboard Layout — App Shell
> v1.0 | Category: ui | Stack: Next.js 15 + Tailwind + shadcn/ui

## What This Skill Does
Complete responsive app shell: sticky sidebar navigation, top navbar with
breadcrumbs, mobile drawer, user menu, notification bell, dark/light mode toggle.
Wraps all authenticated app pages.

## Prerequisites
- [ ] Next.js 15 App Router + Tailwind
- [ ] `npx shadcn@latest init`
- [ ] Auth set up (user object available in session)

## Steps
1. `npx shadcn@latest add sidebar sheet dropdown-menu avatar badge separator`
2. Create `components/layout/sidebar.tsx` — desktop sidebar with nav links
3. Create `components/layout/navbar.tsx` — top bar: breadcrumb + user menu
4. Create `components/layout/mobile-nav.tsx` — Sheet-based mobile drawer
5. Create `config/nav.ts` — nav items array (title, href, icon)
6. Create `app/(app)/layout.tsx` — wraps all authenticated routes
7. Active route highlighting with `usePathname()` + `startsWith`
8. Responsive: sidebar visible ≥ lg breakpoint, hamburger on mobile
9. User avatar + name + sign out in sidebar footer
10. Notification bell (static badge for now)
11. Test breakpoints: 320px (mobile), 768px (tablet), 1440px (desktop)

## Nav Config Pattern
```typescript
// config/nav.ts
export const navItems = [
  { title: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { title: "Projects",  href: "/projects",  icon: FolderKanban },
  { title: "Settings",  href: "/settings",  icon: Settings },
]
```

## Validation
- [ ] Sidebar shows on desktop with nav items
- [ ] Active route highlighted correctly
- [ ] Mobile: hamburger opens drawer, closes on nav click
- [ ] User name + avatar in sidebar footer
- [ ] No layout shift between page navigations
- [ ] Scrollable content area works with sticky sidebar

## Common Errors & Fixes
| Error | Fix |
|---|---|
| Hydration mismatch on active state | Mark nav component `'use client'` |
| Sidebar not sticky | Add `h-screen sticky top-0` to sidebar container |
| Mobile drawer flicker | Ensure `asChild` prop on Sheet trigger |
| Active check wrong for nested routes | Use `pathname.startsWith(href)` not `pathname === href` |
