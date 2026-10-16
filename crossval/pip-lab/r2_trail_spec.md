# R2-TRAIL — pre-registered forward shadow spec

Forged 2026-10-14, session 10. Paper/research only. Forward-only; historical
results are descriptive and earn no forward completed-trade credit.
Rook approved forging subject to binding amendments A1–A8.

## A1 — Entry parity

Shadow enters exactly the live R2 paper book's trades: same ticker, entry,
notional, and fills. Never enter triggers the live book skips. The caller
skips an entry when a same-ticker shadow position is already open; no overlap,
rescheduling, or replacement trades. Log this mandatory skip explicitly. The
shadow eligible entries are therefore a subset of actual live entries when
this overlap constraint binds, never an independent signal stream.

## A2 — Pinned exit rule

Initialize the stop at the live entry's C20 trigger level. On check day t:

`stop_t = max(stop_(t-1), min(close_(t-20), ..., close_(t-1)))`

The trailing 20 trading-bar window EXCLUDES the current bar. Check closes from
entry+1 onward; exit at that close if `close_t < stop_t` (equality does not
stop). Otherwise exit at the close of entry+10 trading days. Whichever occurs
first controls; a stop on day +10 is labeled `stop`. No intraday checks,
lookahead, discretionary changes, or terminal forced liquidation. The stop
never decreases in unchanged price units.

Corporate actions: scale the carried stop by the split price factor before
that effective day's ratchet/check, without discretion (2-for-1 => 0.5;
1-for-10 => 10). Translate the historical trailing window into the same
current price units. A split can decrease the numeric stop only by its
mechanical unit conversion. A consistently adjusted input series already
incorporates split scaling: entry, C20, and all closes must share that basis;
do not apply a split twice.

Implementation: `r2_trail.py`, standard library only, no network calls. API
`evaluate(trade, bars, price_basis=..., split_factors=...)` and local JSON CLI.
Requires 20 pre-entry bars and an explicit price basis. Input preserves live
notional/fills metadata; the evaluator computes exits, not entries or orders.
Output includes exit date, exit close, exit reason (`stop|time`) and the
caller-provided paired live-book exit. Open positions return null exit fields
and `status: open`; these are not completed trades. An unresolved live exit
may remain null while the shadow exit is already complete.

### Reference discrepancies — recorded, not silently reconciled

Direct inspection of session 9 `exit_variants_frozen.py` and its Markdown
shows historical V1 initialized at the prior 20-bar **minimum** close, whereas
binding A2 initializes at the **C20 trigger** (the prior 20-bar maximum in that
backtest). Both ratchet to the prior-window minimum, exclude today's close,
check from +1, use strict `<`, and impose the +10 time exit. Binding A2 governs
this implementation; full historical V1 equivalence is not claimed.

The frozen backtest explicitly uses **raw Close, not Adj Close**. Thus “same
adjusted-close series as the backtest” is factually inconsistent with the
reference. Reference-series parity means `raw_close`, as used by the replay.
For forward evaluation, support explicit `adjusted_close` with consistently
adjusted entry/C20 and history, or `raw_close` with mechanical split factors;
record the choice in every ledger entry and never switch within a trade. An
adjusted forward run must be labeled as differing from the historical raw
series. This disclosure prevents an unsupported data-parity claim.

The self-test replays five fixed AMAT records from `exit_variants_frozen.json`:
2023-05-17, 2024-01-19, 2024-02-09, 2024-05-15, 2025-05-12. It asserts identical
exit dates, closes, reasons, and paired live exits. These are common time-exit
fixtures, not evidence of full V1 parity. Additional synthetic checks cover
C20 initialization, exclusion of current close, strict inequality, pending
status, stop precedence on +10, and split conversion.

## A3 — Separate ledger and reporting

Log entries/exits in a dedicated **R2-TRAIL shadow track** section of the paper
ledger. Use a separate **1530-ET-check: R2-TRAIL shadow track** reporting line.
Zero comingling with live-book entries, exits, totals, or performance claims.
Record ticker, entry date/close, notional/fills, C20, price basis, split factors,
shadow exit, paired live exit, completion count, costs, and shadow net P/L.
Use the same live-book fill/cost convention for comparison; no favorable
cost substitution. Historical noise uses the frozen $7,500 notional and $75
per completed trade, without spreads. Preserve skipped-overlap records.

## A4 — Binding falsifier

Retire permanently if cumulative shadow net P/L is **<= $0 over the FIRST 20
completed shadow trades in entry-chronological order**. Completed means exited
via stop or time exit; no exclusions. Break same-date ordering by ticker, then
live trade identifier if necessary; freeze this ordering at entry. Do not
replace a pending earlier entry with a later completed entry to reach 20;
resolve earlier entries before locking the first-20 cohort. Costs count.

The 12-month clock starts at the first forward shadow entry. If fewer than
20 complete within 12 months, evaluate the completed set (minimum 10). If
still fewer than 10, grant exactly one 6-month extension, then evaluate the
completed set regardless of count. Apply the same <= $0 permanent-retirement
threshold to the time-capped cohort, including $0 for an empty set. Publish
the outcome either way. Freeze the evaluation cohort and show unresolved
positions separately; no discretionary exclusions or repeat extensions.

## A5 — Noise baseline

Matched completed pairs **n=432**; mean **V1-V0 = +$12.65/trade**;
**std = $323.49**; **SE = $15.56**; **mean/SE = 0.81**.

The post-hoc improvement sits inside its own noise band (**~0.8 SE**).
These are matched historical pairs, not a forecast or proof of an edge.
The stated std uses population standard deviation of the 432 differences;
SE = std / sqrt(432). Using sample SD instead gives $323.86 and SE $15.58,
without changing that conclusion. Do not substitute unmatched book totals.

## A6 — Adoption rule STRUCK

The >=30-trade/>=20-lead adoption path is **VOID**. No live-book adoption
without a **fresh Rook review at >=40 completed shadow trades** against a
**pre-stated noise-aware bar**. Guidance: paired shadow-minus-live lead
>= ~2 SE of the paired-difference mean, and shadow total net > $0. Compare
mean paired dollar delta with SE of that mean, not total dollars against
mean SE. Freeze the bar and SD convention before the prospective review
cohort is observed; do not tune it to observed results. Shadow completions
and completed matched pairs may differ while live exits are pending: disclose
both counts and compute paired statistics only when both exits exist.
Surviving the falsifier earns **continued shadow status only**. No automatic
adoption, live-book edits, or order execution.

## A7 — Reporting rhetoric

The '93 losers saved, 0 winners cut short' framing is **retired**. Report
paired delta ± SE, running completed count, and cumulative shadow net only.
Show matched-pair count alongside delta ± SE; with fewer than two completed
pairs report SE as unavailable. Entry dates define cohort ordering. Reports
must retain the noise-band interpretation and avoid selective winner/loser
stories. Publish the falsifier outcome whether it survives or retires.

## A8 — Pixel approval decision

**APPROVE** the binding-A2 forward-only paper/research shadow implementation
and this disclosed spec. There is no credential exfiltration, production
destruction, authentication bypass, network access, or live execution. The
historical initialization and price-basis discrepancies are explicitly
recorded; approval does not assert full historical V1/data parity. No
live-book adoption is authorized. A fresh Rook review remains mandatory
under A6 before any adoption.
