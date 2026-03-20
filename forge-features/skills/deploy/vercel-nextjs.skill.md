# SKILL: Vercel Deploy — Next.js Production Deployment
> v1.0 | Category: deploy | Stack: Next.js 15 + Vercel + Cloudflare DNS

## What This Skill Does
Production deployment of a Next.js app to Vercel: project setup, environment
variables, custom domain with Cloudflare DNS, preview deployments, and
post-deploy health check. Used by DevOps Agent after HITL approval.

## Prerequisites
- [ ] Vercel account + VERCEL_TOKEN env var
- [ ] Cloudflare account (for custom domain DNS)
- [ ] All environment variables ready
- [ ] HITL approval token (non-negotiable gate)
- [ ] `npm install -g vercel`

## Steps
1. Verify HITL approval token before ANY deployment step
2. Run `vercel link` or use Vercel API to create project
3. Set all environment variables via Vercel API or CLI:
   `vercel env add VARIABLE_NAME production`
4. Run `vercel --prod` for production deploy OR use Vercel API
5. Get deploy URL from Vercel response
6. Add custom domain via Vercel: `vercel domains add yourdomain.com`
7. Configure Cloudflare DNS: add CNAME → `cname.vercel-dns.com`
8. Wait for DNS propagation (check with `dig yourdomain.com`)
9. Verify SSL certificate issued by Vercel
10. Run post-deploy health check: GET `/api/health` → expect 200
11. Run Lighthouse audit on deployed URL
12. Write deploy URL to ForgeState

## Vercel API Deploy (programmatic)
```typescript
const deploy = await fetch('https://api.vercel.com/v13/deployments', {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${process.env.VERCEL_TOKEN}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: projectName,
    gitSource: { type: 'github', repoId, ref: 'main' },
    target: 'production',
  })
})
const { url } = await deploy.json()
```

## Validation
- [ ] HITL approval token verified BEFORE starting
- [ ] `vercel --prod` exits with code 0
- [ ] Deploy URL accessible in browser
- [ ] Custom domain resolves correctly
- [ ] SSL certificate active (no browser warning)
- [ ] `/api/health` returns 200
- [ ] Lighthouse performance ≥80
- [ ] All env vars set (check Vercel dashboard)

## Common Errors & Fixes
| Error | Fix |
|---|---|
| `Error: No token found` | Set VERCEL_TOKEN env var |
| Build fails in Vercel but works locally | Check Node version in `package.json` engines field |
| Custom domain not resolving | DNS TTL — wait up to 24h, or check Cloudflare proxy status |
| Environment variables missing in production | Must set vars for "Production" environment in Vercel |
| Function timeout | Increase `maxDuration` in `vercel.json` (max 60s on Pro) |

## Post-Deploy Checklist
- [ ] Auth flow works on live URL
- [ ] Payments checkout loads
- [ ] Database connections healthy
- [ ] No console errors in browser
- [ ] Mobile responsive at 375px
