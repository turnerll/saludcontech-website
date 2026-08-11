# SaludConTech Website — Rolling Handoff

## READ THIS FIRST — 2026-08-11

**The full lossless state is in `HANDOFF-2026-08-11.md`. Read that first.**

**One-line next step:** add the Cloudflare DNS CNAME for `saludcontech.com` on the Mac Mini, verify the live domain serves the new build, test a signup + PostHog event, then capture the COMPA PostHog config from the Mac Mini browser and replicate it in the Ligazon/SCT PostHog project.

## Current state (snapshot)

- **Canonical folder:** `/home/djtl/Projects/saludcontech-website`
- **Repo:** `https://github.com/turnerll/saludcontech-website` (public)
- **Domain:** `saludcontech.com`
- **Latest commit:** `443ea8c`
- **Build:** `source ~/.nvm/nvm.sh && nvm use 22 && npm run build` → `dist/`
- **Deployment live:** `https://0e836df8.saludcontech-relaunch.pages.dev/`
- **DNS:** custom domain added but pending CNAME record. The old 2019 page still serves at `saludcontech.com`.
- **PostHog client:** wired via `/ingest` proxy in `functions/ingest/[[path]].js`, key in `src/layouts/Layout.astro`.
- **Supabase signup:** `src/components/Newsletter.astro` posts to `public.signups` in project `jcxagmhvwakkxogfyrzv`.

## Immediate next steps

1. Add CNAME `@` → `saludcontech-relaunch.pages.dev` (proxied) in Cloudflare DNS for `saludcontech.com` (Mac Mini).
2. Verify `curl -I https://saludcontech.com/` returns the new build, not the old LiteSpeed page.
3. Submit the newsletter form and confirm a row in `public.signups` + a PostHog `relaunch_signup` event.
4. Capture COMPA PostHog settings from the Mac Mini browser into `docs/posthog-compa-config.md` + screenshots.
5. Replicate the relevant settings in Ligazon/SCT PostHog project `464719`.
6. Rotate the exposed Cloudflare API token (ID `35511cd6f8974a30ef14bc9196e5d023`) via Cloudflare dashboard.

## Rules

- All SCT work stays in this folder. Do not write to `/home/djtl/Projects/ligazon` or `/home/djtl/Projects/saludcontech-site`.
- Cloudflare Pages project name is `saludcontech-relaunch`, not `saludcontech-website`.
- Start next session with fresh `opencode` (not `occ`) to load k3.
- No real names in git.
- See `CLAUDE.md` for permanent conventions and gotchas.
