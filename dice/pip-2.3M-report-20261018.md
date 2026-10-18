# Pip Lab Alpha-Mine Report — 2.3M Dice (2026-10-18)

**Run:** weekend_hunt_alphamine.py | Seeds [50,000,000, 52,300,000), all 2,300,000 unique, zero overlap with Watty's [0, 50M) fence.
**Universe:** 22-name watchlist (SPY excluded from sleeves), daily bars, IS 2023-01-01 → 2024-12-31.
**Protocol:** random expression trees (depth ≤ 4, ≥2 distinct inputs, lookbacks {3,5,10,20,60}); operators: rank, delay, ts_rank, ts_corr/ts_cov, delta, signed_power, scale, ts_min/max, ts_argmin/max, decay_linear, rolling stats, arithmetic. NO indneutralize. Walk-forward 4 folds (6-month test blocks), 3d forwards, next-open entry, 5bps/side, 5 sleeves (quintile long-short, daily rebalance). Per-alpha: annualized Sharpe of pooled OOS daily net P&L; NaN if <100 OOS obs or zero variance.
**Compute:** 2 workers, checkpoint every 50k, survived 4 runtime restarts via checkpoint/resume with zero loss.

## Sharpe distribution (2,266,888 valid; 33,112 degenerate NaN = 1.4%)

| stat | value |
|---|---|
| mean | -1.0947 |
| std | 0.9991 |
| skew | 0.3154 |
| kurtosis | 2.4041 |
| min / max | -4.855 / 2.956 |
| p50 / p90 / p99 / p99.9 / p99.99 / p99.999 | -1.146 / 0.333 / 1.079 / 1.658 / 2.106 / 2.522 |

**Raw Sharpe thresholds:** > 2.0: 390 | > 3.0: 0 | > 4.6: 0

Note: mean -1.09 — random alphas are systematically negative on this universe (costs + structure). The null is not centered at zero here.

## Deflated Sharpe Ratio (K = 2,300,000, Bailey & Lopez de Prado 2014)

- Trial variance V = 0.9981 → expected max Sharpe under null = **5.025**
- **DSR ≥ 0.99: 0** | DSR ≥ 0.95: 0 | DSR ≥ 0.90: 0
- Max DSR across all 2.3M: 2.8e-114 (best raw Sharpe 2.956, seed 50195636, n_obs 378)

## Corrected top-20 (by DSR)

| seed | raw Sharpe | n_obs | DSR |
|---|---|---|---|
| 50195636 | 2.956 | 378 | 2.8e-114 |
| 51740903 | 2.909 | 378 | 1.2e-122 |
| 50931756 | 2.879 | 378 | 3.6e-128 |
| 50736038 | 2.861 | 378 | 1.1e-131 |
| 50017272 | 2.761 | 378 | 4.6e-152 |
| 51635347 | 2.743 | 378 | 3.0e-156 |
| 50824973 | 2.734 | 378 | 3.4e-158 |
| 51707290 | 2.707 | 378 | 2.7e-164 |
| 51346300 | 2.640 | 378 | 7.3e-181 |
| 51987859 | 2.620 | 378 | 7.8e-186 |
| 51830096 | 2.614 | 378 | 2.1e-187 |
| 50677306 | 2.600 | 378 | 4.0e-191 |
| 50984035 | 2.598 | 378 | 1.1e-191 |
| 50081187 | 2.594 | 378 | 7.0e-193 |
| 52028119 | 2.583 | 378 | 8.0e-196 |
| 51349349 | 2.580 | 378 | 1.3e-196 |
| 50464975 | 2.576 | 378 | 9.8e-198 |
| 52146135 | 2.576 | 378 | 9.8e-198 |
| 50738334 | 2.572 | 378 | 7.7e-199 |
| 50867778 | 2.558 | 378 | 1.1e-202 |

## Verdict

**Zero promotions.** 390 alphas looked interesting raw (>2.0 Sharpe); the multiple-testing correction killed every single one — the best DSR in 2.3M trials is 2.8e-114 against a 0.99 bar. This mirrors Watty's 8k pilot exactly (327 looked good raw, zero survived). The graveyard is the result: random formulaic alphas on 22-name daily bars, 2023-2024, contain no detectable edge once you pay the 2.3M-trial multiple-testing price. Sealed holdout untouched.
