# SaludConTech Strategy & Research Context

> Distilled from the 2026-08-03 handoff. This is reference material for content, pricing, and outreach decisions. The current action state is in `HANDOFF-2026-08-11.md`.

## Who SaludConTech is

**Mission/vision candidates (use 2026 formulations):**
- 2025 LHIA-integrated vision: "a future where Latino communities lead the transformation of healthcare through technology, entrepreneurship, and community-driven innovation."
- 2026 repositioning: "the Latino-led digital health innovation house: B2B advisory and market access for incumbents entering the 68-million-person Latino health market, and a capital, mentorship, and community engine for Latino founders, MDs, and operators."
- Daniel's new direction (this session): expand cross-industry (all occupations), healthcare as the common thread via social + digital determinants of health.

**Timeline (carry UNVERIFIED flags):**
- Founded 2018 (LA; 1st symposium w/ Manos Accelerator + Google Developers at Google HQ — UNVERIFIED).
- SDHES 2022: 1,000-attendee CAPACITY (design capacity, not verified attendance), keynote Dr. Mario Molina (video on YouTube).
- Dec 2 2022: DHEC 22 (Airmeet).
- May 18 2023: The LinkUp NYC w/ Techqueria + CHCF.
- Aug 2 2023: CHCF x Techqueria x SCT Mixer, BioscienceLA.
- Spring 2023: +200 Slack members (265 accounts created in 2023).
- 2024: sponsor of national healthcare tech leaders letter; HLTH Foundation scholarship partnership.
- Mar 2025: HIMSS25 Collaborator.
- 2024-26 dormancy.
- Fall 2026: relaunch as curated convening engine.

**Membership counts:**
- 659 members (medicine, engineering, venture, public health).
- Slack: 342 members, 16,183 messages (Jun 2024 analytics), 48-66 channels incl. 10 city channels (LA, NYC, SF, Houston, Miami, Chicago, Dallas, San Antonio, Phoenix, San Diego).

**Monetization tiers from Daniel's files:**
- Foundation (free) / Professional $200/yr / Founder Circle $500/yr invite-only cap 150 / Investor Network $1,000/yr application-based.
- Revival doc: Founder $500-1,000; Funder $25K VC / $5K angels; Ecosystem $10K institution / $250 individual.
- Corporate: Entrepreneur Track $200-300; Corporate Partner $2,500-5,000; Institutional custom.
- Sponsorships: Platinum $100K x1, Gold $50K x2, Silver $25K x4, Bronze $10K x8 = $450K target.
- B2B: advisory retainers $20-80K/mo; accelerator "La Cohorte" (10 cos, $150K cash + $50K services for 4% SAFE, $3M Y1 fund); research partnerships $150-400K; exec ed $5-15K/seat.

**Post-DEI positioning rule:** frame as "better health outcomes" / "community health solutions"; never "health equity" / DEI / "Latinx".

## Ecosystem strategy research

**Price anchors:** Hampton $9,500/yr; Chief $5,800-9,800; YPO ~$10K initiation + $4-8.6K/yr; The Information Pro $749-999; Soho House ~$1,270/yr.

**Latino set:** Techqueria (free, 25K+), Latinas in Tech LiT 365, SomosVC (~150 VCs), VCFamilia (650+), ALPFA $200/yr, Prospanica $120/yr, Stanford LBAN/SLEI, Visible Hands VHLX, Angeles Investors (Accredited $1,500/yr), Latino Founders.

**The gap:** nobody convenes Latino founders + funders + operators cross-industry; nobody owns healthcare; nobody pairs community/clinical grounding with capital; the $1,500-5,000 curated-room price band is empty.

**The 5 moves:**
1. Claim the empty $1,500-5,000 band anchored ~$1,500/yr with a free layer beneath.
2. Make capital the product: sell funders deal flow/SPV/GP-LP dinners; sell founders access.
3. Run the freemium flywheel on Luma.
4. Moat = healthcare + community grounding lens no one else owns.
5. Seed first 50 paid members via Salesflow against the 659-member list + Luma list.

**LinkedIn tooling (Salesflow):** $99/mo; 400 connection requests/mo, 800 Open InMails, 2,000 follow-ups. Safety: 100-150 invites/wk on warm account, warm up 2-4 weeks. Sequence: pitch-free connection request, then 3-5 messages over 10-21 days, value-first, stop after 3 non-replies. Expect 30-40% accept, 5-15% reply.

**Luma:** free forever; 5% fee on paid tickets (Luma Plus $59/mo = 0%). Conversion ladder: newsletter → free event → paid ticket → paid membership.

## COMPA PostHog replication checklist

**Client-side (done on SCT):** `/ingest` proxy + `ui_host` us.posthog.com, pageview+pageleave, session recording on in code, respect_dnt, localStorage+cookie, super props environment/app_version/UTM, identify on signup. COMPA does NOT use autocapture (explicit events only). SCT currently has autocapture enabled via PostHog init defaults; decide deliberately whether to turn it off to match COMPA.

**Server-side (optional):** COMPA fires a fire-and-forget POST to `https://us.i.posthog.com/capture/` with public key, adds `source:'server'` + `environment`. COMPA events: `signup_completed`, `rsvp_confirmed`, `invite_sent`, `checked_in/no_show`, `followup_completed`, `mutual_matched`, `seat_hold_paid`. For SCT, replicate shape with site events; client capture already covers newsletter signup.

**Dashboard-side (manual Mac Mini clicks):**
1. Session recording toggle ON in Project Settings.
2. Build funnel insight: `$pageview` → `#join` view → `relaunch_signup`.
3. Create one dashboard/insight page.
4. Verify GeoIP city appears on a real visitor post-proxy.
5. Add a signup alert for `relaunch_signup` (COMPA has no alerting — do not copy that gap).

## Execution plan (phases 0-5)

**Phase 0 — Deploy + Dashboard:** DNS CNAME for saludcontech.com; PostHog dashboard clicks; manual Slack digest test.
**Phase 1 — Site Foundation:** Astro scaffold, fact module, verification script. (Now largely superseded by the public Astro site; remaining: add `scripts/verify-astro.cjs`, `.github/workflows/`, ES pages, fact-based Stats.)
**Phase 2 — Content Build-Out:** Use Slack digest + this doc for homepage, The Room, Proof, Membership tiers, Events, Cities, Join flow, Sponsor page.
**Phase 3 — Membership + Money:** Pick tiers, Luma paid tickets, Stripe membership, sponsor page.
**Phase 4 — Outreach Engine:** Luma import, Salesflow sequences, Twenty CRM.
**Phase 5 — Ligazon Leftovers:** Dependabot, old container decommission, welcome email endpoint.

## Key IDs and rules

**IDs:**
- PostHog org: `019eb357-2112-0000-ca29-74d64d5a1bff`
- PostHog project: `464719`
- Slack workspace: `T7HT7BA0H`
- Slack channel #ligazon-stats: `C0BAHDFJG2W`
- Slack bot: `antigravity_swarm`
- Supabase project: `jcxagmhvwakkxogfyrzv`

**Rules:**
- No em dashes. Never "health equity", "DEI", "Latinx", "race" in labels, "unskilled/low-skilled".
- Never trust a 200: real browser + screenshot before claiming a page works.
- Secrets only in `~/pai/secrets/`; never commit service-role/sbp_/phx_ keys.
- SQL access: pooler URL in `~/pai/secrets/ligazon_backend.env`.
- Supabase project `jcxagmhvwakkxogfyrzv` is shared with a foreign campground app that revokes grants; if PostgREST 401/42501 recurs, re-grant per ligazon CLAUDE.md.
- Names of real people never go in git.
- `cp`/`rm` are interactive-aliased; use `command cp`. Astro needs `nvm use 22`.

## Content sources

- Slack export: `/mnt/t9/docs/SLACKEXPORT/SaludConTech _ Latino Health Innovation Alliance Slack export Oct 14 2017 - Mar 1 2026/`
- Comeback spec (website copy): `/home/djtl/cowork-archive/2026-07-16/outputs/local_6404d1a6-b0a0-413d-a5b2-8632813c6da5/SALUDCONTECH-COMEBACK-2026-07-16.md`
- Google Drive index: `0AJMJPiME4dRyUk9PVA__SCT_LHIA.json`
