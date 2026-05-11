// revenue_prediction_card.tsx
// Dashboard widget for the King James Empire Revenue Prediction Engine.
// Renders 3 cards (30d / 60d / 90d), each showing p50 with a p10–p90
// range bar. Card frame is colored green when the forecast trends up vs.
// current_mrr, red when it trends down, neutral when flat.

import { useEffect, useMemo, useState } from "react";

type Band = { p10: number; p50: number; p90: number };

type Prediction = {
  current_mrr: number;
  "30d": Band;
  "60d": Band;
  "90d": Band;
  assumptions: {
    hot_leads: number;
    active_clients: number;
    close_rate_base: number;
    close_rate_pessimistic: number;
    close_rate_optimistic: number;
    avg_deal_size_30d: number;
    model: string;
    generated_at: string;
  };
};

const fmt = (n: number) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(n);

function trendColor(current: number, p50: number) {
  if (p50 > current * 1.01) return { bg: "#0d2f1f", border: "#22c55e", chip: "#22c55e", label: "UP" };
  if (p50 < current * 0.99) return { bg: "#2f0d0d", border: "#ef4444", chip: "#ef4444", label: "DOWN" };
  return { bg: "#1f1f2a", border: "#6b7280", chip: "#9ca3af", label: "FLAT" };
}

function RangeBar({ band, current }: { band: Band; current: number }) {
  const lo = Math.min(band.p10, current);
  const hi = Math.max(band.p90, current * 1.5);
  const span = Math.max(hi - lo, 1);
  const pct = (v: number) => `${((v - lo) / span) * 100}%`;
  return (
    <div style={{ position: "relative", height: 10, margin: "8px 0", background: "#111827", borderRadius: 6 }}>
      <div
        style={{
          position: "absolute",
          left: pct(band.p10),
          width: `calc(${pct(band.p90)} - ${pct(band.p10)})`,
          top: 0,
          bottom: 0,
          background: "linear-gradient(90deg,#ef4444,#facc15,#22c55e)",
          borderRadius: 6,
        }}
      />
      <div style={{ position: "absolute", left: pct(band.p50), top: -3, width: 2, height: 16, background: "#fff" }} />
      <div style={{ position: "absolute", left: pct(current), top: -3, width: 2, height: 16, background: "#60a5fa" }} />
    </div>
  );
}

function ForecastCard({
  label,
  band,
  current,
}: {
  label: string;
  band: Band;
  current: number;
}) {
  const c = trendColor(current, band.p50);
  return (
    <div
      style={{
        flex: 1,
        background: c.bg,
        border: `1px solid ${c.border}`,
        borderRadius: 12,
        padding: 16,
        minWidth: 200,
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: 14, color: "#94a3b8", letterSpacing: 1 }}>{label}</span>
        <span
          style={{
            background: c.chip,
            color: "#000",
            fontSize: 11,
            fontWeight: 700,
            padding: "2px 8px",
            borderRadius: 999,
          }}
        >
          {c.label}
        </span>
      </div>
      <div style={{ fontSize: 28, fontWeight: 700, color: "#f8fafc", marginTop: 8 }}>
        {fmt(band.p50)}
      </div>
      <div style={{ fontSize: 12, color: "#cbd5e1" }}>
        Range: {fmt(band.p10)} – {fmt(band.p90)}
      </div>
      <RangeBar band={band} current={current} />
      <div style={{ fontSize: 11, color: "#64748b" }}>
        vs. current {fmt(current)} •
        {band.p50 > current
          ? ` +${fmt(band.p50 - current)}`
          : ` -${fmt(current - band.p50)}`}
      </div>
    </div>
  );
}

export default function RevenuePredictionCard({
  endpoint = "/api/revenue/predict",
}: {
  endpoint?: string;
}) {
  const [data, setData] = useState<Prediction | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    fetch(endpoint)
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`))))
      .then((j) => !cancelled && setData(j))
      .catch((e) => !cancelled && setError(String(e)));
    return () => {
      cancelled = true;
    };
  }, [endpoint]);

  const assumptions = useMemo(() => data?.assumptions, [data]);

  if (error) {
    return (
      <div style={{ padding: 16, background: "#2f0d0d", border: "1px solid #ef4444", borderRadius: 12, color: "#fecaca" }}>
        Revenue prediction failed: {error}
      </div>
    );
  }
  if (!data) {
    return <div style={{ padding: 16, color: "#94a3b8" }}>Loading revenue forecast…</div>;
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
        <h3 style={{ margin: 0, color: "#f8fafc" }}>Revenue Forecast</h3>
        <span style={{ fontSize: 12, color: "#64748b" }}>
          Current MRR: {fmt(data.current_mrr)} • {assumptions?.hot_leads ?? 0} hot leads
        </span>
      </div>
      <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
        <ForecastCard label="30 DAYS" band={data["30d"]} current={data.current_mrr} />
        <ForecastCard label="60 DAYS" band={data["60d"]} current={data.current_mrr} />
        <ForecastCard label="90 DAYS" band={data["90d"]} current={data.current_mrr} />
      </div>
      {assumptions && (
        <details style={{ fontSize: 11, color: "#94a3b8" }}>
          <summary>Model assumptions</summary>
          <div style={{ marginTop: 6, lineHeight: 1.5 }}>
            <div>close_rate (base): {assumptions.close_rate_base}</div>
            <div>close_rate (pessimistic / optimistic): {assumptions.close_rate_pessimistic} / {assumptions.close_rate_optimistic}</div>
            <div>avg deal size (30d): {fmt(assumptions.avg_deal_size_30d)}</div>
            <div>active clients: {assumptions.active_clients}</div>
            <div style={{ fontStyle: "italic", marginTop: 4 }}>{assumptions.model}</div>
            <div>Generated: {assumptions.generated_at}</div>
          </div>
        </details>
      )}
    </div>
  );
}
