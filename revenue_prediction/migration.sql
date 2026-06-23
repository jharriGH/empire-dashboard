-- Empire state history — daily snapshots for revenue prediction model.
-- Applied 2026-05-11 against Supabase project dhzpwobfihrprlcxqjbq.

CREATE TABLE IF NOT EXISTS public.empire_state_history (
  id              bigserial PRIMARY KEY,
  snapshot_at     timestamptz NOT NULL DEFAULT now(),
  mrr             numeric,
  active_clients  integer,
  hot_leads       integer,
  close_rate      numeric,
  raw_state       jsonb
);

CREATE INDEX IF NOT EXISTS idx_empire_state_history_snapshot_at
  ON public.empire_state_history (snapshot_at DESC);
