# SaludConTech Website — Rolling Handoff

## READ THIS FIRST — 2026-08-12 PM

**The 2026-08-12 session record (decisions, research, dead ends) is in the cowork folder:**
`~/Documents/claude-cowork/01-Projects/saludcontech/HANDOFF-2026-08-12-membership-sponsors-analytics.md`
(Mac: `/Users/mac_papi/Documents/claude-cowork/01-Projects/saludcontech/`). Read it before pricing,
outreach, or Cloudflare-token work.

**One-line next step:** delete the leaked Cloudflare API token (id `35511cd6f8974a30ef14bc9196e5d023`,
dashboard row "Edit Cloudflare Workers", last used Aug 11) on the Mac Mini — exact next attempt is in
the cowork handoff, section 5 — verify it dead via `/user/tokens/verify`, then shred
`/tmp/cf-pages-token.txt`.

## Current state (snapshot, updated 2026-08-12 PM)

- **Canonical folder:** `/home/djtl/Projects/saludcontech-website` → repo `turnerll/saludcontech-website`.
- **Domain:** `saludcontech.com` live. **7 pages** including `/membership` (invite-only, no prices)
  and `/sponsor` ($450K ladder: Platinum $100K x1, Gold $50K x2, Silver $25K x4, Bronze $10K x8).
  Both verified 200 on the live domain 2026-08-12 PM.
- **Latest commit:** `76f5a44` (run `git log --oneline -1` for absolute latest).
- **Stats are fact-driven:** `LigazonDataViz.astro` pulls from `data/facts.json` via
  `src/data/sctFacts.ts`. Known discrepancy: GDP card renders `approvedViz` 4.1 while facts.json
  says 4. Flagged, not resolved.
- **CI gate live:** `.github/workflows/ci.yml` + `scripts/verify-astro.cjs` — verified-facts check,
  7-page presence, voice rules (no em dash, no "health equity"/DEI/Latinx). It caught 5 em dashes
  in page titles on its first run; they are fixed (titles use `|`).
- **Archetype sync automated:** `scripts/run_archetype_sync.sh` daily 06:00 via cron, logging to
  `~/pai/logs/sct-archetype-sync.log`. Secrets mapped from `~/pai/secrets/ligazon_backend.env`
  (no duplicated values). 57 visitor rows at last check. The parallel lane's weekly inline cron
  was removed (superseded).
- **Design base:** Ligazon design port (parallel lane, 2026-08-12 AM) is the live design.
- **Signup:** name + email ONLY (Daniel's rule). The phone/SMS field was added (36c4f50) and
  reverted (0cddcb0) per Daniel. Do not reinstate without his word.
- **Parallel sessions commit to this repo/main.** `git fetch` + rebase before every push.

## Decisions that supersede older docs

- **saludcontech.org: dropped.** Unregistered, stays unregistered; .com only (Daniel). The
  2026-08-11 handoff's "optional redirect" is superseded. Do not register it.
- **Membership: invite-only, no Stripe, no published prices** (Daniel, 2026-08-12). Paid tiers
  wait for density triggers; sponsors are the first revenue (competitor evidence in cowork handoff).
- **Founding Circle pricing is WITH DANIEL:** $500 founding, cap 150, stepping to $1,500
  (strategy/2026-08-12-SCT-GAME-PLAN.md in cowork). Do not publish prices anywhere.

## Immediate next steps

1. Delete the leaked token (see top of file). ~18 rounds of dashboard automation failed; the exact
   next probe and the 30-second manual fallback are in the cowork handoff, section 5.
2. Draft the Luma reactivation email for the 659-member list (draft only; Daniel approves).
3. Newsletter send path: listmonk (:9015) auth broken (403). Daniel picks: fix listmonk vs Resend.
4. 43 Dependabot advisories (18 high) on main: targeted npm overrides only, never audit-fix-force.
5. Queued by parallel lane: Drive sweep for recent SCT docs into cowork; 777 Wayback photos
   (docs/recovery/wayback/image_urls.txt); Events page with real photography.

## Rules

- All SCT work stays in this folder. `~/Projects/saludcontech-site` is a frozen backup (committed
  marker file says so). The ligazon folder is the design donor, not the workspace.
- Cloudflare Pages project name is `saludcontech-relaunch`, not `saludcontech-website`.
- Build: `source ~/.nvm/nvm.sh && nvm use 22 && npm run build`. Gate: `node scripts/verify-astro.cjs`.
- Secrets only in `~/pai/secrets/`; never commit service-role/sbp_/phx_ keys or Cloudflare tokens.
- No real names in git. House voice: no em dashes; never "health equity"/DEI/Latinx.
- Start sessions with fresh `opencode` in THIS folder so CLAUDE.md loads (not `occ`).
