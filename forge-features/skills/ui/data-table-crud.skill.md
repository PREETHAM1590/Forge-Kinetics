# SKILL: Data Table with CRUD Operations
> v1.0 | Category: ui | Stack: Next.js 15 + Supabase + Tailwind + shadcn

## What This Skill Does
Full data table: sortable columns, search/filter, pagination, row actions
(view/edit/delete), create new record modal, inline editing. Connected to Supabase.

## Prerequisites
- [ ] Supabase table exists with data
- [ ] Auth set up (data is user-scoped via RLS)
- [ ] `npm install @tanstack/react-table`
- [ ] `npx shadcn@latest add table dialog dropdown-menu input`

## Steps
1. Create `components/data-table/columns.tsx` — column definitions with TanStack
2. Create `components/data-table/data-table.tsx` — table component with sort + filter
3. Create `components/data-table/toolbar.tsx` — search input + filter dropdowns
4. Create `components/data-table/pagination.tsx` — prev/next + page size selector
5. Create `components/data-table/row-actions.tsx` — dropdown: view, edit, delete
6. Create `components/modals/create-record-modal.tsx` — shadcn Dialog + form
7. Create `components/modals/edit-record-modal.tsx`
8. Create `app/api/[resource]/route.ts` — GET (list), POST (create)
9. Create `app/api/[resource]/[id]/route.ts` — PUT (update), DELETE
10. Add optimistic updates — update local state before API confirms
11. Add loading states and error toasts

## Validation
- [ ] Table renders all rows from Supabase
- [ ] Search filters rows client-side
- [ ] Click column header → sorts ascending/descending
- [ ] Create modal → form → submit → new row appears
- [ ] Edit modal → pre-filled form → submit → row updates
- [ ] Delete → confirmation → row removed
- [ ] Pagination works at various page sizes
