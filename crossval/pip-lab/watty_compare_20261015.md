# Comparative analysis: Watty's shared research vs our lab

Date: 2026-10-15. Author: analysis subagent (read-only review).
Scope: their 8 shared files (`watty-pip-lab-mirror/`) vs our live specs and evidence.
Stance: PAPER/RESEARCH only. Nothing here is a live-trading recommendation.

---

## 0. TL;DR

- Their package contains **three distinct systems**, not one: (1) **PM Edge v0.2** — a two-agent *swing* system (2–10 day holds), forward-testing since 2026-10-06 with **no results shared yet**; (2) **Intraday Sandbox v0.1** — six frozen 5-minute-bar strategies, whose Stage 2 validation starts 2026-10-16 with **zero valid sessions**; (3) **Pattern Farm v0.1** — a 20-pattern annotation vocabulary + per-pattern stats harness.
- **Do not shift to their model.** Verdict in §4.
- **Do borrow selectively:** post-stop MFE tracking, four-way failure classification, MFE/MAE capture per trade, stop-first ambiguous-bar rule, rejected-entry shadow log, and their freeze-manifest documentation practice. All are cheap on our daily-bar data. Details in §2.
- The highest-value integration is the one their README already proposes: **run their PM Edge entries through our falsifier framework** once their forward test reaches a reviewable milestone — cross-validation, not adoption.

---

## 1. What each side actually does

### 1a. Our lab — daily-bar swing, deterministic, close-based

**R2 CLOSE-20D** (`hidden_files/paper_trader/RULEBOOK.md`):
mechanism is a 20-day closing-high breakout: trigger requires (a) new 20-day
highest close, (b) price ≥ 1.010× that close, (c) volume ≥ 1.25× pro-rated
20-day average; entry at check-time last; invalidation is any print below the
20-day-high close (~1–2% risk); 10-trading-day hold, no target. Sector filter
v3.1: broad semis / memory / semicap only. Binding falsifier: retire at
15 triggered trades if net ≤ $0 at the 1% cost tier.

**H3 MEMORY-SHOCK-RS** (`hidden_files/backtests/sector_entry_model_v3.md`
§"New forged spec: H3 MEMORY-SHOCK-RS v1"): trigger on day T requires the
memory cohort (MU/SKHY/SNDK equal-weight) down ≥ 2% AND the ticker
outperforming the cohort by ≥ 1.5pp; entry next close; 5-trading-day hold;
stop = close below the entry-day 20-day lowest close. Binding falsifier:
retire at 15 trades if net ≤ $0 at 1%.

**Process around the specs:** nine intraday checks (0930–1530 ET) plus a new
post-close evaluation (16:15 ET); `trigger_scan.py` deterministic scan;
two-pass Rook (blind then informed, evidence-cited veto); Pixel as
Caliper-pattern reviewer; decision records frozen per entry; conviction
sizing ($5–30k bands) with block-cohort caps; fills at seen bid/ask + 1%
punitive cost tier with a parallel 20bps realistic tier (dual-cost kill
discipline). Ledger: `hidden_files/paper_trader/ledger.md`.

**Evidence state:** R2 — 4y backtest, point-in-time headline 557 trades /
+$14,352 (+$25.77/trade); Watty's independent cost-model replay of our
780-row ledger (current_22: gross +$53,860, 1%-net +$21,310, 20bps-net
+$47,350; pit_19drop: gross +$28,095, 1%-net +$2,145, 20bps-net +$22,905).
H3 — 41-trade backtest (61% win, +$172.58/trade at 1%); forward test live
at 1 of 15, currently −$121.03 after the SNDK stop-out on 2026-10-15.

### 1b. Their PM Edge v0.2 — two-agent swing system (2–10 day holds)

(`pm-edge/PM-Edge-Engine-v0.2-spec.md`, `-implementation-spec.md`, `-FREEZE.md`;
frozen 2026-10-06, forward-testing since.)

Mechanism, precisely:
- **Stage 0 — Market Regime Engine** (spec §3): classifies RISK-ON / NEUTRAL /
  RISK-OFF / EVENT-RISK (−10…+10); adjusts entry bars and sizing; EVENT-RISK
  blocks new entries entirely.
- **Stage 1 — Discovery (Agent A):** scans a ~517-name universe; emits a
  **candidate packet** (frozen schema, impl-spec §7) with an **Opportunity
  Score /100** = catalyst/20 + trend/15 + relative-strength/15 +
  volume-participation/15 + narrative/10 + alignment/10 + liquidity/10 −
  risk penalty/15.
- **Stage 2 — Entry Engine (Agent B, blind):** independently scores from
  (ticker, timestamp, raw data) only — A's packet withheld until commit.
  **Entry Score /100** = pattern/25 (four named patterns × five binary
  checks each, impl-spec §1) + multi-timeframe/15 + VWAP-acceptance/10 +
  volume/15 + location/15 + reward-risk/15 + tape/5.
- **8-point promotion gate** (impl-spec §4): Opportunity_A ≥ 82,
  Opportunity_B_independent ≥ 75, Entry_B ≥ 82 (87 in RISK-OFF),
  |A−B| ≤ 15, anti-chase veto passes, Tier-1 data COMPLETE, expected R ≥ 2.0,
  regime ≠ EVENT-RISK.
- **Anti-chase veto** (impl-spec §2): fires if > 2.5 ATR from validated
  support, > 1.5 ATR above session VWAP, or entry-bar range > 1.0 ATR.
- **Stops/sizing** (impl-spec §3, §5): structural stop anchors with 0.25 ATR
  buffer; stop < 0.5 ATR → setup rejected (never tightened — size down
  instead); **risk-based sizing** `shares = floor(risk$ / risk-per-share)`,
  0.25–1.0% risk by regime, 20% notional cap, max 5 concurrent.
- **Management** (spec §11): **Exit Pressure Score /100** driving a graded
  ladder (HOLD → PROTECT → PARTIAL 20–33% → TAKE PROFIT 33–50% → EXIT NOW),
  plus systematic partials at +2R/+3R.
- **Records** (spec §14–18): insert-only SQLite; frozen A-packet ∪ B-packet ∪
  outcome fields at signal time; post-trade MFE/MAE/R-multiples/alpha;
  **four-way failure classification** (selection / timing / stop / exit);
  **post-stop MFE tracked at 1/3/5 days**; counterfactual stop/entry
  simulations; **shadow trades** for rejected setups (Opportunity ≥ 82 but
  Entry < 82) as a control group for the entry filter.
- **Anti-lookahead:** fills at bar t+1 open, never signal-bar close
  (FREEZE.md correction #3 — they caught and fixed their own v0.1
  lookahead bias); completed-bars-only; no-quiet-changes freeze discipline
  with version bumps.

**Evidence state:** ~7 trading days of forward testing since 2026-10-06.
**No forward results have been shared with us.** First frozen observation
(RKLB, Opportunity 73 → WATCH) is in the freeze manifest. Nothing to
evaluate yet.

### 1c. Their Intraday Sandbox v0.1 — six frozen 5m strategies

(`intraday/strategies.py`, `intraday/execution.py`.)

Six rulebooks, each a pure function `evaluate_*` returning a signal dict or
(None, reason-code): **W1** (VWAP-reclaim after 6-bar below-VWAP streak +
1.5× volume), **W2** (opening-range breakout/retest, 10:00–12:00 window),
**W3** (daily RSI2 < 10 + prior-day −3% + above SMA200, then intraday
engulfing/hammer), **M1** (EMA20 pullback 38–62% retracement + SPY-relative
strength filter), **M2** (prior-session-low breakdown then reclaim within
3 bars), **M3** (ATR-contraction ≥ 6 bars then 1.5× range expansion with a
20-day liquidity filter). Each ships with a `_BASELINE` control variant.
Universe: 20 mega-cap names (`UNIVERSE` frozenset in both files).
`resolve_entry` validates stop geometry at the next open; `execution.py`
implements **stop-first** ambiguous-candle handling, gap-through-stop exits
at bar open, 15:55 EOD liquidation, $0.01/share/side costs, MFE/MAE per
trade, and refuses to fabricate prices on missing bars.

**Evidence state:** Stage 2 (the repaired validation run of these
strategies) starts 2026-10-16. **Zero valid sessions so far** (day 1:
0 signals, infra failures, did not count).

### 1d. Their Pattern Farm v0.1 — annotation vocabulary, not a signal

(`pattern-farm/detector.py`, `pattern-farm/farm_study.py`.)

A deterministic, no-lookahead annotator emitting a 20-pattern vocabulary
over 5m bars: Group 1 = the 12 strategy/baseline names; Group 2 =
microstructure events (`liq_sweep`, `sweep_seq`, `sweep_failed`,
`liq_retest`, `fv_formed`, `fv_inverted`, `structure_break`, `no_liq`).
`farm_study.py` aggregates per-pattern stats from SQLite
(win rate, avg net R, expectancy, profit factor, MAE, stop-hit rate) with a
**minimum-n = 30 reporting bar** ("no edge claims below n=30" — same
discipline as our product's ~30-sample rule).

### 1e. Their Charlie dip study — fundamental research, not traded

(Reviewed in `hidden_files/backtests/session21_notes.md`.) A beaten-down
SMID screen (82 names down ≥50%, 46 mechanically qualified, 29 PASS /
17 REJECT business verdicts, 3.41× survivorship enrichment quantified).
It produces **business verdicts, not trade signals** — a different product
from a trading system. Not comparable to R2/H3 as a system; comparable as
research process (pre-registered criteria, verifier, Caliper audit — all
solid, and already adopted in part via the falsifier template).

---

## 2. Borrow list — specific, with plug-in points and costs

Ordered by value/cost. All are PAPER/RESEARCH process improvements; none
change a live spec mid-test.

### B1. Post-stop MFE tracking (theirs: spec §17)
**What:** after every stopped trade, keep tracking the ticker for 1/3/5
days and record post-stop MFE. Distinguishes "stop was right" (continued
collapse) from "stop architecture is wrong" (stop → rally).
**Plug-in:** our post-close check cron already runs daily; on a stop-out,
record the exit close and append +1/+3/+5-day closes and post-stop MFE to
the ledger day notes. Purely observational — does not alter the traded spec.
**Cost:** trivial — we already pull daily bars; one small addition to the
close-check body. **Value:** directly attacks our open question of whether
R2's `< C20` stop and H3's 20D-low stop sit inside normal volatility.

### B2. Four-way failure classification (theirs: spec §16)
**What:** label every loser selection / timing / stop / exit error
(multiple labels allowed).
**Plug-in:** add a `failure_labels` column to the trade-log table; assign
at the Friday attribution review (or at exit + weekly review for
post-stop MFE, which needs B1 first).
**Cost:** near-zero — process only. **Value:** our Friday attribution is
by rationale tag (what setup lost); this adds *where the mechanism* lost,
which is what actually improves the next spec version.

### B3. MFE/MAE capture per trade (theirs: spec §15; `execution.py::_outcome`)
**What:** record max favorable/adverse excursion per completed trade.
**Plug-in:** compute from the daily bars we already store, for each closed
paper trade; add `MFE`/`MAE` columns to the trade log.
**Cost:** one small script (`hidden_files/backtests/`), run at the Friday
review. **Value:** Rook-grade evidence on stop/target placement; feeds B2
(stop-error vs exit-error labels become measurable instead of judgmental).

### B4. Stop-first ambiguous-bar rule (theirs: `execution.py::_check_bar`)
**What:** when a single bar hits both stop and target, assume the stop
filled first (conservative); gap-through-stop exits at the open, never at
the stop price.
**Plug-in:** one line in the RULEBOOK's Fills/Costs section: "a daily bar
touching both stop and target reference books the stop." Our backtests
already use spread-adjusted fills; this closes the remaining ambiguity.
**Cost:** zero. **Value:** removes a small optimistic bias in both
backtests and paper accounting. (Their Amendment 2 documents exactly this
failure mode — worth adopting the lesson without re-learning it.)

### B5. Rejected-entry shadow log (theirs: spec §26, shadow-trade control)
**What:** track setups that qualified mechanically but were *not* taken
(vetoed, filtered, or skipped) as shadow trades, to test whether the
filter/veto adds value.
**Plug-in:** we already have the pattern — on 2026-10-14 an AAPL R2 fire
was SKIPPED per the megatech filter. Log such skips with entry/exit per
the signal's own rules in a shadow section of the ledger; compare accepted
vs rejected outcomes at review milestones.
**Cost:** small — a ledger section + the close-check already evaluates
close-based rules. **Value:** the only honest way to know if our filters
(Rook vetoes, sector exclusions) are skill or luck. Their framing is
exactly right: "rejected setups outperform accepted ones → the filter is
broken."

### B6. Freeze-manifest documentation practice (theirs: `FREEZE.md`)
**What:** a single manifest per frozen spec version recording what was
built/verified, pre-freeze corrections (theirs openly documents the /95
Opportunity-scale arithmetic fix), and judgment calls — instead of
scattering them across session notes.
**Plug-in:** when we next freeze a spec version (or retrospectively for
R2 v3.1 / H3 v1), write one `FREEZE-*.md` in `hidden_files/backtests/`.
**Cost:** documentation only. **Value:** auditability; their manifest is
the reason we could review their system in an evening. Ours should be
equally reviewable.

### B7. Explicit time/bar contracts (theirs: `strategies.py` TIME CONTRACT
+ ENTRY CONTRACT; impl-spec §0, §8)
**What:** one place stating bar-timestamp conventions, completed-bars-only,
fill-timing assumptions, and early-close handling.
**Plug-in:** a short "Measurement conventions" section in the RULEBOOK
(timestamps are ET regular-session closes; fills at seen bid/ask with
quote timestamps; developing-bar vs completed-bar handling per check).
Much of this exists scattered in check prompts — consolidate it.
**Cost:** documentation. **Value:** prevents the exact class of bug that
cost us the SNDK stop this evening (close-based rule, pre-close data).

### B8. Risk-constant sizing as a *research* comparison (theirs: impl-spec §5)
**What:** `shares = floor(risk$ / risk-per-share)` with ATR-anchored stops,
instead of conviction bands.
**Plug-in:** do NOT change live sizing (Akshay chose conviction bands; the
forward tests are binding). Run it as an offline sensitivity on the frozen
R2/H3 trade ledgers: what would risk-constant sizing have done to the same
triggers?
**Cost:** one analysis script; zero impact on the live book. **Value:**
answers whether our sizing or our signals drive the economics — without
touching the experiment.

---

## 3. What we should NOT borrow and why

**N1. The intraday strategies (W1–W3, M1–M3) as signals.** They require
5-minute bars, SPY 5m for the M1 RS filter, and 78-bar complete sessions.
Our data reality is yfinance unauthenticated daily bars only, and lab scope
explicitly excludes new feeds. We cannot run them, let alone validate them.
Their 20-name mega-cap universe also doesn't match our 22-ticker semis/tech
book.

**N2. PM Edge as a drop-in system.** Its entry engine is timestamped to
5-minute bars (VWAP acceptance, ORB retest, entry location in ATR bands).
It is not runnable on daily bars, and porting it would mean rebuilding it
into something unrecognizable — at which point it isn't "their model"
anymore.

**N3. Per-candidate agent scoring (Agent A/B loop).** Our two-pass Rook
already performs the adversarial function at a fraction of the cost, and
Pixel's token budget is a binding constraint. Their pattern (two agent
invocations per candidate plus commit/reveal plumbing) is heavier machinery
for the same job. Convergent evolution — no need to import it.

**N4. Their cost model ($0.01/share/side) as a replacement.** Our 1%
punitive tier is Akshay's explicit choice and the binding falsifier runs
on it. Replacing it would void every in-flight falsifier contract. Keep
the dual-tier reporting (theirs is a useful *reference* tier, nothing more).

**N5. Regime-gated entries.** Their regime engine raises bars and blocks
entries (EVENT-RISK = 0%). We killed gating deliberately in session 2
(D1) after evidence; our regime monitor stays descriptive. Do not re-litigate
this — the lane is closed by our own research.

**N6. The 20-pattern vocabulary as signals.** Intraday-only (N1 applies).
The *annotation discipline* (deterministic, no-lookahead, n≥30) is already
ours via trigger_scan.py and the product's sample-size rule.

---

## 4. Shift assessment: "shift completely to their model?"

**Verdict: No — not now, not wholesale. The correct integration is
cross-validation, which is already the agreed shared surface.**

Reasons, in order of weight:

1. **Nothing to shift *to* yet.** Their PM Edge swing system has ~7 trading
   days of forward testing with **zero results shared**. Their intraday
   Stage 2 has **zero valid sessions**. Shifting would mean abandoning
   in-flight *binding* forward tests (R2's 15-trade falsifier, H3's 15-trade
   falsifier at 1/15) for systems with no validated edge — a direct
   violation of the falsifier discipline both labs claim to share, and of
   their own "no quiet changes" freeze rule. You don't retire a running
   experiment to adopt an unmeasured one.

2. **Technically infeasible on our data.** PM Edge's Tier-1 requirements
   (5m/15m/1h bars, session VWAP, live quote, sector ETF feeds) and the
   intraday strategies' 5m-bar contracts cannot be satisfied by our
   yfinance-unauthenticated daily-bar feed. A shift would require new data
   infrastructure the lab is explicitly scoped *not* to build (no new feeds,
   no paid subscriptions).

3. **It breaks the agreed lane split.** "We stay out of the intraday
   engine, they stay out of the daily-bar book" — adopting their swing
   system wholesale puts us inside their research engine, the exact
   duplication both sides called negative-sum. Note the nuance: PM Edge is
   a *swing* system, so it sits closer to our lane than the "intraday
   engine" label suggests — which is precisely why wholesale adoption
   would be a lane violation, not a lane complement.

4. **Our evidence is further along.** R2: 434-trade backtest + pre-registered
   point-in-time universe analysis + Watty's own independent cost-model
   replay (gross edge survived; punitive 1% costs nearly erased it; 20bps
   stayed positive). H3: 41-trade backtest + live binding forward test.
   Their side: honest process, no validated edge yet. Shifting now would be
   trading evidence for architecture.

5. **The right integration already exists.** Their README explicitly invites
   it: *"run our entries through your falsifier framework."* When PM Edge
   reaches a reviewable milestone (their own bar: 25 trades first review),
   we ingest their timestamped entries and grade them with our falsifier
   discipline — same as we did for Charlie. That is collaboration; a shift
   is substitution.

**Under what conditions would the answer change?** If PM Edge completes a
pre-registered forward window (≥25 trades, ideally 50+) with positive
net at *our* dual cost tiers on timestamped, frozen entries — and the
result survives our Rook review — then a *parallel paper track* (not a
replacement) becomes defensible. Until then: borrow the process
improvements in §2, keep our lane.

---

## 5. Suggested next steps for the parent

1. Adopt **B1–B7** (§2) — all are cheap, none disturb live specs. B4 (stop-
   first rule) and B7 (time contracts) are one-line rulebook additions;
   B5 (rejected-entry shadow) starts with the already-skipped AAPL R2 fire.
2. Run **B8** (risk-constant sizing sensitivity) offline against the frozen
   R2/H3 ledgers; report at the next session review.
3. When PM Edge hits 25 forward trades, request their timestamped entry
   log and run it through our falsifier framework per their README
   invitation — this is the concrete "compare things" deliverable.
4. Send Watty the §2 borrow list (it answers "where we can help / what
   we're taking" with specifics) — this doubles as the substantive reply
   their collaboration deserves.
5. Do not re-litigate N5 (regime gating) or N4 (cost tier); both are closed
   by prior lab decisions.

---

*Files read: all 8 in `watty-pip-lab-mirror/` (README, 3 pm-edge specs,
strategies.py, execution.py, detector.py, farm_study.py); our RULEBOOK.md,
H3 spec in `sector_entry_model_v3.md`, `session17_notes.md`,
`session21_notes.md`. No files modified.*
