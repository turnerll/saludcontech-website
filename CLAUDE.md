# SaludConTech Website

## Stack

- Astro 5 (static site generator)
- Tailwind CSS v4
- TypeScript
- Cloudflare Pages (hosting)

## Design

- Colors: primary `#6B5CE7`, text `#1A1A2E`, bg `#FFFFFF`
- Font: Inter (Google Fonts)
- Style: Clean, modern, professional, mobile-first
- Animations: CSS + Intersection Observer (no heavy libraries)

## Content Source

All copy from: `SALUDCONTECH_COMPLETE_PLAYBOOK.docx.md` (repo root)

## Analytics

- Umami (self-hosted): analytics.saludcontech.com
- GA4: G-9KXZSTS8BL (existing, keep for Search Console)

## Deploy

```bash
npm run build   # Outputs to dist/
npm run dev     # Local dev server
```

Cloudflare Pages auto-deploys from GitHub on push.

## Pages

/ (homepage), /about, /community, /volunteer, /contact

## Standing Rules & Gotchas

- **Canonical project folder:** `/home/djtl/Projects/saludcontech-website`. Do not write SaludConTech code into `/home/djtl/Projects/ligazon` or the old `/home/djtl/Projects/saludcontech-site`.
- **Cloudflare Pages project name:** `saludcontech-relaunch` (the repo is `turnerll/saludcontech-website`, but the Pages project predates the repo rename).
- **PostHog:** first-party via `/ingest` proxy (`functions/ingest/[[path]].js`). Client config lives in `src/layouts/Layout.astro`. Dashboard-side setup (session recording toggle, funnel, alert) is done manually in the PostHog UI.
- **Supabase signup:** `src/components/Newsletter.astro` posts to `public.signups` in project `jcxagmhvwakkxogfyrzv`. The anon key and URL are public-safe and checked in.
- **Secrets discipline:** Cloudflare API tokens, service-role keys, and `phx_` keys live in `~/pai/secrets/` only. Never commit them. The old public `HANDOFF.md` exposed a Pages token; it has been redacted and must be rotated via the Cloudflare dashboard.
- **No real names in git.** Slack-derived research goes into `docs/` as paraphrased insights.
- **House voice:** no em dashes, never "health equity" / "DEI" / "Latinx" / "race" in our labels, never "unskilled/low-skilled". Lead with the stake, plainspoken and certain.
- **Model/session trap:** `occ` / `opencode --continue` locks the previous session model. After changing `~/.config/opencode/opencode.json`, start a fresh `opencode` session to load the new model.
