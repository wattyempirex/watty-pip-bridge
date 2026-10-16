#!/usr/bin/env python3
"""Pre-registered 7x6 entry-variant matrix (PAPER/RESEARCH ONLY, stdlib only).

Variants (fixed, pre-registered -- do NOT tune):
  V1: 20D CLOSE breakout, 10d hold (R2 shape: 1.010x prior max close, vol>=1.25xavg20)
  V2: 10D CLOSE breakout, 10d hold
  V3: 30D CLOSE breakout, 10d hold
  V4: 20D CLOSE breakout, 5d hold
  V5: 10D HIGH breakout, 5d hold  (S1 shape: 1.010x prior max high, vol filter)
  V6: PULLBACK: close crosses ABOVE 10D SMA after closing below it (>=5 consec days); 5d hold
  V7: CONTRACTION-BREAK: mean(H-L[-5:]) <= 0.80*mean(H-L[-20:]) then close > 10D high; 5d hold

Cost model (same as reference harness): $7,500 notional, entry_fill=Close*1.001,
exit_fill=Close*0.999, $75 flat per completed trade. Stop checked before time exit.
30-bar warmup. Coverage exclusions: SKHY, SNDK, ARM (not fully covered Oct22-Oct26).

V6/V7 per literal spec: NO volume filter, NO breakout multiplier.
V6 stop = entry-day 10D SMA (structural analog of broken level).
V7 stop = entry-day prior 10D high.
"""
import csv
import json
import math
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data_4y")
OUT_PATH = os.path.join(BASE, "variant_matrix_results.json")

NOTIONAL = 7500.0
FLAT_COST = 75.0
WARMUP = 30

SECTORS = {
    "semicap": ["AMAT", "LRCX"],
    "memory": ["MU"],                      # SKHY, SNDK excluded (coverage)
    "optical": ["COHR", "GLW"],
    "megatech": ["MSFT", "AAPL", "GOOGL", "META", "AMZN"],
    "semis": ["NVDA", "AMD", "AVGO", "TSM", "INTC", "QCOM"],  # ARM excluded
    "other": ["PLTR", "SNOW", "NFLX"],
}


def load_bars(ticker):
    """Parse data_4y CSVs: yfinance multi-index layout, data columns by position:
    Date, Adj Close, Close, High, Low, Open, Volume (first 3 rows are junk headers).
    Uses unadjusted OHLC + Volume, same convention as the reference harness."""
    import re
    path = os.path.join(DATA_DIR, ticker + ".csv")
    bars = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or not re.match(r"^\d{4}-\d{2}-\d{2}$", (row[0] or "").strip()):
                continue
            try:
                date = row[0].strip()
                c = float(row[2]); h = float(row[3]); l = float(row[4])
                o = float(row[5]); v = float(row[6])
            except (IndexError, TypeError, ValueError):
                continue
            if any(math.isnan(x) for x in (o, h, l, c, v)):
                continue
            if any(x <= 0 for x in (o, h, l, c)):
                continue
            if v < 0:
                continue
            bars.append((date, o, h, l, c, v))
    bars.sort(key=lambda b: b[0])
    return bars


def net_pl_for(entry_close, exit_close):
    entry_fill = entry_close * 1.001
    exit_fill = exit_close * 0.999
    gross = (exit_fill - entry_fill) / entry_fill * NOTIONAL
    net = gross - FLAT_COST
    return round(gross, 2), round(net, 2)


def avg(lst):
    return sum(lst) / len(lst)


def avg_vol(bars, i, n):
    return avg([b[5] for b in bars[i - n:i]])


def max_close(bars, i, n):
    return max(b[4] for b in bars[i - n:i])


def max_high(bars, i, n):
    return max(b[2] for b in bars[i - n:i])


def sma10_close(bars, i):
    return avg([b[4] for b in bars[i - 10:i]])


def vol_ok(bars, i):
    v = bars[i][5]
    if v <= 0:
        return False
    a20 = avg_vol(bars, i, 20)
    return a20 > 0 and v >= 1.25 * a20


def _breakout_close(bars, i, n):
    """Prior-n-day CLOSE max breakout w/ vol filter; returns (level, triggered)."""
    if not vol_ok(bars, i):
        return None, False
    C = max_close(bars, i, n)
    return C, bars[i][4] >= 1.010 * C


def entry_V1(bars, i):
    return _breakout_close(bars, i, 20)


def entry_V2(bars, i):
    return _breakout_close(bars, i, 10)


def entry_V3(bars, i):
    return _breakout_close(bars, i, 30)


def entry_V4(bars, i):
    return _breakout_close(bars, i, 20)


def entry_V5(bars, i):
    if not vol_ok(bars, i):
        return None, False
    H10 = max_high(bars, i, 10)
    return H10, bars[i][4] >= 1.010 * H10


def entry_V6(bars, i):
    """Close crosses above 10D SMA after >=5 consecutive closes below their 10D SMA."""
    ma_i = sma10_close(bars, i)
    c = bars[i][4]
    if not (c > ma_i):
        return None, False
    for j in range(i - 5, i):
        if not (bars[j][4] < sma10_close(bars, j)):
            return None, False
    return ma_i, True  # stop = entry-day 10D SMA (structural analog)


def entry_V7(bars, i):
    """5D range <= 0.80 x 20D range, then close > prior 10D high."""
    r5 = avg([b[2] - b[3] for b in bars[i - 5:i]])
    r20 = avg([b[2] - b[3] for b in bars[i - 20:i]])
    if r20 <= 0 or r5 > 0.80 * r20:
        return None, False
    H10 = max_high(bars, i, 10)
    return H10, bars[i][4] > H10


VARIANTS = [
    {"name": "V1_20D-close_10d-hold", "entry": entry_V1, "hold": 10},
    {"name": "V2_10D-close_10d-hold", "entry": entry_V2, "hold": 10},
    {"name": "V3_30D-close_10d-hold", "entry": entry_V3, "hold": 10},
    {"name": "V4_20D-close_5d-hold", "entry": entry_V4, "hold": 5},
    {"name": "V5_10D-high_5d-hold", "entry": entry_V5, "hold": 5},
    {"name": "V6_pullback-MA10_5d-hold", "entry": entry_V6, "hold": 5},
    {"name": "V7_contraction-080_10D-high_5d-hold", "entry": entry_V7, "hold": 5},
]


def backtest(tickers, spec):
    trades = []
    for ticker in tickers:
        bars = load_bars(ticker)
        n = len(bars)
        if n <= WARMUP:
            continue
        open_pos = None
        i = WARMUP
        while i < n:
            date, o, h, l, c, v = bars[i]
            if open_pos is None:
                level, triggered = spec["entry"](bars, i)
                if triggered:
                    open_pos = {"idx": i, "date": date, "close": c, "level": level}
                i += 1
            else:
                stop = c < open_pos["level"]
                if stop:
                    reason = "stop"
                elif i >= open_pos["idx"] + spec["hold"]:
                    reason = "time"
                else:
                    reason = None
                if reason is not None:
                    gross, net = net_pl_for(open_pos["close"], c)
                    trades.append({
                        "ticker": ticker,
                        "entry_date": open_pos["date"],
                        "exit_date": date,
                        "exit_reason": reason,
                        "gross_pl": gross,
                        "net_pl": net,
                    })
                    open_pos = None
                i += 1
    return trades


def summarize(trades):
    net = [t["net_pl"] for t in trades]
    n = len(trades)
    wins = [p for p in net if p > 0]
    return {
        "n_trades": n,
        "wins": len(wins),
        "win_rate": round(len(wins) / n, 4) if n else None,
        "net_pl_total": round(sum(net), 2),
        "net_per_trade": round(sum(net) / n, 2) if n else None,
        "stops": sum(1 for t in trades if t["exit_reason"] == "stop"),
        "time_exits": sum(1 for t in trades if t["exit_reason"] == "time"),
    }


def main():
    results = {}
    for sector, tickers in SECTORS.items():
        results[sector] = {}
        for spec in VARIANTS:
            trades = backtest(tickers, spec)
            results[sector][spec["name"]] = summarize(trades)
    with open(OUT_PATH, "w") as f:
        json.dump({"sectors": SECTORS, "results": results}, f, indent=2)
    for sector, tickers in SECTORS.items():
        print(f"== {sector} ({','.join(tickers)})")
        for spec in VARIANTS:
            s = results[sector][spec["name"]]
            print(f"  {spec['name']:<38} n={s['n_trades']:<4} win={s['win_rate']} "
                  f"net=${s['net_pl_total']:>10.2f} per_trade=${s['net_per_trade']}")


if __name__ == "__main__":
    main()
