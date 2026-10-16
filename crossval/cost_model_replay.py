#!/usr/bin/env python3
"""Cost-model replay — run any per-trade ledger through the crossval cost model.

Companion to cost-model-replay-2026-10-14.md (crossval leg 1: Pip's 780-row R2
re-cut ledger through OUR cost model). Pip's lab asked for this script to
reproduce the replay on their side.

Usage:
    python3 cost_model_replay.py [ledger.csv]

Ledger format (per the crossval contract): one row per trade with at least
entry_px, exit_px, side (LONG expected), exit_reason, and a universe column
(defaults to "all" when absent).

Cost model (published in the report, frozen):
  - Notional: $7,500/trade (Pip's spec, kept for comparability)
  - Shares: 7500 / entry_px (fractional allowed — paper)
  - Gross P&L: (exit_px - entry_px) * shares (LONG)
  - Cost tiers: 1% round-trip = $75/trade (punitive)
                 20bps round-trip = $15/trade (realistic)
                 $0.01/share per side, i.e. $0.02/share round-trip
                 (our execution.py default, reference only)
  - No spread/slippage add-on: ledger prices are raw closes per the re-cut notes.

Deterministic: stdlib only, no randomness. Recomputes purely from entry_px /
exit_px / side; prints per-universe totals, per-trade means, win rates, and
exit mix (stop vs time).
"""
import csv
import sys

NOTIONAL = 7500.0
COST_1PCT = 75.0
COST_20BPS = 15.0
PER_SHARE_RT = 0.02  # $0.01/share per side, $0.02 round trip (execution.py default)


def replay(path, universe_col="universe"):
    rows = []
    with open(path, newline="") as f:
        r = csv.DictReader(f)
        for i, row in enumerate(r, 1):
            entry = float(row["entry_px"])
            exit_ = float(row["exit_px"])
            side = row.get("side", "LONG").strip().upper()
            if entry <= 0:
                raise ValueError(f"row {i}: non-positive entry_px {entry}")
            shares = NOTIONAL / entry
            gross = (exit_ - entry) * shares
            if side != "LONG":
                raise ValueError(f"row {i}: side={side!r}, this replay is LONG-only")
            rows.append({
                "universe": row.get(universe_col, "all") or "all",
                "gross": gross,
                "net_1pct": gross - COST_1PCT,
                "net_20bps": gross - COST_20BPS,
                "net_share": gross - PER_SHARE_RT * shares,
                "win": gross > 0,
                "exit_reason": (row.get("exit_reason") or "").strip().lower(),
            })
    return rows


def summarize(rows):
    by_uni = {}
    for r in rows:
        by_uni.setdefault(r["universe"], []).append(r)
    out = []
    for uni, rs in sorted(by_uni.items()):
        n = len(rs)
        g = sum(r["gross"] for r in rs)
        n1 = sum(r["net_1pct"] for r in rs)
        n2 = sum(r["net_20bps"] for r in rs)
        ns = sum(r["net_share"] for r in rs)
        win = sum(1 for r in rs if r["win"])
        stops = sum(1 for r in rs if r["exit_reason"] == "stop")
        times = sum(1 for r in rs if r["exit_reason"] == "time")
        out.append(
            f"universe={uni} n={n} "
            f"gross={g:+.2f} ({g/n:+.2f}/tr) "
            f"net@1%={n1:+.2f} ({n1/n:+.2f}/tr) "
            f"net@20bps={n2:+.2f} ({n2/n:+.2f}/tr) "
            f"net@$0.01sh={ns:+.2f} "
            f"win_rate={100.0*win/n:.1f}% "
            f"exits: {stops} stops / {times} time-exits"
        )
    return out


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "r2-ledger-pip-crossval-2026-10-14.csv"
    for line in summarize(replay(path)):
        print(line)


if __name__ == "__main__":
    main()
