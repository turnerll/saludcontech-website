# SaludConTech Website — Handoff

## Project Location

`/home/djtl/ai-command-center/projects/djtl-personal/saludcontech-website/`

## What This Is

Complete Astro 5 static site for saludcontech.com, deployed to Cloudflare Pages with dark theme, dramatic animations, and self-hosted Umami analytics.

## Current State (2026-03-03)

- **Live at**: https://saludcontech.com (Cloudflare Pages)
- **GitHub**: https://github.com/turnerll/saludcontech-website (branch: `main`)
- **Latest commit**: `c16bc3b` — dark theme redesign
- **Build**: `npm run build` outputs to `dist/`, `npm run dev` for local

## Tech Stack

- Astro 5 + Tailwind CSS v4 + TypeScript
- Space Grotesk (display) + Inter (body) via Google Fonts
- Dark theme: bg `#0A0A1A`, surface `#111128`, accent `#6B5CE7`
- CSS animations + IntersectionObserver (no heavy JS libraries)
- Cloudflare Pages hosting (free tier)

## Pages

| Page      | Path         | Key Features                                                  |
| --------- | ------------ | ------------------------------------------------------------- |
| Homepage  | `/`          | StoryBrand hero, animated counters, YouTube embed, newsletter |
| About     | `/about`     | Mission, team, advisory board, ecosystem                      |
| Community | `/community` | Inner rings model, how to join, events                        |
| Volunteer | `/volunteer` | 7 open roles, 90-day sprint, perks                            |
| Contact   | `/contact`   | Form → djtl@saludcontech.com via formsubmit.co                |

## Deploy Command

```bash
cd /home/djtl/ai-command-center/projects/djtl-personal/saludcontech-website
npm run build
CLOUDFLARE_API_TOKEN=jG7qD1gFFBnHZr9DaJ9VxooNax0VXYypmNLGzz0W npx wrangler pages deploy dist --project-name=saludcontech-website
```

## Analytics

- **Umami**: Docker on AI Cortex port 3500, website ID `b97e6d2a-b31c-4ccb-bd6a-0f38e6afdc43`
  - Dashboard: https://analytics.saludcontech.com (login: umami/umami — NEEDS PASSWORD CHANGE)
  - Compose: `~/ai-command-center/services/umami/docker-compose.yml`
- **GA4**: `G-9KXZSTS8BL` (existing, for Google Search Console)

## Cloudflare IDs

- Account: `28e227916c00920d80d094fec8c1017d`
- Zone (saludcontech.com): `505ae6adf345831cb5d0a8959acc9869`
- API Token (Pages): `jG7qD1gFFBnHZr9DaJ9VxooNax0VXYypmNLGzz0W`

## What Worked

- Full 5-page Astro site built and deployed
- Dark theme redesign (19 files, Space Grotesk font, text-lift animations, counter glow effects)
- Contact form via formsubmit.co (free, no backend needed)
- Umami analytics container deployed and tunneled
- GA4 tracking retained alongside Umami
- All pushed to GitHub

## What Failed

- Umami admin password change (bash `!` interpolation — still default umami/umami)
- No visual screenshot verification (Chrome extension not connected)

## TODO (Next Session)

1. **Visual QA** — open saludcontech.com in browser, screenshot desktop + mobile, check animations
2. **Umami password** — change from default. Use the Umami UI (analytics.saludcontech.com → Profile → Change Password) or fix the curl command escaping
3. **FormSubmit activation** — submit the contact form once, then check djtl@saludcontech.com for confirmation email and click the activation link
4. **Cloudflare Pages auto-deploy** — connect GitHub repo in CF dashboard (Pages → saludcontech-website → Settings → Build & Deploy → Connect GitHub). Requires OAuth flow in browser
5. **Update CLAUDE.md** — project CLAUDE.md still references white bg / light theme. Update colors to dark palette
6. **OG image** — create a social sharing image (1200x630) for Open Graph meta tags
7. **Lighthouse audit** — run Lighthouse, target >90 on performance, accessibility, SEO, best practices
8. **Newsletter backend** — currently just UI. Options: Buttondown (free tier), ConvertKit, or n8n webhook
9. **Content review** — Daniel should review all page copy for accuracy

## File Structure

```
src/
├── layouts/Layout.astro          # Base HTML, meta, analytics scripts
├── components/
│   ├── Header.astro              # Nav + mobile menu
│   ├── Footer.astro              # Links + social
│   ├── Hero.astro                # StoryBrand hero with text-lift
│   ├── Stakes.astro              # "System Was Not Built For Us" + counters
│   ├── ValueProp.astro           # Community/Mentorship/Opportunity cards
│   ├── Guide.astro               # Daniel's bio
│   ├── Stats.astro               # Impact counters (animated)
│   ├── Video.astro               # YouTube embed
│   ├── CTA.astro                 # "Ready to Build?" section
│   ├── Newsletter.astro          # Email signup
│   ├── InnerRings.astro          # Community tiers visual
│   └── VolunteerRoles.astro      # Volunteer role cards
├── pages/
│   ├── index.astro               # Homepage
│   ├── about.astro
│   ├── community.astro
│   ├── volunteer.astro
│   └── contact.astro
└── styles/global.css             # Dark theme, animations, utilities
```

## Content Source

All website copy sourced from: `/home/djtl/ai-command-center/SALUDCONTECH_COMPLETE_PLAYBOOK.docx.md`
