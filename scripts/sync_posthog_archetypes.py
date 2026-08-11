#!/usr/bin/env python3
"""Sync PostHog visitor behavior into Supabase visitor_archetypes.

Stdlib only. Reads env vars:
  POSTHOG_PERSONAL_KEY   PostHog personal API key (phx_...)
  SUPABASE_URL           Supabase project URL
  SUPABASE_SERVICE_ROLE_KEY

Usage:
  python3 sync_posthog_archetypes.py [--dry-run]
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from urllib import parse, request

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
POSTHOG_HOST = "https://us.posthog.com"
POSTHOG_PROJECT_ID = "464719"
DAYS_BACK = 90
EVENT_PAGE_LIMIT = 100
PERSON_PAGE_LIMIT = 100
MAX_EVENT_PAGES = 200
UPSERT_CHUNK_SIZE = 500

REQUIRED_ENV = [
    "POSTHOG_PERSONAL_KEY",
    "SUPABASE_URL",
    "SUPABASE_SERVICE_ROLE_KEY",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _die_missing_env(missing):
    print("Missing required environment variables:", ", ".join(missing), file=sys.stderr)
    sys.exit(1)


def _die_api_error(call_desc, status, body):
    snippet = (body or "")[:200]
    print(f"API failure: {call_desc}", file=sys.stderr)
    print(f"HTTP {status}: {snippet}", file=sys.stderr)
    sys.exit(2)


def _parse_iso(ts):
    """Parse an ISO 8601 timestamp to an aware datetime."""
    if not ts:
        return None
    try:
        # datetime.fromisoformat supports trailing 'Z' from Python 3.11,
        # but normalizing keeps us compatible with older runtimes.
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def _to_iso(dt):
    if dt is None:
        return None
    return dt.isoformat().replace("+00:00", "Z")


def _safe_float(value):
    """Return a float for a numeric property, or None."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _pathname(url):
    """Extract pathname from a URL; default to '/' for bare origins."""
    if not url:
        return None
    try:
        path = parse.urlparse(url).path or "/"
        return path
    except ValueError:
        return None


def _api_json(url, headers, call_desc):
    """Make a GET request and return parsed JSON; exit(2) on failure."""
    req = request.Request(url, headers=headers)
    try:
        with request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except request.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        _die_api_error(call_desc, exc.code, body)
    except Exception as exc:
        _die_api_error(call_desc, type(exc).__name__, str(exc))


def _post_json(url, headers, payload, call_desc):
    """Make a POST request and return parsed JSON."""
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=body, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=120) as resp:
            # PostgREST upserts may return 201 with no body.
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except request.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        _die_api_error(call_desc, exc.code, body)
    except Exception as exc:
        _die_api_error(call_desc, type(exc).__name__, str(exc))


# ---------------------------------------------------------------------------
# PostHog ingestion
# ---------------------------------------------------------------------------
def fetch_events(headers):
    """Page through PostHog events for the last N days."""
    since = datetime.now(timezone.utc) - timedelta(days=DAYS_BACK)
    after = _to_iso(since)

    base_url = (
        f"{POSTHOG_HOST}/api/projects/{POSTHOG_PROJECT_ID}/events/"
        f"?limit={EVENT_PAGE_LIMIT}&after={parse.quote(after)}"
    )

    events = []
    url = base_url
    pages = 0
    while url and pages < MAX_EVENT_PAGES:
        pages += 1
        data = _api_json(url, headers, f"GET events page {pages}")
        batch = data.get("results") or []
        events.extend(batch)
        url = data.get("next")
        if url:
            print(f"  events page {pages}: fetched {len(batch)} (running {len(events)})")
    if pages >= MAX_EVENT_PAGES and url:
        print(f"  reached max {MAX_EVENT_PAGES} event pages; stopping.")
    return events


def fetch_person_emails(headers):
    """Map every distinct_id to the person's email property."""
    url = (
        f"{POSTHOG_HOST}/api/projects/{POSTHOG_PROJECT_ID}/persons/"
        f"?limit={PERSON_PAGE_LIMIT}"
    )
    email_by_distinct = {}
    pages = 0
    while url:
        pages += 1
        data = _api_json(url, headers, f"GET persons page {pages}")
        for person in data.get("results") or []:
            props = person.get("properties") or {}
            email = props.get("email")
            if not email or not isinstance(email, str):
                continue
            for distinct_id in person.get("distinct_ids") or []:
                if distinct_id:
                    email_by_distinct[distinct_id] = email
        url = data.get("next")
        if url:
            print(f"  persons page {pages}: mapped {len(email_by_distinct)} ids")
    return email_by_distinct


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------
def build_archetypes(events, email_by_distinct):
    """Aggregate per-distinct_id behavior from PostHog events."""
    # Each entry holds intermediate mutable state.
    raw = defaultdict(
        lambda: {
            "pageviews": 0,
            "visit_dates": set(),
            "total_seconds": 0.0,
            "first_seen": None,
            "last_seen": None,
            "cities": [],
            "city_seen": set(),
            "country_codes": [],
            "country_seen": set(),
            "devices": [],
            "device_seen": set(),
            "browsers": [],
            "browser_seen": set(),
            "os": [],
            "os_seen": set(),
            "page_counts": defaultdict(int),
            "utm_first_seen_at": None,
            "utm_source": None,
            "utm_medium": None,
            "utm_campaign": None,
            "signed_up": False,
        }
    )

    for ev in events:
        distinct_id = ev.get("distinct_id")
        if not distinct_id:
            continue

        ts = _parse_iso(ev.get("timestamp"))
        if ts is None:
            continue

        props = ev.get("properties") or {}
        name = ev.get("event") or ""
        a = raw[distinct_id]

        # First / last seen across all events
        if a["first_seen"] is None or ts < a["first_seen"]:
            a["first_seen"] = ts
        if a["last_seen"] is None or ts > a["last_seen"]:
            a["last_seen"] = ts

        # Pageview metrics
        if name == "$pageview":
            a["pageviews"] += 1
            a["visit_dates"].add(ts.date())
            path = _pathname(props.get("$current_url"))
            if path:
                a["page_counts"][path] += 1

        # Signup signal
        if name == "relaunch_signup":
            a["signed_up"] = True

        # Session duration (null-safe, guard non-numeric).
        # $session_duration exists on some events; $pageleave carries
        # $prev_pageview_duration (seconds spent on the page just left).
        for dur_key in ("$session_duration", "$prev_pageview_duration"):
            seconds = _safe_float(props.get(dur_key))
            if seconds is not None and seconds >= 0:
                a["total_seconds"] += seconds

        # Categorical properties (ordered unique)
        for key, store, seen in [
            ("$geoip_city_name", a["cities"], a["city_seen"]),
            ("$geoip_country_code", a["country_codes"], a["country_seen"]),
            ("$device_type", a["devices"], a["device_seen"]),
            ("$browser", a["browsers"], a["browser_seen"]),
            ("$os", a["os"], a["os_seen"]),
        ]:
            value = props.get(key)
            if value and isinstance(value, str):
                normalized = value.strip()
                if normalized and normalized not in seen:
                    seen.add(normalized)
                    store.append(normalized)

        # First-touch UTM: keep values from the earliest event that carries them.
        utm_src = props.get("utm_source")
        utm_med = props.get("utm_medium")
        utm_camp = props.get("utm_campaign")
        has_utm = utm_src or utm_med or utm_camp
        if has_utm and (
            a["utm_first_seen_at"] is None or ts < a["utm_first_seen_at"]
        ):
            a["utm_first_seen_at"] = ts
            a["utm_source"] = utm_src if isinstance(utm_src, str) else None
            a["utm_medium"] = utm_med if isinstance(utm_med, str) else None
            a["utm_campaign"] = utm_camp if isinstance(utm_camp, str) else None

    # Convert to serializable rows.
    now = datetime.now(timezone.utc)
    rows = []
    for distinct_id, a in raw.items():
        email = email_by_distinct.get(distinct_id)
        identified = bool(email)

        # Top 10 pages by view count.
        sorted_pages = sorted(a["page_counts"].items(), key=lambda x: (-x[1], x[0]))
        top_pages = dict(sorted_pages[:10])

        rows.append(
            {
                "distinct_id": distinct_id,
                "email": email,
                "identified": identified,
                "signed_up": a["signed_up"],
                "first_seen": _to_iso(a["first_seen"]),
                "last_seen": _to_iso(a["last_seen"]),
                "pageviews": a["pageviews"],
                "visit_days": len(a["visit_dates"]),
                "total_seconds": round(a["total_seconds"], 3),
                "cities": a["cities"] or None,
                "country_codes": a["country_codes"] or None,
                "devices": a["devices"] or None,
                "browsers": a["browsers"] or None,
                "os": a["os"] or None,
                "top_pages": top_pages if top_pages else None,
                "utm_source": a["utm_source"],
                "utm_medium": a["utm_medium"],
                "utm_campaign": a["utm_campaign"],
                "updated_at": _to_iso(now),
            }
        )

    return rows


def apply_supabase_signups(archetypes, supabase_url, supabase_key):
    """Mark archetypes as signed_up when their email exists in public.signups."""
    url = f"{supabase_url}/rest/v1/signups?select=email,created_at,source"
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Accept": "application/json",
    }
    data = _api_json(url, headers, "GET signups")

    signup_emails = {row.get("email") for row in data if row.get("email")}
    marked = 0
    for row in archetypes:
        if row.get("email") in signup_emails:
            row["signed_up"] = True
            marked += 1
    print(f"  marked {marked} archetypes signed_up from Supabase signups table")


# ---------------------------------------------------------------------------
# Upsert
# ---------------------------------------------------------------------------
def upsert_archetypes(archetypes, supabase_url, supabase_key, dry_run):
    """Upsert archetype rows into Supabase via PostgREST merge-duplicates."""
    if not archetypes:
        print("  no archetypes to upsert")
        return

    url = f"{supabase_url}/rest/v1/visitor_archetypes"
    headers = {
        "Content-Type": "application/json",
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Prefer": "resolution=merge-duplicates",
    }

    total = len(archetypes)
    chunks = [
        archetypes[i : i + UPSERT_CHUNK_SIZE]
        for i in range(0, total, UPSERT_CHUNK_SIZE)
    ]

    if dry_run:
        print(f"  DRY RUN: would upsert {total} rows in {len(chunks)} chunk(s)")
        return

    for idx, chunk in enumerate(chunks, start=1):
        status, body = _post_json(url, headers, chunk, f"POST visitor_archetypes chunk {idx}/{len(chunks)}")
        print(f"  upsert chunk {idx}/{len(chunks)}: HTTP {status} ({len(chunk)} rows)")


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------
def print_summary(events, archetypes):
    identified = sum(1 for a in archetypes if a.get("email"))
    signed_up = sum(1 for a in archetypes if a.get("signed_up"))

    print("\n--- Summary ---")
    print(f"events read:     {len(events)}")
    print(f"archetypes:      {len(archetypes)}")
    print(f"identified:      {identified}")
    print(f"signed_up:       {signed_up}")

    top = sorted(archetypes, key=lambda a: a.get("pageviews", 0), reverse=True)[:3]
    print("\ntop 3 by pageviews:")
    for a in top:
        label = a.get("email") or f"{a.get('distinct_id', '')[:24]}..."
        print(
            f"  - {label}: "
            f"pageviews={a.get('pageviews')}, "
            f"visit_days={a.get('visit_days')}, "
            f"total_seconds={a.get('total_seconds')}, "
            f"cities={a.get('cities')}, "
            f"devices={a.get('devices')}"
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Sync PostHog visitor behavior into Supabase visitor_archetypes."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the full pipeline but skip the final Supabase upsert.",
    )
    args = parser.parse_args()

    missing = [k for k in REQUIRED_ENV if not os.environ.get(k)]
    if missing:
        _die_missing_env(missing)

    posthog_key = os.environ["POSTHOG_PERSONAL_KEY"]
    supabase_url = os.environ["SUPABASE_URL"]
    supabase_key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

    posthog_headers = {
        "Authorization": f"Bearer {posthog_key}",
        "Accept": "application/json",
    }

    print("1/4 Fetching PostHog events...")
    events = fetch_events(posthog_headers)

    print("2/4 Fetching PostHog persons for emails...")
    email_by_distinct = fetch_person_emails(posthog_headers)

    print("3/4 Aggregating archetypes...")
    archetypes = build_archetypes(events, email_by_distinct)

    print("4/4 Applying Supabase signup status...")
    apply_supabase_signups(archetypes, supabase_url, supabase_key)

    print("Upserting archetypes...")
    upsert_archetypes(archetypes, supabase_url, supabase_key, args.dry_run)

    print_summary(events, archetypes)


if __name__ == "__main__":
    main()
