# Sector-aware entry model v3.1 — Pip, session 5 (2026-10-14)

Amends v3. PAPER/RESEARCH. Falsifiable, pre-registered, no tuning.

## v3.1 allocation (Pixel-APPROVED 2026-10-14)
- **Traded (1% scoreboard):** R2, unfiltered, in **semis / memory**
  (memory flagged: MU-only evidence in early window). **"Other"
  (PLTR/SNOW/NFLX) REMOVED** — see rationale below.
- **Excluded:** optical (gross-negative at any cost), megatech (v3),
  semicap at 1% (joins at realistic 20bps per v3 cost analysis).
- **Per-sector forward falsifiers (unchanged):** 15 triggers in an
  eligible sector, cumulative net ≤ $0 → drop the sector.

### Why "other" was removed (session 5, per-ticker attribution; stop corrected session 6)
Full replay: other_ticker_attribution.py/.json (rulebook stop: close < C20
trigger level — corrected 2026-10-14 session 6; prior min-close-stop output
preserved in other_ticker_attribution_minclose_stop.json). Per-ticker sum
+$6,941.31 now matches the sector aggregate exactly ($260 discrepancy
resolved — it was 100% the stop definition).
4y R2-other +$6,941 decomposes to ticker-specific, regime-flipped edges:
- PLTR: +$1,883.32 net — edge only in 2024–2025 (+$1,535/+$1,958);
  2023 −$777, 2026 YTD −$833. Dead in the current regime.
- SNOW: +$5,521.67 net — 2026 YTD +$5,047; 2023–2025 combined +$475
  (thin, choppy). Dead in every regime except the current one.
- NFLX: −$463.68 — negative overall (one positive year, 2025 +$712);
  no stable edge in any year.
- S1-other 4y: −$5,539 (signal-specific, session 3).
The bucket has no shared mechanism (AI software / data cloud / streaming)
and no stable forward expectancy — PLTR's edge and SNOW's edge never
coexisted. Keeping it eligible was aggregation illusion. Tickers stay on
watch individually; the bucket is not a tradeable rule.
- RECONCILED (session 6): the $260 per-ticker-vs-aggregate gap was the
  stop definition — replay used prior-20D minimum close; rulebook and v3
  harness use close < C20 trigger level. Corrected; sums match exactly.

## H3 MEMORY-SHOCK-RS — forward paper status (session 5)
- Trade #1: TRIGGERED Oct 13 (cohort −2.38%, SNDK RS +2.05pp). Entry at
  Oct 14 close. 5d hold → exit Oct 21 close. Stop: close < $1,482.33
  (20D lowest close on completed bars through Oct 13; finalizes at entry —
  if Oct 14 close < $1,482.33 the reference updates to the 20D low through
  Oct 14). Notional $7,500, 1% cost. Falsifier: 15 trades net ≤ $0 → retire
  (1 of 15 logged).
- Mid-session monitor (Oct 14 ~10:30 ET): SNDK developing ~$1,436.59,
  −3.1% vs prior close; memory cohort weak again (MU −1.4%, SKHY −3.5%).
  No action until close — entry is at close per spec.

## Live-vs-backtest comparison log (session 5, trigger_scan.py 2026-10-14 ~10:23 ET)
- 22/22 tickers evaluable. S1=0, R1=0, R2=1.
- **AAPL R2 FIRE** (last $345.46 ≥ level $344.68, pace 3.67x) → v3
  megatech exclusion → **SKIPPED, Pixel-approved** (lab decisions to Pixel
  per Akshay 2026-10-14). No paper trade. Conflict logged, resolved.
- V1-vs-V2 semis challenger: V2 10D-close checked on all 7 semis tickers —
  0 fires. V1 (R2) 0 fires on semis. Challenger forward count unchanged
  (V1: 0, V2: 0).

## Earnings-window filter — source scoped (session 5, spec to forge)
- **Source: Nasdaq unofficial earnings calendar API**
  (api.nasdaq.com/api/calendar/earnings?date=YYYY-MM-DD), free, no key.
  Verified 4/4 known dates (TSM 10-15, NFLX 10-20, META+LRCX 10-21,
  GLW 10-27) AND historical dates (2025-10-15 → 32 rows) — so the filter
  is backtestable over 4y.
- Coverage: 21/22 (SKHY Korean listing not covered — exempt/flagged).
- Spec queued for session 6: R2-EW — skip R2 triggers when the ticker
  reports earnings inside the 10-day hold window. Pre-register + backtest
  with/without, then falsifier.

## Regime read (descriptive, 2026-10-14)
semis 27.4% vol / 30th pctile / persist −0.22 (the below-median-vol,
mean-reverting pocket where ~100% of 4y R2 edge lives); memory HIGH-VOL
80th pctile / trending +0.18; megatech mid-vol 56th; optical HIGH-VOL 93rd.

---
# (v3 content follows, unchanged)

Supersedes v2. Four parallel research tracks + one new forged spec.
PAPER/RESEARCH. Falsifiable, pre-registered, no tuning. All numbers 4y
(Oct 2022–Oct 2026) unless noted; $7,500 notional, 0.1% half-spread each
way, fees as stated.

## Akshay's four questions — answers

### 1. One model per sector, or one model + filters?
**One model + sector filters. Decisive.** A pre-registered 7-shape ×
6-sector matrix (all cells reported, no cherry-picking) shows the
10-day-hold close-breakout family (V1=R2 20D, V2 10D, V3 30D) beats 5-day
holds in ALL six sectors, and the sector sign pattern is identical across
all three windows — sectors, not shapes, determine viability. Pullback
entries (V6) are dead-last overall (−$32,450); the "different shape for
mean-reverting sectors" hypothesis is KILLED by data. Optical and
megatech are negative under every shape. The only sector×shape
interaction: semis prefers the 10D window (V2 +$18,387 vs V1 +$13,913).
Rook verdict: do NOT adopt V2 — post-hoc window-picking is overfitting.
V1 stays the traded spec; V2 is a candidate challenger for a future
pre-registered test, not an adoption.

### 2. Dependencies to watch (ranked by evidence)
1. **SPY sign on entry day (strongest found).** R2 triggers on SPY-down
   days average +$167 net (n=86) vs +$1 on SPY-up days (n=348). Best cell:
   down-day breakout inside a 20d market uptrend (+$224, n=65). The signal
   wants breakouts AGAINST a red tape — a relative-strength tell.
2. **Sector vol regime (trailing 60d vs own 4y median).** ~100%+ of R2's 4y
   net comes from below-median-vol entries: LOW +$17,151 (226 trades,
   45.1% win) vs HIGH −$2,453 (208 trades, 38.0%).
3. **Cohort shock proximity.** Optical breakouts within ±2d of a ±3%
   cohort shock: 27.5% win, −$237 avg (n=40); calm optical breakouts: 83%,
   +$313 (n=12). Semicap triggers genuinely cluster near shocks.
4. **Cohort block structure.** Semicap (0.91) and memory (0.78–0.80) trade
   as blocks; megatech fragmented in 2026 (0.47→0.25). Correlated entries
   are one bet, not three — size accordingly.
5. **Honest nulls:** 5d RS persistence predicts nothing (spreads 0.0–0.3pp);
   no NVDA→semis or SPY→sector next-day lead-lag (|r|≤0.15); SPY 20d trend
   sign and consecutive up-days don't separate.

### 3. Regime shifts — characterization
Regimes are (vol level × persistence sign), measured on trailing 60d
windows, NOT calendar years: 2024 = calm (persistence ≈ 0 everywhere);
2026-YTD = fear (vol explosion + deep mean-reversion, megatech excepted).
Nuance that matters: 2026-YTD is simultaneously the highest-vol year AND
R2's best calendar year (+$8,015) — because the edge lives in
below-median-vol *moments within* the year, not in calm years. Semicap
and optical flip by regime (semicap HIGH −$908 / LOW +$1,268; optical
HIGH −$6,162 / LOW +$1,249); semis/memory/other positive in both;
megatech negative in both. Every sector flips year-to-year — no sector
verdict is stable across calendar years.

### 4. Indicators that point direction (entry-day, descriptive)
Separators (pooled terciles): **persist5** (+11.49pp win, +$146/trade),
**breakout_depth** (+11.48pp, +$120.53; shallow breakouts die at the
structural stop — 61% stop rate bottom tercile → 27% top), **rs20**
(+9.41pp, +$99.75). Non-separators: vol percentile, SPY trend sign,
consecutive up-days. Sector caution: persist5 reverses in memory (tiny
cells); breakout_depth reverses in megatech. **Descriptive only — the
session-2 gate experiment proved filtering on these destroys value.**

## v3 allocation
- **Traded (1% scoreboard):** R2, unfiltered, in semis / other / memory
  (flagged: MU-only evidence). Excluded: optical (gross-negative, no cost
  assumption rescues it), megatech, semicap.
- **At realistic 20bps:** semicap joins (R2 +$360 → +$2,880, +$68.57/trade
  — solid, edge-driven); megatech borderline (+$1,042, fee-driven not
  edge-driven — flag, don't size). R2 total at 20bps: +$40,739 (+$93.87/trade).
- **S1:** stays retired. At 20bps it's +$3,289 total but fails at 30bps
  and lives entirely in one pocket (semis +$11,280, all else negative).
  Zombie, not alive.
- **Per-sector forward falsifiers (unchanged):** 15 triggers in an
  eligible sector, cumulative net ≤ $0 → drop the sector.

## New forged spec: H3 MEMORY-SHOCK-RS v1 (PRE-REGISTERED, first backtest done)
- **Trigger (day T):** memory-cohort equal-weight day return ≤ −2% AND
  ticker day return − cohort return ≥ +1.5pp (the RS leader on a shock
  down-day — the SNDK pattern, now backed by the SPY-down-day finding).
- **Entry:** next close. **Hold:** 5 trading days. **Stop:** close <
  entry-day 20D lowest close (R2's structural stop, reused).
- **Falsifier:** 15 trades net ≤ $0 → retire permanently.
- **First backtest (honest, thin):** 41 trades, 61.0% win, gross
  +$10,151 → **net +$7,076 (+$172.58/trade)** at 1% cost. BUT: all 41
  trades fall in 2025-02→2026-10 (needs ≥2 cohort names; MU-only years
  can't trigger), top 3 trades = 67% of P/L, SNDK only 6 trades. This is
  a forged spec with an encouraging first print — NOT a proven signal.
  Next: forward paper-trade it against its falsifier.
- Rationale chain (not tuning): parameters from the observed SNDK
  signature (+1.5–2.3pp above cohort), validated post-hoc by the
  independent SPY-down-day result.

## Dropped this session (dead ends)
- **D5:** R1 re-forge (V7, 0.80 contraction gate). Tradable count (238
  trades/4y) but loses in every sector (−$19,894). Rook's original veto
  stands — R1 is not re-forged.
- **D6:** Pullback entries (V6) as the mean-reversion-sector model.
  Dead-last overall. Hypothesis killed.
- **D7:** H3-as-5d-RS-persistence spec. RS persistence is null; reforged
  around shock-day RS instead (see H3 above).
- **D8:** Semis 10D-window adoption (V2). Measured (+$18,387 vs +$13,913)
  but not adopted — post-hoc selection. Challenger candidate only.

## Descriptive monitors (never gates — D1/session-2 killed gating)
For interpreting live R2 triggers, not filtering: SPY-day sign,
trailing-60d vol-regime flag, breakout-depth tercile, persist5/rs20
context, cohort-shock proximity. Plus a paper-trading risk rule: cap
concurrent positions per block-cohort (semicap/memory r≈0.8–0.9).

## Cost interaction (H1 closed)
20bps rerun on frozen harness: sector flips listed above. The 1% paper
scoreboard stays punitive per Akshay's choice; the 20bps view informs
research direction only.

## Files (this session)
- variant_matrix.md/.py/_results.json — 7×6 matrix (reproduces R2/S1 exactly)
- cost_sensitivity.md/.py/.json — 1%/30bps/20bps per-sector tables
- features_regimes.md/.py/.json — separators + regime attribution
- dependencies.md + dependency_analysis.py — cohort/macro mapping
- h3_trades.json — H3 first backtest ledger
- sector_entry_model_v3.md (this file)

## Infra flags for Muse
- Pixel/Codex CLI broken in this environment: 0.149.0 binary missing
  `codex-code-mode-host` (hard failure); 0.162.1 runs but its sandbox
  lacks `python` on PATH. Two tracks worked around via direct
  implementation. Reinstall/repair before Pixel is relied on for execution.
- `data_4y/*.csv` are yfinance multi-index exports with 3 junk header
  rows; the reference backtest.py DictReader loader silently loads ZERO
  bars from them. Future backtests must parse positionally (Date, AdjClose,
  Close, High, Low, Open, Volume).
