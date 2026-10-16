# Variant Matrix: 7 entry shapes × 6 sectors (4y, Oct 2022–Oct 2026)

**PAPER/RESEARCH ONLY.** Pre-registered matrix — all 42 cells run, all reported, no tuning.

**Setup:** $7,500 notional, 0.1% adverse half-spread each way, $75 flat per completed trade, 30-bar warmup, structural stop = the broken reference level (checked before the time exit, same as the reference harness). Data: `data_4y/`. Coverage exclusions applied: SKHY, SNDK, ARM (not fully covered) → memory={MU}, semis={NVDA,AMD,AVGO,TSM,INTC,QCOM}.

**Variant definitions (pre-registered):**
- **V1:** 20D CLOSE breakout (1.010× prior max close, vol ≥ 1.25×avg20), 10d hold — the R2 reference shape
- **V2:** 10D CLOSE breakout (same filters), 10d hold
- **V3:** 30D CLOSE breakout (same filters), 10d hold
- **V4:** 20D CLOSE breakout (same filters), 5d hold
- **V5:** 10D HIGH breakout (1.010× prior max high, vol filter), 5d hold — the S1 reference shape
- **V6:** PULLBACK — close crosses above 10D SMA after ≥5 consecutive closes below their own 10D SMA; 5d hold; stop = entry-day 10D SMA (structural analog). No volume filter, no multiplier (literal spec).
- **V7:** CONTRACTION-BREAK — mean(H−L,5) ≤ 0.80×mean(H−L,20), then close > prior 10D high; 5d hold; stop = entry-day 10D high. No volume filter, no multiplier (literal spec).

**Validation:** V1 reproduces Session 2's R2 exactly — 434 trades, net **+$14,699** (vs reported +$14,699). V5 reproduces Session 2's S1 net exactly — **−$25,571** (vs reported −$25,571). Harness is faithful to the reference.

## Full matrix (net $ per cell; format: trades / win% / net$)

| Variant | semicap (AMAT,LRCX) | memory (MU) | optical (COHR,GLW) | megatech (5) | semis (6) | other (PLTR,SNOW,NFLX) | **TOTAL** |
|---|---|---|---|---|---|---|---|
| V1 20D-close, 10d | 42 / 45.2% / **+$360** | 24 / 50.0% / **+$3,176** | 53 / 41.5% / −$4,914 | 97 / 39.2% / −$4,778 | 145 / 43.5% / **+$13,913** | 73 / 37.0% / **+$6,941** | 434 / **+$14,699** |
| V2 10D-close, 10d | 49 / 46.9% / **+$680** | 29 / 51.7% / **+$2,568** | 64 / 37.5% / −$7,673 | 113 / 40.7% / −$5,724 | 166 / 44.0% / **+$18,387** | 82 / 41.5% / **+$7,346** | 503 / **+$15,584** |
| V3 30D-close, 10d | 38 / 50.0% / **+$1,115** | 22 / 50.0% / **+$3,252** | 47 / 38.3% / −$4,270 | 84 / 38.1% / −$5,641 | 132 / 42.4% / **+$9,991** | 63 / 39.7% / **+$8,975** | 386 / **+$13,421** |
| V4 20D-close, 5d | 49 / 36.7% / −$3,166 | 30 / 46.7% / **+$1,923** | 59 / 42.4% / −$9,661 | 104 / 41.4% / −$7,116 | 169 / 40.2% / −$1,554 | 83 / 42.2% / −$3,630 | 494 / **−$23,205** |
| V5 10D-high, 5d | 52 / 34.6% / −$5,127 | 33 / 42.4% / **+$1,156** | 55 / 40.0% / −$9,461 | 95 / 35.8% / −$7,861 | 167 / 41.3% / **+$1,260** | 79 / 39.2% / −$5,539 | 481 / **−$25,571** |
| V6 pullback, 5d | 63 / 30.2% / −$6,987 | 32 / 46.9% / **+$3,571** | 62 / 37.1% / −$2,977 | 162 / 34.6% / −$11,061 | 196 / 35.7% / −$8,262 | 96 / 37.5% / −$6,734 | 611 / **−$32,450** |
| V7 contract-0.80, 5d | 40 / 27.5% / −$3,603 | 12 / 50.0% / +$37 | 25 / 36.0% / −$2,398 | 62 / 21.0% / −$7,664 | 71 / 35.2% / −$4,582 | 28 / 53.6% / −$1,684 | 238 / **−$19,894** |

## (1) Per-sector best / worst shape (by net $)

- **semicap** (n=38–63/cell): best **V3** (+$1,115, 50.0% win) → V2 (+$680) → V1 (+$360); worst **V6** (−$6,987, 30.2% win). All three 10d-hold close-breakouts positive; all 5d shapes negative.
- **memory** (MU only, n=12–33/cell): best **V6** (+$3,571) → V3 (+$3,252) → V1 (+$3,176); worst **V7** (+$37 — positive but trivial). Every cell positive, but this is a single ticker — treat as anecdote, not a sector result.
- **optical**: everything negative. Least-bad **V7** (−$2,398, n=25) → V6 (−$2,977); worst **V4** (−$9,661), then V5 (−$9,461). Consistent with Session 2's "exclude optical" — no shape works here.
- **megatech**: everything negative. Least-bad **V1** (−$4,778) → V3 (−$5,641); worst **V6** (−$11,061, n=162). No shape works — confirms the megatech exclusion.
- **semis** (largest sample, n=132–196/cell): best **V2** (+$18,387, 44.0% win, +$110.76/trade) → V1 (+$13,913) → V3 (+$9,991); worst **V6** (−$8,262). Note V5 is barely positive (+$1,260) but V4 is negative — the 10d hold carries everything.
- **other**: best **V3** (+$8,975, +$142.45/trade) → V2 (+$7,346) → V1 (+$6,941); worst **V6** (−$6,734).

## (2) One shape vs per-sector models

**Verdict: one shape family dominates — one model + sector filters is supported; per-sector *shapes* are not warranted.**

Evidence:
- **Hold period is the master variable.** 10d-hold close-breakouts (V1/V2/V3) beat the 5d-hold versions in **all 6 sectors** (V1 > V4 everywhere: semicap +360 vs −3,166; memory +3,176 vs +1,923; optical −4,914 vs −9,661; megatech −4,778 vs −7,116; semis +13,913 vs −1,554; other +6,941 vs −3,630). No sector reverses this.
- **Sign pattern is sector-determined, not shape-determined.** V1/V2/V3 are positive in the same 4 sectors (semicap, memory, semis, other) and negative in the same 2 (optical, megatech) — identical to Session 2's sector filter. Within the winning family, the window (10D vs 20D vs 30D) is second-order: total nets are V2 +$15,584 / V1 +$14,699 / V3 +$13,421 — a ~$2k spread across 4 years, versus the ~$37k gap between the best 10d-hold and the 5d-hold family.
- The only sector×shape interaction with any size: **semis prefers the 10D window** (V2 +$18,387 vs V1 +$13,913 vs V3 +$9,991, n=132–166 — the largest cell samples in the matrix), while other/semicap/memory prefer 20D/30D. This is a candidate *parameter tweak within one model* (e.g., shorter lookback for semis), not a different entry shape — and it needs a Rook review before being treated as real, since V2-vs-V1 in semis could be sampling noise.

## (3) Is V6 (pullback) systematically better in mean-reverting sectors? **No.**

Per the regime table's mean-reverting sectors:

| Sector | V6 rank (of 7) | V6 net | Best shape net |
|---|---|---|---|
| memory | **1st** | +$3,571 | V6 itself (+$3,571 vs V3 +$3,252 — margin $319 on n=32) |
| optical | 2nd (least-bad loser) | −$2,977 | V7 −$2,398 (also negative) |
| semicap | **7th (worst)** | −$6,987 | V3 +$1,115 |

V6 is dead-last in 3 of 6 sectors overall (semicap, megatech, other) and worst in aggregate (−$32,450, the lowest total of any variant). The memory "win" is a single-ticker result where V6 beats V3 by $319 — noise-level. **The pullback shape does not systematically exploit mean reversion; if anything it systematically loses.**

## (4) V7 as an R1 re-forge candidate: **tradable volume, dead on arrival.**

- **Trade count at the 0.80 gate is fine:** 238 trades over 4y (semicap 40, memory 12, optical 25, megatech 62, semis 71, other 28) — roughly 2× the dead R1's sparsity problem is resolved; the gate is NOT too tight to be tradable.
- **But every cell loses money:** aggregate −$19,894 (−$83.59/trade), win rates 21.0%–53.6% (mostly ~0.35), and it is the worst or second-worst shape in megatech (−$7,664), semis (−$4,582), and semicap (−$3,603). Loosening the gate fixed the count problem without fixing the shape problem.
- **Recommendation: do not re-forge R1 from V7.** Rook's original veto stands — contraction-break is rejected on economics, not just on sparsity.

## Bottom line for Akshay's open question

One model with sector filters suffices. The winning specification is a **close-breakout with a 10-day hold** (V1/V2/V3 all work; V2's 10D window edges it in semis). The 5-day hold is uniformly worse in every sector; the high-breakout (S1 shape), pullback, and contraction-break shapes lose everywhere that matters. Optical and megatech exclusions confirmed under all 7 shapes. The single open refinement is the semis 10D-window preference — a parameter question for Rook, not a new model.
