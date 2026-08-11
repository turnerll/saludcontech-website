# COMPA PostHog configuration — captured 2026-08-11

Captured from the live PostHog UI (Mac Mini Chrome, logged-in session) for project
**joincompa-production** (id `306035`). Text-based capture via in-page DOM dumps;
screenshots were not possible from a headless SSH session (no GUI access).

## COMPA (joincompa-production, project 306035)

### Session replay (Settings → Session replay)
- Record user sessions: **ON**
- Capture console logs: **ON**
- Capture canvas elements: OFF
- Capture network requests: **ON**
- Capture headers: OFF · Capture body: OFF
- Recording conditions: no trigger groups; legacy conditions = **all sessions, 100% sampling**, no minimum duration, no URL blocklist
- Masking: **Normal (mask inputs but not text/images)**
- Retention: **30 days**
- Integrations: Linear (joincompa), GitHub (compa-research)

### Autocapture (Settings → Autocapture)
- Web autocapture: **ON** (evidence: autocaptured events present — Rageclick, Pageleave, Pageview, "User interactions")
- Web vitals (CLS, FCP, LCP, INP): **ON** (evidence: dedicated p75 insights exist and receive data)
- Dead clicks: OFF (capture_dead_clicks analog; no dead-click events seen)
- Data attributes: `data-attr`
- NOTE: this corrects the earlier handoff guess that COMPA runs explicit events only. Autocapture is ON.

### Custom events observed
`Card Revealed`, `Reading Completed`, `Share Tapped`, `Survey Completed`,
`survey_milestone_10`, `survey_milestone_20`, `survey_question_answered`
(plus PostHog autocapture stock events: $pageview, $pageleave, $rageclick, $autocapture, $set)

### Actions
None defined.

### Dashboards
- **COMPA 4DX War Room** — 4 Disciplines of Execution scorecard (WIG, lead measures, cadence)
- **Core web metrics** — traffic, top pages, top referrers, device breakdown, web vitals p75 (LCP/INP/CLS), exception rate, last 30 days
- My App Dashboard (legacy)

### Saved insights (selection)
Exception rate · CLS p75 · INP p75 · LCP p75 · Device type breakdown · Top referrers · Top pages

### Feature flags / Experiments
None active.

---

## Replicated into the Ligazon/SCT project (464719) — 2026-08-11

Done via the PostHog API (personal key, `turnerlloveras@alumni.usc.edu` account):

- **Session replay enabled** (`session_recording_opt_in = true`). Console logs and performance capture were already on. Retention already 30d. Masking default (Normal), 100% sampling — matches COMPA.
- **Autocapture**: left ON (was the default; COMPA runs ON too). No code change needed in `src/layouts/Layout.astro`.
- **Dashboard "SaludConTech"** (id `1986725`) with five insights:
  - Relaunch signups (daily) — id `10951978`
  - Signup funnel: $pageview → relaunch_signup — id `10951979`
  - Top pages (30d) — id `10951980`
  - Top referrers (30d) — id `10951981`
  - Device type breakdown (30d) — id `10951982`
- **Weekly email subscription** of the dashboard to `turnerlloveras@alumni.usc.edu` (Mondays 09:00 PT), id `115807`.
- **Alert**: "SaludConTech daily signups" (id `019ff311-71a8-0000-e127-cab257b85937`), daily, fires when signups ≥ 1, subscribed: turnerlloveras@alumni.usc.edu. (API note: alert creation requires `config: {"type": "TrendsAlertConfig", "series_index": 0}` — that missing field was the cause of the earlier "Unsupported alert config type" errors. Schema learned from COMPA's working "Daily Visitors Anomaly Alert".)

## End-to-end proof (2026-08-11)
- Real-Chrome signup on https://saludcontech.com produced:
  - Supabase row in `public.signups`: `sct-verify-20260811@ligazon.org`, source `saludcontech.com`, interest `newsletter`
  - PostHog `relaunch_signup` event with `$host=saludcontech.com`, GeoIP Los Angeles, US, `site=saludcontech`
