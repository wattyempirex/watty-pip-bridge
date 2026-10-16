#!/usr/bin/env python3
"""Measure requested V1 lowest-close stop using local variant_matrix loader/costs."""
import json
from pathlib import Path

import variant_matrix as vm

BASE = Path(__file__).resolve().parent
OUT = BASE / "other_ticker_attribution.json"
TICKERS = ("PLTR", "SNOW", "NFLX")


def replay(ticker):
    bars = vm.load_bars(ticker)
    assert bars, f"No bars loaded for {ticker}"
    position = None
    trades = []
    for i in range(vm.WARMUP, len(bars)):
        date, _, _, _, close, _ = bars[i]
        if position is None:
            level, triggered = vm.entry_V1(bars, i)
            if triggered:
                position = {
                    "index": i, "entry_date": date, "entry_close": close,
                    # RULEBOOK stop (R2 invalidation): exit on close < C20,
                    # the trigger level. Corrected 2026-10-14 session 6:
                    # prior version used prior-20D minimum close (wrong).
                    "stop_level": level,
                }
            continue
        reason = "stop" if close < position["stop_level"] else (
            "time" if i >= position["index"] + 10 else None
        )
        if reason:
            gross, net = vm.net_pl_for(position["entry_close"], close)
            trades.append({
                "entry_date": position["entry_date"], "exit_date": date,
                "entry_close": position["entry_close"], "exit_close": close,
                "stop_level": position["stop_level"], "exit_reason": reason,
                "holding_bars": i - position["index"],
                "gross_pl": gross, "net_pl": net,
            })
            position = None
    return bars, trades, position


def main():
    results = {
        "sector": "other", "signal": "R2 CLOSE-20D / V1",
        "methodology": {
            "data": "local data_4y CSVs; variant_matrix.load_bars positional loader",
            "entry": "close >= 1.010 * prior 20-bar max close; volume >= 1.25 * prior 20-bar mean volume",
            "stop": "close < trigger level C20 (prior 20-bar max close at entry) — RULEBOOK R2 invalidation, corrected 2026-10-14 session 6 (prior version used prior-20D minimum close; old output preserved in other_ticker_attribution_minclose_stop.json)",
            "harness_difference": "none after correction — stop now matches variant_matrix V1 (close < open_pos['level']) and the rulebook",
            "hold_bars": 10, "warmup_bars": vm.WARMUP,
            "notional": vm.NOTIONAL, "flat_round_trip_cost": vm.FLAT_COST,
            "entry_fill": "entry close * 1.001", "exit_fill": "exit close * 0.999",
            "gross_definition": "P/L after harness fill slippage, before flat round-trip cost",
            "net_definition": "gross minus $75 (1% of $7,500)",
            "win_definition": "net P/L > 0; losses are net P/L < 0",
            "year_attribution": "exit year; 2022 reported separately if present",
            "position_policy": "one open position per ticker; no same-bar re-entry; stop before time exit; unclosed final positions excluded",
            "prices": "unadjusted Close, matching harness",
        },
        "tickers": {},
    }
    for ticker in TICKERS:
        bars, trades, position = replay(ticker)
        summary = vm.summarize(trades)
        summary.update({
            "losses": sum(t["net_pl"] < 0 for t in trades),
            "breakevens": sum(t["net_pl"] == 0 for t in trades),
            "gross_pl_total": round(sum(t["gross_pl"] for t in trades), 2),
            "year_net_pl": {str(y): round(sum(t["net_pl"] for t in trades if t["exit_date"].startswith(str(y))), 2) for y in range(2022, 2027)},
            "data_coverage": {"bars": len(bars), "first_date": bars[0][0], "last_date": bars[-1][0]},
            "unclosed_position": position,
            "top_3_trades": sorted(trades, key=lambda t: t["net_pl"], reverse=True)[:3],
            "bottom_3_trades": sorted(trades, key=lambda t: t["net_pl"])[:3],
            "trades": trades,
        })
        assert summary["n_trades"] == summary["wins"] + summary["losses"] + summary["breakevens"]
        assert summary["n_trades"] == summary["stops"] + summary["time_exits"]
        assert abs(sum(summary["year_net_pl"].values()) - summary["net_pl_total"]) < 0.01
        results["tickers"][ticker] = summary
    OUT.write_text(json.dumps(results, indent=2) + "\n")
    for ticker, s in results["tickers"].items():
        print(f"{ticker}: {s['n_trades']} trades, {s['wins']}W/{s['losses']}L, win {s['win_rate']:.1%}; gross ${s['gross_pl_total']:,.2f}, net ${s['net_pl_total']:,.2f}, net/trade ${s['net_per_trade']:,.2f}; stops/time {s['stops']}/{s['time_exits']}")
        print("  Year net: " + ", ".join(f"{y}{'-YTD' if y == '2026' else ''} ${s['year_net_pl'][y]:,.2f}" for y in ('2023', '2024', '2025', '2026')))
        for label, key in (("Top", "top_3_trades"), ("Bottom", "bottom_3_trades")):
            print(f"  {label}: " + "; ".join(f"{t['entry_date']}→{t['exit_date']} gross ${t['gross_pl']:,.2f}, net ${t['net_pl']:,.2f}" for t in s[key]))
        print(f"  Coverage: {s['data_coverage']}; unclosed position: {s['unclosed_position']}")
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
