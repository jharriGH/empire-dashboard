"""Daily empire-state snapshot writer.

Pulls live state from Brain /context and appends one row to
public.empire_state_history in Supabase. Scheduled via cron at 09:00.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone

import requests

from predictor import fetch_current_state

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")


def snapshot() -> dict:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError(
            "SUPABASE_URL / SUPABASE_SERVICE_KEY missing from env"
        )

    state = fetch_current_state()
    row = {
        "snapshot_at": datetime.now(timezone.utc).isoformat(),
        "mrr": state.mrr,
        "active_clients": state.active_clients,
        "hot_leads": state.hot_leads,
        "close_rate": state.close_rate,
        "raw_state": state.raw,
    }
    r = requests.post(
        f"{SUPABASE_URL}/rest/v1/empire_state_history",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        },
        json=row,
        timeout=20,
    )
    r.raise_for_status()
    return r.json()[0] if r.text else row


if __name__ == "__main__":
    try:
        result = snapshot()
        print(
            f"[{datetime.now(timezone.utc).isoformat()}] snapshot ok: "
            f"mrr={result.get('mrr')} clients={result.get('active_clients')} "
            f"hot={result.get('hot_leads')} close={result.get('close_rate')}"
        )
    except Exception as exc:
        print(
            f"[{datetime.now(timezone.utc).isoformat()}] snapshot FAIL: {exc}",
            file=sys.stderr,
        )
        sys.exit(1)
