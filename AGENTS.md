# SaludConTech Website — agent instructions

**READ FIRST:** the current plan and handoff for this project do NOT live in this repo. They live in
the knowledge base at `~/Documents/claude-cowork/01-Projects/saludcontech/` (same relative path on Mac
and Ubuntu via Syncthing): `HANDOFF-2026-08-16-EXECUTE.md` (the resume point) and
`SALUDCONTECH-PLAN-2026-08-15.md` (section 19 is the 2026-08-18 website relaunch record).
Read the handoff before making changes, and follow it.

## Stack

- Astro 5 static site, Tailwind CSS v4, TypeScript, deployed on Cloudflare Pages
  (project `saludcontech-relaunch`).
- Build: `source ~/.nvm/nvm.sh && nvm use 22 && npm run build`
- Gate (must pass before push): `node scripts/verify-astro.cjs` — verified facts, page presence,
  voice rules. It has caught real defects; never weaken it to make a change pass.
- Deploy: push to `main` and Pages auto-builds. The custom domain's HTML is edge-cached up to 4 hours
  (`cache-control: max-age=14400`); verify on the deployment URL
  (`*.saludcontech-relaunch.pages.dev`) before concluding the live site did not update.

## Truth sources and voice

- Published numbers come from `data/facts.json` via `src/data/sctFacts.ts`. An unknown id fails the build.
- Canon: **336 active members** (never 659), **no "10 city chapters"** claim, GDP **$4.0T** (never 4.1 or 4.7).
- Voice: no em dash, never "health equity" / DEI framing / "Latinx" / "Latino/a/x/e", and none of:
  delve, keen, robust, leverage, landscape, navigate.
- Founder references: "Daniel Turner-Lloveras, MD" only. Adjunct Professor of Medicine at the Keck
  School of Medicine of USC. Principal Investigator at the Public Health Institute since 2021.
  Never "Dr.", never MPH or JD, no board certification in any form.

## Backend

- Forms POST to Supabase project `jcxagmhvwakkxogfyrzv` (tables `signups` and `contact_messages`,
  anon insert). The signup table has an `is_test` flag; never delete rows, flag them.
- Analytics: PostHog project `464719` via the `/ingest` first-party proxy, opt-in-only (consent
  banner). Umami/GA4 entries in the CSP header are stale and queued for removal (handoff Step 2).
- Secrets live in `~/pai/secrets/ligazon_backend.env` on Ubuntu. Never commit keys or tokens.

## House rules

- `~/Projects/saludcontech-site` is a FROZEN backup. Never work there.
- Recovered old-site photography: `recovery-photos/` (234 files, 2015 to 2022). The Photos page
  build is Step 1 of the handoff.
- Parallel agent sessions commit to this repo on `main`: `git fetch` and rebase before every push.
