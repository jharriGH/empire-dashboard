# 🧠 KJE Empire — CLAUDE.md
# Auto-healed by claude_md_healer.py from Jim Brain state
# Last healed: 2026-05-12 00:00:09 UTC
# Repo: /opt/empire_dashboard

---

## WHO YOU WORK FOR

You are working for Jim Harris — King James Empire (KJE).
Empire-wide rules in `/opt/jim-brain/CLAUDE.md` (KJ_RULEZ) apply unless this
file explicitly supersedes them.

Brain endpoint: `https://jim-brain-production.up.railway.app`
Brain key: `jim-brain-kje-2026-kingjames` (header: `x-brain-key`, lowercase)

---

## PROJECT STATUS

- **Project:** KJE Empire 💰
- **ID:** `kje_empire_1775521531140`
- **Group:** Infrastructure
- **Status:** `live`
- **Description:** This is the foundation of KJE

### Next Action
Set up empire-dashboard GitHub repo and enable Pages. Then: launch DemoBoosterz outreach campaign (product is ready). Then: KJWidgetz Stripe live key swap.

---

## RECENT MEMORIES (top 10)

1. Deploy: github.com/jharriGH/kje-orchestrator → Render service srv-d813bjvavr4c73b223b0 → https://kje-orchestrator.onrender.com
2. Wave 3 fan-out was completed by prior coordinator on 2026-05-11 at 19:51:33Z
3. Emails client via lib/email noreply@kjwidgetz.com
4. Tags: vps, bootstrap, milestone, blocker
5. Alerts: 0
6. Commits: b8b877d, be3c39b, 0076569
7. KJLE Session 2B shipped on 2026-05-10
8. Rebuild target is westcoaststylez.com (currently empty, post-hack-recovery)
9. Two bugs found: parser checks state==bad but API returns invalid so 0 invalids in 87701 cleaned; verify_inline naming inconsistent across emails
10. Just blocked on schema creation

---

## BUILD STATE

**Card:** KJE Orchestrator BUILD_STATE 2026-05-11
**Saved:** 2026-05-11T20:14:22.905640

# KJE Orchestrator — BUILD_STATE 2026-05-11

**Status:** LIVE
**URL:** https://kje-orchestrator.onrender.com
**Render Service:** srv-d813bjvavr4c73b223b0
**Repo:** https://github.com/jharriGH/kje-orchestrator
**Build SHA:** cee25b8799de (P3 v1.0.0)
**Plan:** starter ($7/mo)
**Region:** oregon

## Verified endpoints
| Endpoint | Result |
|----------|--------|
| `GET /health` | HTTP 200 `{"status":"ok","version":"1.0.0"}` |
| `GET /version` | HTTP 200 (build, poll_interval, stall_timeout) |
| `GET /status` | HTTP 500 — pending `kjcodedeck.wave_manifest` table creation |
| `POST /trigger-poll` | guarded by `x-trigger-key` header |

## Files shipped (11)
1. `main.py` — FastAPI app, lifespan boots BrainClient + WaveEngine + Poller
2. `poller.py` — APScheduler 60s tick, calls `wave.process_logs(logs)`
3. `wave_engine.py` — wave_manifest reader, complete/blocked/stalled detection, VPS dispatch
4. `notify.py` — retry+backoff wrappers around `/notify`, `/memory`, `/log`
5. `brain_client.py` — httpx async client with lowercase `x-brain-key`
6. `requirements.txt` — fastapi 0.115.5, supabase 2.9.1, apscheduler 3.10.4, etc.
7. `Procfile` — `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
8. `render.yaml` — service blueprint w/ `sync: false` secrets
9. `Dockerfile` — python:3.11-slim, non-root user, healthcheck
10. `.env.example` — every env var documented
11. `README.md` — full runbook + schema + ops guide
   (+ `.python-version` and `runtime.txt` pinning 3.11.10 after Render's default of 3.14 broke first deploy)

## Wave-chaining logic
- Poll Brain `/logs?limit=50` every 60s (configurable).
- Group entries by `tags + job_id`. Match against active wave's `jobs[]`.
- **Complete:** every job logged `task_complete` → mark wave `done`, chain next queued.
- **Blocked:** any job tagged `blocker`/`fatal`/`halt` → mark wave `blocked`, SMS + memory.
- **Stalled:** >30 min without job-tagged log entries → mark `stalled`, SMS.
- **Chain:** lowest-priority queued wave promoted to `active`, each job POSTed to VPS_DISPATCH_URL with X-Dispatch-Key.

## Env vars on Render (14)
PYTHON_VERSION=3.11.10, BRAIN_URL, BRAIN_KEY, SUPABASE_URL, SUPABASE_SERVICE_KEY,
VPS_DISPATCH_URL=http://192.161.173.97:8091/dispatch, VPS_DISPATCH_KEY (64-char),
TRIGGER_KEY (auto-generated, stored on VPS at /tmp/p3_orch_trigger.env),
POLL_INTERVAL=60, POLL_LOG_LIMIT=50, STALL_TIMEOUT=1800, DISPATCH_TIMEOUT=20,
PROJECT_SLUG=kje_orchestrator, LOG_LEVEL=INFO.

## Gotchas captured
- **Render Python default:** first deploy used Python 3.14.3 (latest) and crashed — must pin via `.python-version` + `PYTHON_VERSION` env var + `runtime.txt`.
- **Render envVars via POST /v1/services:** the envVars array inside serviceDetails was silently dropped on create. Fix: `PUT /v1/services/{id}/env-vars` separately, then trigger redeploy.
- **Brain has no POST /projects:** new projects must be registered through the Brain UI; API exposes only GET/PATCH. `PATCH /projects` for kje_orchestrator currently 404s until Jim adds it.
- **/status 500:** `kjcodedeck.wave_manifest` table does not yet exist in Supabase. Create it before promoting orchestrator to active duty (DDL in README.md).

## Decisions
- Starter plan, oregon, autoDeploy=yes — same shape as kjle/jim-brain.
- 30-min stall timeout (configurable via env).
- Trigger key generated via `secrets.token_urlsafe(40)`, not stored in repo.
- Force-push to main per spec; competing P3v3 build script also pushed (commit 71aff4b7) — currently running container is still `cee25b87` build until a later redeploy promotes the newer commit.

## Next actions
1. Register `kje_orchestrator` project in Brain UI so PATCH /projects works.
2. Run DDL to create `kjcodedeck.wave_manifest` table.
3. Insert first test wave (one harmless job) and watch `/status` cycle through queued → active → done.
4. Tune `STALL_TIMEOUT` after observing first 24h of throughput.

---

## EMPIRE-WIDE RULES (excerpt)

1. **Brain Endpoint Verification** — always hit `/health` then the real
   endpoint with `x-brain-key` header BEFORE coding against it. Document
   actual response shape. No assumptions from convention.

2. **Empire Cost Logging** — any LLM call must be instrumented via
   `kje-cost-logger` per `docs/EMPIRE_COST_LOGGING_BUILD_CARD.md`.

3. **Env Var Automation** — CC never asks Jim to manually click env vars
   into a dashboard. Use Render / Railway / Cloudflare APIs. Tokens live
   in CC env (`RENDER_API_KEY`, `RAILWAY_TOKEN`, `CF_API_TOKEN`).

4. **Gotcha Logging** — log any bug / workaround to Brain via
   `POST /memory` with tags `["kje_empire_1775521531140", "gotcha", "lesson"]` the
   moment context is fresh.

5. **Session Start / End** — every CC session begins with
   `brain_session_start(focus="...", product="kje_empire_1775521531140")` and ends
   with `brain_session_end(...)` + `brain_save_card(...)`.

---

## VAULT KEYS AVAILABLE FOR THIS PROJECT

*No vault keys registered under project `kje_empire_1775521531140`. Empire-wide secrets live in `/vault/shared/*`.*

Empire-wide shared keys (always available):

- `GITHUB_PAT_VPS` — VPS automation PAT (contents:write)
- `SUPABASE-PAT-SHARED` — Supabase DDL automation token
- `SUPABASE_PERSONAL_ACCESS_TOKEN` — Supabase PAT (44+ chars)

---

## SESSION END PROTOCOL

Before closing the chat, run:

```
POST /memory   tags=["kje_empire_1775521531140", "session_end"]
               content="<what shipped, what's next>"
POST /log      tags=["kje_empire_1775521531140", "session_complete"]
               content="<one-liner>"
POST /cards    title="<Project> BUILD_STATE <date>"
               project="kje_empire_1775521531140"
               content="<full markdown spec>"
```

If anything broke, log a gotcha memory FIRST so the next session inherits
the lesson.

---

*Synced from Brain state at 2026-05-12 00:00:09 UTC.*
*This file is auto-regenerated every 4h. Manual edits will be overwritten
on the next heal if the rebuilt content differs by >20% of lines.*

<!-- KJE-ONBOARD-V1 -->
## KJ Empire — SC Onboarding
This repo belongs to the KJ Empire (DevelopingRiches Inc, owner Jim Harris / jharriGH).
- Central repo: jharriGH/kjle. Brain: https://jim-brain-production.up.railway.app
- New SC seats: run brain_status, brain_search this repo's slug, and verify live state before declaring anything done.
- Decide-and-proceed. Cost-gate chargeable dispatches. Never echo secrets — pull keys from the Brain vault.
- See ROADMAP.md for status.
<!-- /KJE-ONBOARD-V1 -->
