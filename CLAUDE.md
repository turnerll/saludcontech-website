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
