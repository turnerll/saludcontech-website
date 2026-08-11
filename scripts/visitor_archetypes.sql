-- Visitor archetypes table: merges PostHog behavioral data with Supabase signups.
-- Rebuilt by scripts/sync_posthog_archetypes.py
-- NOTE: This table is intentionally RLS-off and accessed only via service-role keys.

CREATE TABLE IF NOT EXISTS public.visitor_archetypes (
    distinct_id text PRIMARY KEY,
    email text,
    identified boolean DEFAULT false,
    signed_up boolean DEFAULT false,
    first_seen timestamptz,
    last_seen timestamptz,
    pageviews int DEFAULT 0,
    visit_days int DEFAULT 0,
    total_seconds numeric DEFAULT 0,
    cities text[],
    country_codes text[],
    devices text[],
    browsers text[],
    os text[],
    top_pages jsonb,
    utm_source text,
    utm_medium text,
    utm_campaign text,
    updated_at timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_visitor_archetypes_email
    ON public.visitor_archetypes(email);

CREATE INDEX IF NOT EXISTS idx_visitor_archetypes_last_seen
    ON public.visitor_archetypes(last_seen DESC);

COMMENT ON TABLE public.visitor_archetypes IS
    'Visitor archetypes merged from PostHog behavior + Supabase signups. Rebuilt by scripts/sync_posthog_archetypes.py.';
