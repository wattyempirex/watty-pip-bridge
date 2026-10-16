# Paper trader rulebook — experimental simulated book

Purpose: grade the lab's research process over weeks by paper-trading it.
Separate track from Akshay's real decisions. NEVER a recommendation to him.
Authorized 2026-10-09; sizing/fills revised per his 2026-10-09 refinements.
Starts Monday 2026-10-12.

## Book
- Starting equity: $100,000 paper (his instruction; the growth of this $100k
  is the scoreboard). USD. No margin, no leverage.
- Direction: LONG ONLY (matches the "go in on a stock" framing; revisit if
  he asks).
- Universe: the 22-ticker watchlist only — same stocks the research checks
  watch. No separate universe, no separate signals.

## Measurement conventions (consolidated 2026-10-15; Watty-inspired)
- All timestamps are America/New_York; all bars are regular-session daily
  bars unless stated otherwise. A "close" means the completed 16:00 ET
  regular-session close — never a developing intraday bar.
- Close-based rules (stops, expiries) are evaluated ONLY against completed
  daily bars, by the 16:15 ET post-close check. Intraday checks (0930–1530
  ET) never adjudicate a close-based rule — that was the 2026-10-15 SNDK
  miss, now closed by construction.
- Fills book at prices actually seen (bid/ask with quote timestamps, or
  last with "spread-unavailable, used last"). If a finalized daily bar is
  unavailable at evaluation time, the last regular-session print may stand
  in as PRELIMINARY, flagged as such, and reconciled against the finalized
  bar at the next opportunity.
- Early closes and market holidays: no bars, no evaluations, no entries —
  the calendar gate decides, silence is the correct output.

## Sizing — conviction-based (his instruction: not fixed)
Bands are arbitrary starting parameters for the experiment, not optimized:
- High conviction: $20,000–$30,000 notional
- Medium conviction: $10,000–$20,000 notional
- Low conviction: $5,000–$10,000 notional
- Max 3 concurrent positions.
- Block-cohort cap (Pixel-approved 2026-10-14): max 2 concurrent positions
  per block-cohort — semicap (AMAT/LRCX, r=0.91) and memory (MU/SKHY/SNDK,
  r=0.78–0.80) trade as blocks; correlated entries are one bet, size
  accordingly.
- Every entry states its conviction tier + one-line why. No adding to an
  existing position in the same ticker.

## Fills — prices actually seen (his instruction)
- Buy (long entry): at the ASK. Sell (exit): at the BID. Use the bid/ask
  actually seen at decision time, with quote timestamps recorded.
- If bid/ask unavailable for a ticker: fall back to last price and log
  "spread-unavailable, used last".
- Stop-first on ambiguous bars (adopted 2026-10-15 from Watty's execution
  layer): a daily bar touching BOTH the stop and the target reference books
  the stop — conservative by construction. A gap through the stop exits at
  the bar open, never at the stop price.

## Costs
- Fills already cross the spread (buy ask / sell bid).
- PLUS 1% of entry notional per completed round-trip trade (his "fees and
  random market pricing" assumption).
- Net P/L per trade = (bid_exit − ask_entry) / ask_entry × notional
  − 0.01 × notional.

### Dual-cost kill discipline (Watty-adopted 2026-10-14, Pixel-approved)
- Every future kill/adopt verdict on a signal CONCEPT must show results at BOTH cost tiers: the 1% scoreboard tier AND the realistic 20bps tier (30bps sensitivity where informative).
- The falsifier stays binding at the 1% tier: a signal that hits net <= $0 over its falsifier window retires, period.
- But no concept dies on the 1% tier ALONE: if the 1% evidence kills while the 20bps evidence shows positive edge-driven (not fee-driven) economics, the concept goes to Rook for a stay-or-kill verdict with both tiers on record, instead of retiring by cost model.
- Prospective only. Past verdicts stand as recorded — e.g. S1's retirement is unaffected (fails at 20bps too: +$3,289 total, negative at 30bps, edge confined to one pocket).

## Approved entry signals (pre-registered 2026-10-13, his instruction: ~1 trade/day)
Forged by Forge, approved by Rook (independent veto gate) on 2026-10-13.
Two proposed specs (INSIDE-BREAK, VOLUME-SURGE) were VETOED — 3-day holds
cannot clear the 1% + spread friction on their own math. All survivors are
momentum-only: no mean-reversion (v1.1 A2 stays falsified), no rotation-fade,
no single-day overnight-continuation shape. Each spec carries trigger +
rule-derived invalidation + expiry, so all three satisfy the 2026-10-13
entry bar. New entries default LOW conviction ($5,000–$10,000). Never force
a trade when no signal fires. Each signal carries a binding falsifier:
retire permanently when its trade count hits net ≤ $0 (spread + 1% cost).

### S1 — BREAKOUT-10D — RETIRED 2026-10-14 (Pixel-approved)
- Was: 10-day high breakout, 5-day trend hold. 4y backtest (Oct 2022–Oct
  2026): 481 trades, gross +$10,504 → net −$25,571 under the 1% cost.
  Falsifier fired. No further triggers evaluated; no entries.

### R1 — SQUEEZE-BREAK — RETIRED 2026-10-14 (Pixel-approved)
- Was: volatility-contraction breakout, 5-day hold. Three strikes:
  (1) original 0.60-gate spec fired 1 trade in 6 months across 22 tickers
  (unevaluable); (2) loosened V7 re-forge (0.80 gate): 238 trades/4y, net
  −$19,894, negative in EVERY sector; (3) final pre-registered 18-cell
  viability grid (session 7, r1_final_grid.json): 15 of 18 cells negative
  net; only positives n=2 (+$266) and n=4 (+$20) — noise. The concept has
  no life in this universe. No further triggers evaluated; no entries.

### R2 — CLOSE-20D (20-day closing-high breakout, 10-day hold)
- Trigger (checks ≥10:15 ET, all required): (a) C20 = highest close of prior
  20 daily bars; (b) P ≥ 1.010×C20; (c) volume ≥ 1.25 × pro-rated avg20;
  (d) no open position.
- Entry: long at check last. Invalidation: exit on any check printing
  last < C20 (~1.0–2.0% risk). Hold: 10 trading days, 15:50 ET exit day 10,
  no target. 10-day window raises earnings-gap exposure (unhedged, logged).
- Falsifier: 15 triggered trades net ≤ $0 → retire (lower N for lower
  frequency). Distinct from S1 (20-day closes vs 10-day highs; 10-day hold).
- Rook note: best cost geometry of the three — longest hold amortizes the
  fixed 1%.
- v3 sector filter (Pixel-approved 2026-10-14, from 4y backtest; v3.1
  2026-10-14: "other" REMOVED — PLTR/SNOW/NFLX edge is ticker-specific and
  regime-flipped, no shared mechanism): R2 trades ONLY in broad semis /
  memory / semicap (semicap at realistic costs only). Optical, mega-cap
  tech, and other/idiosyncratic EXCLUDED (R2 optical −$4,914, megatech
  −$4,778 over 4y). 2026-10-14: AAPL R2 fired live — SKIPPED per this filter.

### 4y backtest provenance — point-in-time update (Watty-adopted 2026-10-14, session 12, Pixel-approved)
- The 434-trade / +$14,699 figure above is the 19-ticker watchlist run (SKHY/SNDK/ARM excluded per coverage rule).
- Pre-registered point-in-time re-run (M2): SOX constituents as of Aug 2022 (Wikipedia rev 1105073321), 28 names with full bars, identical R2 spec, no sector filter.
- Scored result: SEVERE selection bias at the 1% tier — dropped 19 names: 346 trades, −$3,097 (−$8.95/trade); overlap 9 names: 211 trades, +$17,449 (+$82.70/trade). At 20bps: MODEST (dropped +$51.05/trade vs reference +$93.87/trade).
- The point-in-time parallel estimate — **557 trades / +$14,352 (+$25.77/trade)** — is now the lab's reported 4y R2 headline. It replaces the watchlist number in provenance; no bias-dollar subtraction is valid.
- The edge concentrates in 9 overlap names (+$17,449) plus SNDK/ARM (+$20,169 over 37 trades — 'interesting now' names); it does not generalize to the broader 2022 semis universe at punitive costs.
- Forward paper falsifiers carry the validation burden. Spec: hidden_files/backtests/pit_universe_spec.md; results: pit_universe_results.json/.md.

Falsifier scoreboard (updated by each check; binding):
- S1 BREAKOUT-10D: RETIRED 2026-10-14 (falsifier fired on 4y backtest)
- R1 SQUEEZE-BREAK: RETIRED 2026-10-14 (concept dead: 3 strikes, final 18-cell grid 15/18 negative)
- R2 CLOSE-20D: 0 trades, net $0.00 (falsifier at 15 trades net ≤ $0)
- H3 MEMORY-SHOCK-RS: 1/15 (trade #1 OPEN: SNDK entered 2026-10-14 close $1403.3400,
  5-trading-day hold → exit Oct 21 close; mark $1,364.21 @2026-10-15 15:30 ET,
  gross P/L −$209.11; $75 1% cost accrues on completion; stop = close <
  $1,403.34, adjudicated on completed daily closes; falsifier at 15 trades
  net ≤ $0)
- R2-TRAIL (forward shadow spec, forged 2026-10-14 session 10; Rook APPROVED
  with binding amendments A1–A8, Pixel A8 APPROVED): 0 shadow trades.
  Same R2 entries (paired, A1); exit = earlier of close below ratcheting
  trailing-20D-low stop (init at C20, window excludes current bar, close-only
  from entry+1) or +10-bar time exit (A2). Shadow-only — live-book exits
  unchanged. Falsifier (A4, binding): retire permanently if cumulative shadow
  net ≤ $0 over the FIRST 20 completed shadow trades (entry-chronological;
  12-month clock, min-10 fallback, one 6-month extension). Adoption path
  STRUCK (A6): no live adoption without fresh Rook review at ≥40 completed
  shadow trades vs a ~2 SE bar. Noise baseline (A5, matched frozen pairs
  n=432): mean V1−V0 +$12.65/trade, std $323.49, SE $15.56, mean/SE 0.81 —
  the post-hoc improvement sits inside its own noise band. Reference
  discrepancy on record: the frozen V1 backtest initialized the stop at the
  prior 20-bar MINIMUM close (not C20) and used raw Close; the forged shadow
  uses binding A2 (C20 init) — full V1 parity not claimed; the frozen
  +$28,009 is a directional reference, not an exact preview. The "93 losers
  saved, 0 winners cut short" framing is retired (A7). Spec:
  hidden_files/backtests/r2_trail_spec.md; evaluator:
  hidden_files/backtests/r2_trail.py (self-test PASS).

## Entries
- Revision 2026-10-13 (his instruction: 3-day flat book is too quiet — the
  experiment needs trades to grade): entries allowed from any Rook-APPROVED
  WATCH item, not only "worth-a-look" setups, provided the item has (a) a
  stated trigger/entry zone, (b) a rule-derived invalidation/stop reference,
  and (c) an expiry. The "genuinely compelling" bar is lowered to "meets the
  checklist." Rook's veto still kills any entry, and item-level Rook bars
  (e.g. "no paper-trader entry" on attribution-only items) still override.
  Most checks will still enter nothing, but the expected rate is now ~1–3
  trades/week rather than ~0. Selective by design, not silent by design.
- New entries default to LOW conviction ($5,000–$10,000) unless the checklist
  is strong → medium. HIGH conviction ($20,000–$30,000) reserved for
  multi-confirmation setups only.
- Each entry logs: date, ticker, entry time, bid/ask seen, fill price,
  notional, conviction tier + why, stop reference + rule, target reference
  (if any), rationale tags (which setup features/indicators drove it, e.g.
  volume-expansion, level-break, RSI-divergence, news-catalyst), one-line
  thesis, invalidation.

## Exits
- Stop reference hit → exit, reason "stop".
- Target reference hit → exit, reason "target".
- Thesis invalidated → exit, reason "thesis-invalidated".
- 15:50 ET time-stop → exit at verified bid, reason "eod-flat", UNLESS the
  thesis is explicitly multi-day with a stated reason → hold overnight, reason
  "overnight-hold" with the reason logged; re-evaluated next trading day.
- Exits evaluated at check times only — blind windows between checks disclosed.

## Reporting
- Each check with open positions: one terse status line per position in the
  main-chat message (price vs entry, P/L, vs stop/target).
- 1530 ET check: full daily report — starting equity, every trade (buy/sell
  times + bid/ask seen + fill prices, exit reason, gross/net P/L), stop-hits
  vs voluntary exits, overnight holds carried, ending equity ($100k → ?).
- Friday 1530 ET: week-to-date attribution by rationale tag (which setup
  types/indicators made or lost money net of spread + the 1% cost).
- Every paper-trader section carries the header:
  "PAPER TRADER (simulated book — not a recommendation)".

## Evaluation guardrails
- Rationale tags exist so weekly reviews can attribute results to setup
  types/indicators.
- No parameter optimization off paper results (that would overfit the experiment).
- Paper profits never presented as validation of a live signal.
