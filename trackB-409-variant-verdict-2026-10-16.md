# Track B — Massive Strategy Search: Final Report
**Date:** 2026-10-16 · **Track:** B (compute) of the Working Indicator Push
**Disposition:** `trackB-disposition.md` (bootstrap-t/Holm demoted to diagnostic-only)
**Manifest:** `manifests/MANIFEST.json` (sha16=71642d1517ab5e4c) · **Caliper:** NEEDS REPAIR → 7/7 fatal findings repaired

> Research/paper only. No brokerage, no live orders. Sealed prospective holdout
> 2026-11-02→2027-10-29 never touched.

## 0. VERDICT

**Variants run:** 409 (240 C1 configs + 116 C2 + 40 regime + 13 C3)
**Cleared ALL economic gates:** **0**
**Promoted to forward paper:** **0** (nothing qualified; no goalpost-moving)

The search was executed faithfully. Nothing works. SPY beats 408 of 409 variants on a risk-adjusted basis. The honest conclusion is that none of the 20 tournament families, the 116-variant earnings-drift deep dive, regime conditioning, or the 13 intraday families contain a "working" indicator under the binding gates.

## 1. Results by cohort

### Cohort 1 (primary): 240 configs, 20 tuning policies
- **Policies clearing ALL gates: 0/20.** Every policy hit CASH_FOLD in at least one outer fold: in the inner quarters, no config achieved Sharpe>0 in all 4 quarters. The tuning mechanism correctly refused to deploy.
- **Configs clearing ALL gates: 0/240.** Best: S14-h10-b005-s2 (Sharpe 0.89, fails 5 gates).
- Inner-quarter analysis: in O2/O3 dev windows (2023), the best configs had min-quarterly-Sharpe of −0.70 to −3.22 — the strategies lost money consistently.

### Cohort 2 (earnings-drift deep grid): 116 variants
- **Cleared ALL: 0/116.** Best: C2-10-020080-l1-loud-e-1-snone (Sharpe 0.65).
- Median Sharpe: 0.052 (zero). **Sharpe−SPY > 0: 0/116.** The earnings-drift hypothesis is dead under these gates.

### Regime conditioning: 40 variants
- **Cleared ALL: 0/40.** Best: RG-V-S10 (Sharpe 0.29). Median Sharpe: −0.18 — regime filters made things worse.

### Cohort 3 (intraday, 5-min): 13 families
- **Cleared ALL: 0/13.**
- Intraday families (ID-01..04) were disastrous (Sharpe −6 to −15): 5-min mean-reversion doesn't overcome 10bps costs; win rates ~29%.
- Swing translations (ID-05..09): best ID-06 at 0.70, none near 1.25.

## 2. Global top-10 (all 409 variants)

| # | Cohort | Variant | Sharpe | MaxDD | Trades | Sharpe−SPY | Intercept |
|---|--------|---------|--------|-------|--------|------------|-----------|
| 1 | C1 | S14-h10-b005-s2 | 0.89 | −0.17 | 713 | +0.13 | 7.4% |
| 2 | C1 | S02-h10-b005-s2 | 0.75 | −0.11 | 613 | −0.00 | 3.2% |
| 3 | C1 | S14-h05-b005-s2 | 0.72 | −0.13 | 893 | −0.04 | 4.6% |
| 4 | C1 | S18-h10-b000-s2 | 0.68 | −0.23 | 1204 | −0.08 | 3.8% |
| 5 | C1 | S07-h10-b005-s1 | 0.67 | −0.28 | 1699 | −0.09 | 3.0% |
| 6 | C1 | S15-h05-b000-s1 | 0.66 | −0.32 | 2958 | −0.09 | 3.1% |
| 7 | C2 | C2-10-020080-l1-loud-e-1-snone | 0.65 | −0.10 | 359 | −0.11 | 2.1% |
| 8 | C1 | S14-h05-b000-s2 | 0.64 | −0.09 | 709 | −0.11 | 3.3% |
| 9 | C1 | S18-h10-b005-s1 | 0.62 | −0.21 | 2109 | −0.13 | 2.4% |
| 10 | C2 | C2-05-020080-l2-band-e-5-snone | 0.62 | −0.11 | 826 | −0.14 | 1.9% |

Full ranking: `results/global_ranking.pkl` (409 rows).

## 3. Benchmark honesty
- **SPY Sharpe−SPY > 0: 1/409** (only S14-h10-b005-s2, at +0.13 — and it fails 5 other gates).
- If SPY beats everything again: **it did.** Buy-and-hold SPY dominates this entire search on a risk-adjusted basis.

## 4. Why nothing cleared (diagnosis)
1. **Inconsistency across time:** min-fold Sharpe negative for nearly all top variants. What works in 2022 fails in 2023.
2. **Costs dominate intraday:** 10bps/side erases the thin intraday edge (mean trade −0.20%, win rate 29%).
3. **Tuning can't find stability:** the nested procedure correctly identifies that no configuration is robust — this is the system working, not failing.
4. **Earnings drift is noise:** 116 variants, median Sharpe 0.05, none beats SPY.

## 5. Stress & bootstrap (E members)
- **E sets are empty** (C1: 0, C2: 0, regime: 0, C3: 0). Per the architecture, stress replays and bootstrap-t run on E members only. With no E members, both are moot. (Running them on non-qualifiers would be goalpost-moving.)

## 6. Data gaps & spend proposals (PROPOSE ONLY)
### G1. Delisted PIT member bars (76 names) — RESIDUAL BIAS
- Missing: daily OHLCV for delisted S&P 500 members 2020→2026. Free sources exhausted.
- Candidates: **Norgate Platinum** ($630/12mo; delisted back to 1990 — minimum tier); **Sharadar SEP** (tens of $/mo; 1998→ incl. delisted); **Polygon Developer** ($79/mo; partial delisted coverage).
- Recommendation: **NO SPEND** — with zero qualifiers, closing the survivorship gap wouldn't change the verdict. Revisit only if a future search produces a nominee.

### G2. 5-min coverage gaps (14 tickers partial/missing)
- 558/572 tickers (97.5%). Missing: symbology edge cases (BRK.B/BF.B), late IPOs (RDDT), rate-limit gaps.
- Not blocking. No spend proposed.

### G3. Pre-2022 intraday depth
- Not blocking (2022+ window adequate). No spend proposed.

## 7. Caliper methodology verdict
One-shot (gpt-6-astra, high reasoning): **NEEDS REPAIR**, 7 FATAL findings (F1 no prospective gate; F2 false-promotion risk; F3 holdout seal; F4 opening portfolio not constructible; F5 unadjusted accounting; F6 cohort 2/3 timing; F7 nomination unit). **All 7 repaired.** Demotion of bootstrap-t/Holm UPHELD as correct. Full review: `caliper/methodology-review-2026-10-16.md`.

## 8. Prospective protocol
Frozen (`prospective-protocol.md`): PASS/FAIL/INCONCLUSIVE; INCONCLUSIVE on <60 trades; no statistical confirmation ever; false-promotion risk UNQUANTIFIED; evaluator stub sha-pinned, must not run before 2027-10-29. **No nominees** — nothing to freeze by the 2026-10-30 deadline.

## 9. Files
- Disposition, manifests, harness (15 fixture groups PASS): `trackB/`
- Results: `results/cohort1/`, `results/cohort2/`, `results/regime/`, `results/cohort3/`, `results/global_ranking.pkl`
- This report: `trackB-report.md`
