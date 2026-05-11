# 🧠 KJE Empire — CLAUDE.md
# Auto-healed by claude_md_healer.py from Jim Brain state
# Last healed: 2026-05-11 20:00:10 UTC
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

1. Tags: vps, bootstrap, milestone, blocker
2. Alerts: 0
3. Commits: b8b877d, be3c39b, 0076569
4. KJLE Session 2B shipped on 2026-05-10
5. Rebuild target is westcoaststylez.com (currently empty, post-hack-recovery)
6. Two bugs found: parser checks state==bad but API returns invalid so 0 invalids in 87701 cleaned; verify_inline naming inconsistent across emails
7. Just blocked on schema creation
8. Options to unblock: (A) run schema DDL manually in Supabase SQL Editor, (B) regenerate Supabase PAT and update vault
9. Verified on GitHub
10. Commit eaa38d9 with notify.py + /notify endpoints pushed to jim-brain main on 2026-05-10 20:02:58Z

---

## BUILD STATE

**Card:** KJLE BUILD_STATE 2026-05-10 (Session 2B closed)
**Saved:** 2026-05-11T01:21:09.193664

# KJLE Build State — Session 2B (Truelist Bulk Batches) — CLOSED 2026-05-10

## What shipped (commits)
- b8b877d feat(email-clean): Truelist bulk batches architecture (Session 2B)
- be3c39b fix(email-clean): NULL-semantics bug in select_uncleaned_leads
- 0076569 fix(email-clean): paginate select_uncleaned_leads past PostgREST 1000-row cap
- 14 repos updated via brain_sync for new status-banner rule
- KJ_RULEZ.md commit 031a0c3 on kj-bridgedeck/main

## Architecture changes
- New migration: migrations/2026_05_10_truelist_batches.sql (audit table + email_sub_state + email_truelist_batch_id + 2 admin_settings keys)
- Rewrite api/routes/enrichment_email_clean.py: parse_truelist_state (handles ok/invalid/risky/unknown + email_* prefixed variants), is_campaign_eligible (positive whitelist only), select_uncleaned_leads (HOT>WARM>COLD priority with .range() pagination), submit_batch (POST /api/v1/batches + audit), ingest_batch_result (idempotent cursor + id-range UPDATE), 4 new endpoints
- New api/routes/webhooks_truelist.py: receiver shim at /webhooks/truelist/batch-complete?secret=... ready for Truelist dashboard webhook
- scheduler.py: replaced v1 verify_inline loop with batch submitter; new job_email_clean_poll_batches cron every 30 min
- 41-fixture boot check at scripts/test_email_clean_parser.py covering parser vocab, prefixed forms, defensive defaults, positive-whitelist campaign eligibility, CSV ingestion, reordered headers

## Batch-1 verification (LIVE)
- batch_id: 9292028e-f0e3-401a-ac5e-390e92838f9a
- 4000 KJLE leads submitted, 3907 unique emails after Truelist dedup
- Truelist completed in ~95 min wallclock
- Auto-ingest counts: valid=2795, invalid=76, unknown=1129, error=0, no_csv_match=0
- CSV reconciliation: 1:1 with ingest (CSV 2722 ok + 74 invalid + 1111 risky/unknown = 3907 unique; ingest 2795 + 76 + 1129 = 4000 = 3907 + 93 duplicates ✓)
- Per-lead spot-check: 7/7 verified leads matched expected mapping AND scoped to batch-1
- Sub-state preservation working: email_ok 2250, is_role 816, accept_all 326, failed_mx_check 42, failed_no_mailbox 19, unknown 547

## Live segment + email state (post-batch-1)
- total: 560,057 (was 556,830, +3,227 new from CSV import last night)
- hot: 20,596 / warm: 129,524 / cold: 406,710 / unclassified: 3,227
- by_email_status: valid 70,559 / invalid 76 (was 0!) / unknown 17,576 / error 3,490 / pending_batch 18,352

## Bugs found and fixed mid-session
- NULL-semantics bug: select_uncleaned_leads filtered .neq('email_status','pending_batch') which excludes NULL email_status rows in PostgREST. Switched to .is_('email_truelist_batch_id','null'). Same gotcha family as pain Session 1.
- 1000-row response cap: .limit(25000) capped at 1000 per segment so first batch only marked 4000 leads. Switched to .range()-based pagination per segment, drains 1000 at a time.
- Parser bug from v1: checked state=='bad' but Truelist returns 'invalid'. Fixed in parse_truelist_state; verified live by first-ever nonzero invalid count.

## Investigation surprises (worth remembering)
- Truelist's POST /batches accepts but silently ignores webhook_url field. Webhook is dashboard-side config only. Receiver shim built, awaiting dashboard wire-up.
- verify_inline returns inconsistent prefixed/unprefixed state strings (email_invalid vs risky). Parser handles both defensively now.

## Open anomalies for Session 2C
- 2786 orphan leads with email_status='pending_batch' and no parent batch_id. Likely leftovers from earlier aborted submits. Cleanup: flush back to NULL or sweep into next batch.
- 17576 'unknown' leads from v1 verify_inline include hidden invalids (the v1 parser miscategorized state=='invalid' as unknown). Re-verify via new architecture to recover them.
- Truelist dashboard webhook not yet configured. 30-min poller is currently the only completion path. Latency 0-30 min instead of seconds.

## Session 2C scope
1. Configure Truelist dashboard webhook → /webhooks/truelist/batch-complete?secret=... (5 min Truelist UI work)
2. Re-verify the 17576 v1-unknown leads via batch architecture
3. Cleanup 2786 orphan pending_batch rows
4. Watch first full weekend of 4-batches/night nightly cron — expect backlog clear in ~5 days at 100K/day
5. Build Card v9 update reflecting Truelist-v2-as-canonical state

## Pinned items (carry-over)
- Send to DemoBoosterz from Lead Finder (after tour rebuild)
- Schedule local backups for Documents/GitHub folder
- Rotate exposed ReachInbox + DemoEnginez Supabase service role keys on Render


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

*Synced from Brain state at 2026-05-11 20:00:10 UTC.*
*This file is auto-regenerated every 4h. Manual edits will be overwritten
on the next heal if the rebuilt content differs by >20% of lines.*
