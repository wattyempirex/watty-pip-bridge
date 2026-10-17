# Weekend Hunt — Track D research-mining backlog (2026-10-17)

**PAPER/RESEARCH ONLY.** Backlog of testable ideas for the joint weekend hunt with Watty's lab (sprint starts Mon Oct 19). Mined 2026-10-17 from quant papers, backtested-blog claims, and the lab's own dead-ends.

**What's already dead (do not re-propose):** short-horizon (1–10d) daily-bar momentum/breakout/mean-reversion on large caps (our 42-cell variant matrix: only 10d-hold close breakouts V1/V2/V3 work, on 4 of 6 sectors); 5-min intraday mean reversion (Watty Track B: Sharpe −6 to −15); earnings drift at short horizons (Watty: 116 variants, median Sharpe 0.05); naive regime filters (made things worse); pullback V6 (−$32,450, worst variant); contraction-break V7 (−$19,894); support-bounce v1 (shelved, n=3 < 30 guard); retail ICT/SMC concepts (Watty Track B covers). Optical + megatech excluded under all shapes.

**Ground rules for every idea below:** frozen pre-registered rules before any test; 30-bar warmup; Wilder ATR14 per vocabulary spec §2.3; costs per the lab's dual tiers (1% raw-close + 20bps realistic); no invented numbers — every cited claim names its source; [UNVERIFIED CLAIM] where I couldn't verify.

---

## Idea 1 — Overnight-leg momentum capture [FRESH]

**The claimed edge.** Lou, Polk & Skouras ("A Tug of War: Overnight Versus Intraday Expected Returns," *Review of Financial Studies*) decompose momentum profits into overnight vs intraday components and find that **100% of momentum abnormal returns accrue overnight**; the intraday component is economically and statistically insignificant. The pattern is strongest in large caps. Our V1/V2 breakouts hold close-to-close for 10 days, blindly mixing both legs. The testable question: does our breakout edge live in the overnight leg? If yes, a close→open holding strategy (enter at close, exit at next open) captures the premium while sidestepping intraday chop — or at minimum, the decomposition tells us where V1's +$14,699 actually comes from.

**Mechanism.** Investor heterogeneity: institutions prefer to trade intraday and trade *against* the momentum characteristic (rebalancing, VWAP execution), while individuals are more likely to trade at/after the open *with* momentum, and value-relevant news disproportionately arrives when the market is closed. Overnight = slow-diffusion + retail momentum; intraday = institutional fade. This is a who-trades-when story, not a price-pattern story — which is why it survives where price patterns died.

**Frozen rules (v1).** Universe: the 22-name watchlist (large-cap daily bars 2022–2026). Each evening, rank names by trailing 12–1 month return (skip most recent month, Jegadeesh-Titman convention) OR reuse the V1 breakout trigger as the entry screen. Enter top-decile/triggered names at the closing print; exit at the next morning's open print. One-night hold, rebalanced nightly. Invalidation: none beyond the nightly exit (this is a pure leg-capture). Diagnostic arm (run first, cheaper): decompose existing V1 trade P&L into overnight (close→open) vs intraday (open→close) legs and report the split before trading the leg standalone.
**Costs note:** one full round trip per night per name — the effect must survive realistic costs; the paper documents ~2%/month variation in the overnight–intraday spread, so the margin exists on paper but the cost hurdle is the entire test.

**Data needed:** daily OHLCV only (overnight return = open[t]/close[t−1] − 1; intraday = close[t]/open[t] − 1).

**Honesty tag: [FRESH].** Never decomposed in our lab. Caveat: Lou et al. is cross-sectional momentum on a broad universe; applying it to breakout entries / our 22-name watchlist is our generalization — the generalization is untested, the decomposition diagnostic is not.

---

## Idea 2 — Gap continuation vs gap fade, volume-conditioned [FRESH]

**The claimed edge.** Large overnight gaps (open vs prior close) resolve in one of two ways: informed gaps continue intraday and over subsequent days as analysts revise, while uninformed gaps (inventory, noise, thin pre-market) fade as liquidity returns. The conditioning variable — signed volume and alignment with the prior 5-day trend — separates the two regimes. This is the single-name, daily-bar version of the overnight/intraday tug-of-war in Idea 1.

**Mechanism.** Overnight = news arrival without trading; the open print aggregates it. Informed gaps (earnings, guidance, regulatory) carry fundamental content that diffuses over days (analyst revisions, institutional repositioning). Uninformed gaps carry no content and revert as market-makers lean against the imbalance. Volume signs the gap: heavy-volume gaps in the direction of the 5-day trend = institutional sponsorship; light-volume gaps against the trend = noise.

**Frozen rules (v1).** Signal at the open: gap% = open[t]/close[t−1] − 1. Trade only if |gap%| ≥ 1.5 × ATR14[t]/close[t−1] (material gap). Continuation arm: if sign(gap) == sign(close[t−1] − close[t−6]) (with-trend) AND volume[t−1] ≥ 1.25× avg20 → enter at open in gap direction, exit at close (intraday) — plus a 5d-hold variant. Fade arm: if sign(gap) != sign(prior 5d trend) AND volume[t−1] < 1.0× avg20 → enter at open against the gap, exit at close. Stop: 1.0 × ATR14 beyond the open print (structural: gap-fill failure). Test continuation and fade arms separately; the hypothesis is that the conditioning (not the gap alone) carries the edge.

**Data needed:** daily OHLCV only.

**Honesty tag: [FRESH].** Gaps never isolated as a signal in our lab. Related literature: the overnight/intraday decomposition field (Lou-Polk-Skouras; Bogousslavsky 2021 on overnight holding costs; Akbas et al. 2022 on night-to-day reversals) — our contribution is the volume×trend conditioning, which is our hypothesis, not theirs.

---

## Idea 3 — Customer→supplier lead-lag on the watchlist (Cohen–Frazzini) [FRESH]

**The claimed edge.** Cohen & Frazzini ("Economic Links and Predictable Returns," *Journal of Finance*, 2008) show that shocks to a firm's principal customers predict the supplier's returns with a lag — "customer momentum," ~18%/year long-short in their sample, surviving factor controls. Investors and sell-side analysts specialize by stock/industry and underweight public supply-chain links, so value-relevant customer news diffuses slowly into supplier prices. Our watchlist IS a supply chain: equipment (AMAT, LRCX) → foundry/memory (TSM, MU, SKHY) → fabless/design (NVDA, AMD, AVGO, QCOM, ARM) → OEMs/platforms (AAPL, MSFT). The chain is hand-mappable and frozen pre-test.

**Mechanism.** Limited attention + analyst specialization: when NVDA guides capex up, that is immediately value-relevant for TSM (its foundry) and AMAT/LRCX (its equipment chain), but the analysts covering TSM/AMAT are not the ones on the NVDA call. Prices adjust over days/weeks as the implication diffuses. This is an information-diffusion mechanism, completely orthogonal to every price-pattern shape we tested.

**Frozen rules (v1).** Frozen directed pair map (customer → supplier), e.g.: NVDA→TSM, AAPL→QCOM, AAPL→AVGO, MU→AMAT, MU→LRCX, TSM→AMAT, TSM→LRCX, INTC→AMAT, AMD→TSM, MSFT→NVDA (cloud capex → accelerators). Signal: customer 5-day return ≥ +5% idiosyncratic (vs SPY) → long the supplier at next close, 15-session hold, stop = 2× ATR14. Mirror for negative shocks is long-only-incompatible; test the long leg only, or test shorts as a diagnostic. Continuous variant: supplier position score = customer trailing 5d idiosyncratic return, rebalanced weekly.
**Pair-map discipline:** the map is frozen BEFORE the first backtest, from public supply-chain knowledge (company 10-Ks, investor presentations) — no peeking at which pairs "worked."

**Data needed:** daily closes (+ SPY for the idiosyncratic leg); the frozen pair map (hand-built, documented).

**Honesty tag: [FRESH].** Cross-asset lead-lag never tested in our lab. Caveats: Cohen-Frazzini is monthly, long-short, broad-universe; our translation (daily bars, long-only, 22 names, 15d holds) is ours and untested. A 2023 replication (arXiv:2301.11394) confirms the effect persists post-discovery in broad universes — cited as support, not proof for our universe.

---

## Idea 4 — 52-week-high nearness (George–Hwang) [FRESH]

**The claimed edge.** George & Hwang ("The 52-Week High and Momentum Investing," *Journal of Finance*, 2004) find that nearness to the 52-week high — current price divided by the highest price of the past year — dominates past returns in predicting momentum profits, and crucially that momentum measured by 52-week-high proximity does NOT reverse (unlike Jegadeesh-Titman momentum). Our V1 uses a 20-day breakout anchor; the 52-week anchor is a different reference point operating on a different behavioral mechanism.

**Mechanism.** Anchoring-and-adjustment (Tversky & Kahneman): investors use the 52-week high as a salient reference price and are reluctant to bid above it even when news warrants it — underreaction near highs, drift as news prevails. Bhootra & Hur (2013) add that *recency* of the 52-week high matters: stocks that hit their high recently outperform those that hit it long ago (recency bias layered on anchoring). [UNVERIFIED CLAIM: I could not pull the Bhootra-Hur paper directly; the recency result is reported in a secondary review of the 52-week-high literature.]

**Frozen rules (v1).** nearness[t] = close[t] / max(high[t−252..t−1]). Monthly rebalance: long the top-tercile nearness names (nearness ≥ 0.90 required for entry), 30-session hold, stop = 2× ATR14. Recency variant: among high-nearness names, prefer those whose 252d high occurred within the last 63 sessions. This is a 1–2 month hold strategy — deliberately longer than everything we tested.

**Data needed:** daily OHLCV with 252-session history (data_4y covers it after warmup).

**Honesty tag: [FRESH].** 252-day anchor never tested in our lab. Disclosed overlap: Watty's Track A tests 12-1 momentum; 52-week-high is a distinct formulation (nearness ratio vs past return, different mechanism, no-reversal property) but correlated — report the correlation, don't double-count a win.

---

## Idea 5 — Volatility-expansion-filtered breakout (V1 + ATR gate) [VARIANT of V1]

**The claimed edge.** V1/V2 work (+$14,699 / +$15,584 over 4y), and our risk-constant study showed the edge concentrates in wide-extension breakouts (+1.75R wide tercile vs −0.32R middle). This variant adds one gate: take the V1 breakout ONLY when volatility is expanding into the breakout — ATR14 rising or the breakout day's range materially above normal. Breakouts on expanding volatility = genuine supply absorption with sponsorship; breakouts on dead volatility = low-conviction drift that fails on the first pullback.

**Mechanism.** Volatility is the footprint of disagreement being resolved by volume. A breakout that expands range says new information is being priced by committed participants; a breakout on a narrow-range day says the level was crossed by indifference. The filter keeps the proven entry shape and cuts the marginal trades — the ones most likely to be the 55–60% losers in V1's ~40% win rate.

**Frozen rules (v1).** V1 trigger exactly (20D close breakout ≥ 1.010×, vol ≥ 1.25× avg20) PLUS: ATR14[t] / ATR14[t−5] ≥ 1.10 (volatility expanding into the signal) OR range[t] ≥ 1.5 × ATR14[t] (breakout-day expansion). Same 10d hold, same structural stop (broken reference level), same universe and sector filters. One gate, no other changes — this is a clean ablation of V1.

**Data needed:** daily OHLCV only.

**Honesty tag: [VARIANT] — of V1, the lab's working shape.** Explicitly a filter on a proven trigger, not a new shape. Risk: fewer trades (V1 has 434; the gate will cut it) — pre-register a minimum-trade guard (≥100 trades) so we don't grade noise.

---

## Idea 6 — First-retest entry after breakout (resistance→support flip) [VARIANT of V1]

**The claimed edge.** Instead of chasing the V1 breakout print, wait for the first pullback to the broken level: old resistance becomes new support. The retest entry gets a tighter structural stop (just under the level) and better reward/risk than the breakout-chase entry, at the cost of missing breakouts that never look back. This is the standard professional treatment of the breakout shape we already trade.

**Mechanism.** The breakout triggers momentum algos and traps late shorts; the first retest shakes weak hands while institutions add to the position they started on the breakout. The level holds because of clustered stop-loss orders beneath it and anchored limit-order books at the round reference price. When the retest holds and turns, the resumption carries the "unfinished business" of the interrupted move.

**Frozen rules (v1).** V1 breakout fires on day 0 (record C20max). Then: wait up to 10 sessions for a daily close inside [C20max × 0.98, C20max × 1.02] (the retest band). Enter at the first such close. Stop: C20max × 0.98 − 0.25 × ATR14 (under the band, thesis = level failed). Target: measured move — base height (C20max − min(low, 20d before breakout)) projected upward; exit at target, stop, or 10 sessions after entry, whichever first. If no touch within 10 sessions, the setup expires untraded (no chase).
**Convergence note:** Watty's v0.2 spec independently lists "resistance→support flip" as a support anchor and our support-bounce memo independently derived reclaim mechanics — convergent, not copied. Their backtest of the full bounce mechanism shelved at n=3; this variant differs by attaching to the PROVEN V1 breakout rather than standalone support levels.

**Data needed:** daily OHLCV only.

**Honesty tag: [VARIANT] — of V1 (entry-timing variant, same underlying phenomenon).**

---

## Idea 7 — Post-shock drift at 20–40 sessions (H3 long-horizon) [VARIANT of H3]

**The claimed edge.** H3 (idiosyncratic shock reversal) was tested at short horizons: 41-trade backtest +$7,075.59, forward paper 1/15 (−$120.48). The classic post-event drift literature (Bernard & Thomas, "Post-Earnings-Announcement Drift: Delayed Price Response or Risk Premium?", *Journal of Accounting Research*, 1989) finds drift persists ~60 trading sessions after the event. If H3's mechanism (overreaction → forced selling → slow correction) is real, the correction may need weeks, not days — and the short-horizon test may have measured noise around a slower signal.

**Mechanism.** Sharp idiosyncratic selloffs: day 1–2 = forced selling, stop cascades, headline algos (overshoot); days 3–40 = analyst revisions, value buyers scaling in, shorts covering — the digestion cycle plays out over weeks. H3's 10d-ish window may simply be too short for the mechanism it posits.

**Frozen rules (v1).** H3 trigger exactly (large idiosyncratic down move vs cohort/SPY — reuse the frozen H3 definition) with holds of 20 and 40 sessions (two pre-registered arms, not a tuned choice). Same structural stop logic. Report alongside the original H3 window so the horizon is the only moving part.

**Data needed:** daily closes + SPY (same as H3).

**Honesty tag: [VARIANT] — of H3, with the longer hold as the new hypothesis.** Stated plainly: this is NOT a rescue of H3's forward record (1/15); the forward falsifier keeps running independently. If the 20/40d arms fail too, the shock-reversal mechanism is dead at all tested horizons.

---

## Idea 8 — High-beta drift after large market moves (Hong–Stein diffusion) [FRESH]

**The claimed edge.** After a large SPY move, high-beta single names drift in the same direction over the next 5–20 sessions. Hong & Stein ("A Unified Theory of Underreaction, Momentum Trading, and Overreaction in Asset Markets," *Journal of Finance*, 1999) model gradual diffusion of private information: news travels slowly across investor classes, and momentum traders amplify the drift. The tradable surface: market-wide news is priced into the index first; single-name analysts are slow to update; high-beta names have the most catch-up.

**Mechanism.** Information diffusion is gradual, not instantaneous — especially for market-wide news that has to be translated into single-name earnings implications by specialized analysts. High-beta names mechanically have larger pending adjustments. This is a cross-sectional diffusion trade, not a price pattern: the signal is (market shock) × (name beta), both measured, not chart-read.

**Frozen rules (v1).** If |SPY 5d return| ≥ 2%: rank watchlist by 60d beta vs SPY; go long the top-5 beta names in the direction of the SPY move at next close; 15-session hold; stop = 2× ATR14. If |SPY 5d| < 2%: no position (the diffusion trade needs a shock worth diffusing). Re-evaluate weekly.

**Data needed:** daily closes + SPY (beta from 60d regression).

**Honesty tag: [FRESH].** Never tested in our lab. Note: needs a real market shock to fire — in quiet regimes this strategy holds nothing, which is a feature (selectivity), not a bug.

---

## Idea 9 — V1 + pre-breakout volatility-compression filter [VARIANT of V1]

**The claimed edge.** Multi-week volatility compression (narrowing daily ranges) before a breakout marks disagreement resolving and positioning going quiet — the calm before repricing. Filter V1 breakouts to only those preceded by compressed volatility: the breakout then represents genuine news arrival against a coiled spring, not drift through an indifferent level.

**Mechanism.** Range contraction = declining disagreement + withdrawing liquidity provision; when real information arrives into a compressed market, the price move is larger and more persistent (there is no overhang of stale limit orders to absorb it). This is a setup filter on the proven breakout, not a standalone contraction-breakout shape.

**Frozen rules (v1).** V1 trigger exactly, PLUS in the 10 sessions before the breakout: mean(range, 5) ≤ 0.85 × mean(range, 20) on at least 3 of those 10 sessions (compression present, not necessarily on the signal day). Same 10d hold, same structural stop.
**Explicit distinction from dead V7:** V7 (−$19,894) was contraction + price-breakout-above-10D-high at 5d holds with no volume filter — a different shape, different hold, different anchor. This variant keeps V1's exact trigger (20D close, 1.010×, volume filter, 10d hold) and adds compression only as a pre-condition. If this fails, it fails as a V1 filter, and V7's verdict is untouched.

**Data needed:** daily OHLCV only.

**Honesty tag: [VARIANT] — of V1 (pre-condition filter).** The V7-caution is stated in the rules so no one confuses the two.

---

## Idea 10 — Turn-of-the-month seasonality [LONG-SHOT]

**The claimed edge.** Ariel ("A Monthly Effect in Stock Returns," *Journal of Financial Economics*, 1987) and Lakonishok & Smidt document that a disproportionate share of monthly returns accrues around the turn of the month (last + first few trading days) — attributed to clustered institutional cash flows (payrolls, pension contributions, window-dressing flows).

**Mechanism.** Predictable liquidity demand: month-end inflows must be put to work, creating systematic buying pressure concentrated in a few sessions. Calendar-based, not price-based — orthogonal to everything we trade.

**Frozen rules (v1).** Long the watchlist (equal-weight, or SPY as the vehicle) from the close of the last trading day of the month through the close of the 3rd trading day of the new month; flat otherwise. 4-session holding window, monthly.

**Data needed:** daily closes + calendar.

**Honesty tag: [LONG-SHOT].** Honest assessment: this is one of the most-published calendar effects in finance and large-cap arbitrage has had 35+ years to kill it; Watty's "conventional space is exhausted" verdict applies here with force. Included because it's cheap to test (one rule, monthly) and a clean kill is itself a deliverable ("the kills are the deliverable").

---

## Idea 11 — Options skew / IV-rank signals [LONG-SHOT, needs data we don't have]

**The claimed edge.** Informed traders prefer options (leverage, defined risk); heavy put-skew buying or extreme implied-volatility rank can precede or predict underlying moves. Two sub-hypotheses: (a) put/call skew extremes mark informed hedging ahead of downside events; (b) IV rank (current IV vs 1-year range) mean-reverts and conditions directional entries — buy breakouts only when IV rank is low (cheap optionality, complacent positioning).

**Mechanism.** Options market as the venue of choice for informed/leveraged flow; skew as the footprint of directional hedging demand.

**Frozen rules (v1).** [NOT FORMALIZABLE YET — no options data in the lab.] Sketch for when data exists: 25-delta put/call skew percentile (63d lookback); signal when skew > 90th percentile (defensive → avoid longs / tighten stops); IV rank = (IV − 52w low)/(52w high − 52w low); V1 breakouts only when IV rank < 0.5.

**Data needed:** daily options chains (implied vols by delta, or at minimum 30d ATM IV + 25-delta skew) for the watchlist. We do not have this. yfinance has some options data (unverified quality/delay).

**Honesty tag: [LONG-SHOT].** Cannot test with current lab data. Included so the backlog records the data gap honestly rather than pretending options don't exist.

---

## Idea 12 — Measured-move exits for V1 (exit-side improvement) [VARIANT]

**The claimed edge.** V1's exit is a fixed 10-day hold — the matrix proved the 10d hold beats 5d everywhere, but a fixed time exit is still crude. Classical technical analysis (Edwards & Magee; bulk of retail/pro literature) uses measured moves: project the height of the base (breakout level minus the lowest low of the formation) upward from the breakout point as the minimum objective. If breakouts genuinely resolve toward measured objectives, a structure-based exit beats a clock-based exit on reward/risk.

**Mechanism.** The base height measures the energy of the resolved disagreement: the longer/taller the base, the more supply was absorbed, the further the resumption travels before meeting new supply. Time exits cut winners at arbitrary points; measured objectives let structure decide.

**Frozen rules (v1).** V1 entry exactly. On entry: objective = C20max + (C20max − min(low, 20 sessions before breakout)). Exit at the first close ≥ objective, or stop (broken level), or 20 sessions (time backstop — twice the current hold, so the structure gets room). Compare against V1's fixed-10d exit on identical entries: the entry set is frozen, only the exit rule changes — a pure exit ablation.

**Data needed:** daily OHLCV only.

**Honesty tag: [VARIANT] — exit-side variant of V1.** Note: measured-move objectives are textbook TA with thin academic backing — the edge claim here is modest (better exits on a proven entry), and the test is designed to kill it cheaply if it's folklore.

---

## Appendix: what this backlog deliberately excludes (and why)

- **12-1 / 6-1 cross-sectional momentum, short-term reversal, betting-against-beta, quality-minus-junk, idiosyncratic vol, MAX lottery** — Watty's Track A factor zoo covers these; duplicating wastes the weekend. Our Idea 4 notes the 52-week-high overlap explicitly.
- **ICT/SMC, Connors RSI(2), turtle breakouts, opening-range variants** — Watty's Track B covers; their kills are their deliverable.
- **Anything needing earnings dates** — our earnings lookup is degraded; Ideas 3 and 7 use price-shock proxies instead of event dates, honestly.
- **Pairs/relative-value with a short leg** — our paper book is long-only; Ideas 3 and 8 are framed long-only with short legs as diagnostics only.
- **Intraday (5-min) shapes** — Watty Track B: Sharpe −6 to −15. Dead.

## Suggested forge order (cheapest kills first)

1. Idea 1 diagnostic arm (decompose V1 P&L into overnight/intraday) — zero new trades, pure accounting on existing results.
2. Idea 5 (one added gate on V1) — single ablation, ≥100-trade guard.
3. Idea 9 (one pre-condition on V1) — single ablation, same guard.
4. Idea 6 (retest entry) — needs new backtest but reuses V1 trigger code.
5. Idea 12 (exit ablation on frozen V1 entries) — pure exit comparison.
6. Ideas 2, 3, 4, 8 (new signals) — full new backtests, in that order of mechanism strength.
7. Idea 7 (H3 long-horizon) — only after 1–6; do not let it become H3 life support.
8. Ideas 10, 11 — background/testability permitting.

*Backlog ends. PAPER/RESEARCH only. Nothing here is a signal; everything here is a candidate for the forge.*

---

## Appendix: non-daily-bar dimension per idea (added 2026-10-17 per Watty's ask)

What makes each idea NOT just another daily-bar price pattern — tagged by DATA SOURCE, HORIZON, or MECHANISM:

1. Overnight-leg capture — MECHANISM (who-trades-when: institutional intraday fade vs retail overnight momentum) + HORIZON (single-night holds)
2. Gap continuation/fade — MECHANISM (informed vs uninformed gaps, signed by volume × trend alignment)
3. Customer→supplier lead-lag — DATA SOURCE (hand-mapped supply-chain graph) + MECHANISM (analyst inattention/specialization)
4. 52-week-high nearness — MECHANISM (anchoring-and-adjustment) + HORIZON (252d anchor, 30d holds)
5. Vol-expansion-filtered V1 — MECHANISM (volatility as disagreement-resolution footprint); closest to the daily-bar zoo of the set — acknowledged
6. First-retest entry — MECHANISM (order-flow at flipped resistance→support levels); close to the zoo, acknowledged
7. Post-shock drift 20–40d — HORIZON (20–40 sessions vs the 10d everything else tested)
8. High-beta drift after SPY shocks — DATA SOURCE (market-wide shock × 60d beta) + MECHANISM (Hong–Stein gradual diffusion)
9. Vol-compression pre-filter — MECHANISM (liquidity withdrawal before news arrival); close to the zoo, acknowledged
10. Turn-of-the-month — MECHANISM (calendar liquidity flows: payrolls, pension contributions) + HORIZON (monthly calendar window)
11. Options skew / IV-rank — DATA SOURCE (options market — needs data we don't have; recorded as gap)
12. Measured-move exits — MECHANISM (structure-based exit vs clock-based exit; exit-side only)

Ideas 5, 6, 9 are flagged honestly as the most daily-bar-adjacent — they're filters/variants on the one proven shape, not new mechanisms. If the weekend is about new ground, ideas 1–4, 7–8, 10–11 are the frontier.
