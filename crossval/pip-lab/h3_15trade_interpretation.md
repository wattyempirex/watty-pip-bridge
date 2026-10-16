# H3 15-trade interpretation — pre-registered 2026-10-15

Written BEFORE the outcome is known (forward test at 1/15, net −$120.48).
The binding falsifier ("retire at 15 trades if cumulative net P/L ≤ $0 at
the 1% tier") stands unchanged. This document fixes what each outcome MEANS,
so neither survival nor kill gets reinterpreted after the fact.

## The power problem (from the 2026-10-15 strict audit, h3_trades.json n=41)
- Per-trade mean +$172.58, sd $869.02; top 3 trades = 67.2% of total profit.
- P(kill at 15 | true edge +$172.58/tr) = 22%.
- P(kill at 15 | true edge +$61.14/tr, ex-top-3 mean) = 39%.
- P(survive 15 | true edge $0) = 50%.
Neither outcome is decisive. Act accordingly:

## If H3 is KILLED at 15 (net ≤ $0)
1. Publish the full 15-trade log plus the ex-top-3 decomposition before
   retiring. A kill concentrated in missing the right-tail trades is
   reported as such, not as "no edge."
2. Retire H3 v1 permanently. No re-forge of the same spec.

## If H3 SURVIVES 15 (net > $0)
1. Survival is NOT validation — it is permission to continue testing.
2. Extend to 30 trades under the identical rule and spec. No parameter
   changes at the extension point.
3. Report the ex-top-3 decomposition alongside the headline at 30.

## H3 v2 (queued — do NOT touch v1 mid-falsifier)
The audit found ~17% of backtest trades had the stop exactly at the entry
close (zero adverse room; the live SNDK trade demonstrated it). v2 re-forge
must either (a) enforce minimum adverse room, e.g. stop = min(20D low
close, entry × (1 − X%)) with X pre-registered, or (b) explicitly
pre-register the degenerate case as its own bet type with its own
expectancy. Forge → Rook → backtest before any v2 paper trade.
