# SaludConTech Website — Rolling Handoff

## READ THIS FIRST — 2026-08-11

**The full lossless state is in `HANDOFF-2026-08-11.md`. Read that first.**
**Strategy/research reference:** `docs/SCT-STRATEGY-CONTEXT.md`.

**One-line next step:** add the Cloudflare DNS CNAME for `saludcontech.com` on the Mac Mini, verify the live domain serves the new build, test a signup + PostHog event, then capture the COMPA PostHog config from the Mac Mini browser and replicate it in the Ligazon/SCT PostHog project.

## Current state (snapshot, updated 2026-08-11 PM)

- **Canonical folder:** `/home/djtl/Projects/saludcontech-website`
- **Repo:** `https://github.com/turnerll/saludcontech-website` (public)
- **Domain:** `saludcontech.com` — **LIVE with the new build.** DNS CNAME `@` → `saludcontech-relaunch.pages.dev` (proxied) added 2026-08-11; old apex A record (185.73.8.100) deleted. Old 2019 page only persists in expiring edge cache.
- **Commit at time of writing:** `6491648` (run `git log --oneline -1` for absolute latest)
- **Build:** `source ~/.nvm/nvm.sh && nvm use 22 && npm run build` → `dist/`
- **CSP fix (ed0c0dd):** `public/_headers` now allows Supabase in connect-src plus umami/cloudflareinsights in script-src. Before this, signups were silently blocked by CSP.
- **Signup verified end-to-end 2026-08-11:** real-Chrome submit → Supabase `public.signups` row (`source=saludcontech.com`) + PostHog `relaunch_signup` event with GeoIP (Los Angeles). 
- **PostHog client:** wired via `/ingest` proxy in `functions/ingest/[[path]].js`, key in `src/layouts/Layout.astro`. Project `464719`.
- **PostHog dashboard-side setup: DONE via API.** Session replay ON, autocapture ON (COMPA runs ON — the earlier guess was wrong), dashboard "SaludConTech" (id 1986725) with signup trend/funnel/top pages/referrers/devices, weekly email subscription to turnerlloveras@alumni.usc.edu. Signup alert NOT created (API rejected condition schemas; 30-second manual step, see docs/posthog-compa-config.md).
- **COMPA PostHog capture:** `docs/posthog-compa-config.md` (config + replication record).
- **Strategy doc:** `docs/SCT-STRATEGY-CONTEXT.md`

## Immediate next steps

1. ~~DNS CNAME~~ DONE. ~~Signup + PostHog test~~ DONE. ~~COMPA capture + replicate~~ DONE.
2. Rotate the exposed Cloudflare API token (ID `35511cd6f8974a30ef14bc9196e5d023`) via Cloudflare dashboard — still pending, was held to avoid breaking a parallel session.
3. Optional: create the signup alert in the PostHog UI (insight 10951978 → New alert).
4. Replace hardcoded stats in `src/components/Stats.astro` with sourced facts from `data/facts.json`; add `scripts/verify-astro.cjs` + CI; membership/pricing pages (see HANDOFF-2026-08-11.md "NOT started").

## Rules

- All SCT work stays in this folder. Do not write to `/home/djtl/Projects/ligazon` or `/home/djtl/Projects/saludcontech-site`.
- Cloudflare Pages project name is `saludcontech-relaunch`, not `saludcontech-website`.
- Start next session with fresh `opencode` (not `occ`) to load k3.
- No real names in git.
- See `CLAUDE.md` for permanent conventions and gotchas.
