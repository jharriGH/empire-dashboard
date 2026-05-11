"""Revenue Prediction Engine — King James Empire.

Pulls live empire state from Jim Brain GET /context, joins it with
historical state snapshots from Supabase `empire_state_history`, and
produces 30/60/90 day MRR projections with pessimistic/base/optimistic
ranges (p10/p50/p90).

Model (weighted projection):
    monthly_new_mrr   = hot_leads * close_rate * avg_deal_size
    30d_predicted_mrr = current_mrr + monthly_new_mrr
    60d_predicted_mrr = 30d * (1 + growth_rate)
    90d_predicted_mrr = 60d * (1 + growth_rate)

Variants:
    p10 = base run with close_rate * 0.5  (pessimistic)
    p50 = base run with close_rate * 1.0  (expected)
    p90 = base run with close_rate * 1.5  (optimistic)

avg_deal_size is inferred from the last 30 days of history (mrr deltas /
new_clients deltas) and falls back to $99 (Empire base SaaS tier) if no
history is available yet.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from typing import Optional

import requests

BRAIN_URL = os.environ.get(
    "BRAIN_URL", "https://jim-brain-production.up.railway.app"
)
BRAIN_KEY = os.environ.get("BRAIN_KEY", "jim-brain-kje-2026-kingjames")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")

DEFAULT_DEAL_SIZE = 99.0
HTTP_TIMEOUT = 15


@dataclass
class EmpireState:
    mrr: float
    active_clients: int
    hot_leads: int
    close_rate: float
    raw: dict


@dataclass
class Forecast:
    p10: float
    p50: float
    p90: float


def fetch_current_state() -> EmpireState:
    """Pull live empire state from Brain /context."""
    r = requests.get(
        f"{BRAIN_URL}/context",
        headers={"x-brain-key": BRAIN_KEY},
        timeout=HTTP_TIMEOUT,
    )
    r.raise_for_status()
    ctx = r.json()
    dyn = ctx.get("dynamic", {}) or {}
    hot = dyn.get("hot_leads_queue", 0)
    if isinstance(hot, list):
        hot = len(hot)
    return EmpireState(
        mrr=float(dyn.get("mrr") or 0.0),
        active_clients=int(dyn.get("active_clients") or 0),
        hot_leads=int(hot or 0),
        close_rate=float(dyn.get("vapi_close_rate_7d") or 0.0),
        raw=dyn,
    )


def _sb_get(path: str, params: Optional[dict] = None) -> list:
    if not SUPABASE_URL or not SUPABASE_KEY:
        return []
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/{path}",
        params=params or {},
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Accept": "application/json",
        },
        timeout=HTTP_TIMEOUT,
    )
    r.raise_for_status()
    return r.json() if r.text else []


def avg_deal_size_30d(default: float = DEFAULT_DEAL_SIZE) -> float:
    """Infer average deal size from last 30 days of empire_state_history.

    deal_size = (mrr_now - mrr_30d_ago) / (clients_now - clients_30d_ago).
    Falls back to `default` when there is no history, no client delta, or
    the inferred delta is non-positive.
    """
    since = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
    rows = _sb_get(
        "empire_state_history",
        {
            "select": "mrr,active_clients,snapshot_at",
            "snapshot_at": f"gte.{since}",
            "order": "snapshot_at.asc",
        },
    )
    if len(rows) < 2:
        return default
    first, last = rows[0], rows[-1]
    mrr_delta = float(last.get("mrr") or 0) - float(first.get("mrr") or 0)
    client_delta = int(last.get("active_clients") or 0) - int(
        first.get("active_clients") or 0
    )
    if client_delta <= 0 or mrr_delta <= 0:
        return default
    return round(mrr_delta / client_delta, 2)


def _project(state: EmpireState, deal_size: float, close_rate: float) -> dict:
    """Compound projection across 30/60/90d windows."""
    new_mrr_30 = state.hot_leads * close_rate * deal_size
    p30 = state.mrr + new_mrr_30

    growth = (new_mrr_30 / state.mrr) if state.mrr > 0 else (
        new_mrr_30 / max(p30, 1.0)
    )
    p60 = p30 * (1 + growth)
    p90 = p60 * (1 + growth)
    return {"30d": round(p30, 2), "60d": round(p60, 2), "90d": round(p90, 2)}


def predict(state: Optional[EmpireState] = None) -> dict:
    """Build a full 30/60/90 day forecast with p10/p50/p90 bands."""
    if state is None:
        state = fetch_current_state()
    deal_size = avg_deal_size_30d()

    pess = _project(state, deal_size, state.close_rate * 0.5)
    base = _project(state, deal_size, state.close_rate * 1.0)
    opti = _project(state, deal_size, state.close_rate * 1.5)

    def band(k: str) -> dict:
        vals = sorted([pess[k], base[k], opti[k]])
        return {"p10": vals[0], "p50": vals[1], "p90": vals[2]}

    return {
        "current_mrr": state.mrr,
        "30d": band("30d"),
        "60d": band("60d"),
        "90d": band("90d"),
        "assumptions": {
            "hot_leads": state.hot_leads,
            "active_clients": state.active_clients,
            "close_rate_base": state.close_rate,
            "close_rate_pessimistic": round(state.close_rate * 0.5, 4),
            "close_rate_optimistic": round(state.close_rate * 1.5, 4),
            "avg_deal_size_30d": deal_size,
            "model": "monthly_new_mrr = hot_leads * close_rate * avg_deal_size; compounded across 30/60/90d",
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(predict(), indent=2))
