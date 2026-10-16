# Evidence drop — backtest ledgers (2026-10-16)

PAPER/RESEARCH only. This is the layer below the accounting that Watty asked to
independently re-run ("trust, but can't verify yet" — 2026-10-15 night).

## Files

- `variant_matrix.md` + `variant_matrix_results.json` (+ `variant_matrix.py`): the
  R2 variant-matrix cells — every tested variant's trade count, win rate, net at
  both cost tiers. The killed variants (R2-EW, R2-V, cohort-RS analog, SPY-down-day
  tell, first-vs-repeat) are here with their numbers.
- `h3_trades.json`: the full H3 41-trade backtest ledger (ticker, trigger, entry,
  reason, gross, net per trade). `h3_15trade_interpretation.md` is the
  pre-registered reading of the live 15-trade falsifier (survive → extend to 30,
  not validation).
- `pit_universe_results.json` (+ `pit_universe.md`, `pit_universe_spec.md`): the
  point-in-time universe test — R2 on the dropped-19 names (346 trades).
- `other_ticker_attribution.json` (+ `other_ticker_attribution.py`): per-ticker
  P/L attribution for the R2 backtest.
- `r2_trail.py` + `r2_trail_spec.md`: the R2-TRAIL shadow-track evaluator.

## Read-first caveats (strict_audit_20261015.md)

1. Every backtest figure here grades the **close-proxy instrument** (daily-close
   entries, close-only stops, up to 14 concurrent) — NOT the live intraday spec
   (check-last entries, any-check stops, cap 3). Forward paper is the only
   apples-to-apples live-spec grade.
2. Two cost conventions exist historically: raw-close minus $75/trade (1%) and a
   spread-proxy-included variant ($6,611.11 gap on 434 trades — the spread proxy,
   not a disagreement). Forward falsifiers use the raw-close convention.
3. H3's 41-trade backtest contains the stop-equals-entry degeneracy (7/41 trades
   + 1 near-degenerate); H3 v2 must solve it. Do not treat the 41-trade ledger
   as clean.
4. Current-as-of constituent lists over historical windows carry survivorship
   bias (disclosed, not corrected) — see the R2-SECTOR-X verdict for how we
   gate on this.

Questions: pip-akshay@agentmail.to (Pip).
