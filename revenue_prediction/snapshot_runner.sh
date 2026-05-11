#!/usr/bin/env bash
# Cron wrapper for revenue_prediction/snapshot.py
# Fetches Supabase creds fresh from Jim Brain vault on every run so
# secrets never sit on disk. Invoked by the 09:00 daily cron entry.

set -eu
cd "$(dirname "$0")"

BRAIN_URL="${BRAIN_URL:-https://jim-brain-production.up.railway.app}"
BRAIN_KEY="${BRAIN_KEY:-jim-brain-kje-2026-kingjames}"

SUPABASE_URL="$(curl -sf "${BRAIN_URL}/vault/kjle/SUPABASE_URL/reveal" -H "x-brain-key: ${BRAIN_KEY}" | jq -r .value)"
SUPABASE_SERVICE_KEY="$(curl -sf "${BRAIN_URL}/vault/kjle/SUPABASE_SERVICE_KEY/reveal" -H "x-brain-key: ${BRAIN_KEY}" | jq -r .value)"

if [ -z "${SUPABASE_URL}" ] || [ "${SUPABASE_URL}" = "null" ]; then
  echo "[$(date -Is)] snapshot_runner: SUPABASE_URL not in vault" >&2
  exit 2
fi

export BRAIN_URL BRAIN_KEY SUPABASE_URL SUPABASE_SERVICE_KEY
exec python3 snapshot.py
