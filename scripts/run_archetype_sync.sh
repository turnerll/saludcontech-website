#!/usr/bin/env bash
# Run the PostHog -> Supabase visitor archetype sync.
#
# Secrets are sourced from ~/pai/secrets/ligazon_backend.env (single home for
# the shared PostHog project 464719 / Supabase jcxagmhvwakkxogfyrzv keys) and
# mapped to the variable names sync_posthog_archetypes.py expects.
# No secret values live in this file.
set -euo pipefail

SECRETS_FILE="$HOME/pai/secrets/ligazon_backend.env"
if [ ! -f "$SECRETS_FILE" ]; then
  echo "Missing secrets file: $SECRETS_FILE" >&2
  exit 1
fi

set -a
# shellcheck disable=SC1090
source "$SECRETS_FILE"
set +a

export POSTHOG_PERSONAL_KEY="$LIGAZON_POSTHOG_PERSONAL_API_KEY"
export SUPABASE_URL="$LIGAZON_SUPABASE_URL"
export SUPABASE_SERVICE_ROLE_KEY="$LIGAZON_SUPABASE_SERVICE_ROLE_KEY"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec /usr/bin/python3 "$SCRIPT_DIR/sync_posthog_archetypes.py" "$@"
