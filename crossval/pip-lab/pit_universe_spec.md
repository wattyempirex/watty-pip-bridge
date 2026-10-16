# M2 point-in-time universe — PRE-REGISTERED SPEC (session 12, Watty program workstream a)

Rook verdict implemented: M2 PRIMARY (M1 vetoed VETO-1, M3 rejected, M4
subsumed). Frozen BEFORE any run. PAPER/RESEARCH ONLY.

## 0. Spec amendments (pre-run corrections, disclosed)
These correct factual errors in the original draft. The scored run has
not happened; amendments are legitimate and disclosed here.
- A-spec-1: the lab's canonical 4y R2 reference (434 trades / +$14,699)
  is computed on a **19-ticker** universe — variant_matrix.py documents
  coverage exclusions SKHY, SNDK, ARM ("not fully covered Oct22-Oct26";
  memory = MU only; semis excludes ARM). The sanity run is therefore the
  19-ticker v3.1 universe and must reproduce 434 trades / +$14,699 at
  the 1% tier (tolerance: ±2 trades, ±$200).
- A-spec-2: dropped-side group is **19** names (18 data_pit CSVs +
  IIVI→COHR mapping), not 20. The "20" label in the draft was wrong.
- A-spec-3: (b) watchlist-only = 13 names as recomputed in their
  available windows (no anachronistic bars — CSVs start at listing).
  Additionally report the 3 coverage-excluded names (SKHY/SNDK/ARM)
  separately: per-ticker n_trades and net (their recomputed delta vs
  the 19-ticker reference is +$20,169 over 37 trades — directly
  informative for the bias question, not hidden).
- The interpretation band's "watchlist" comparator is the 19-ticker lab
  reference (434 trades / +$14,699 at 1%), NOT a recomputed 22-ticker run.

## 1. Universe source (frozen)
Wikipedia "PHLX Semiconductor Sector", revision **1105073321**
(retrieved 2026-10-14 via public MediaWiki API; revision timestamp
2022-08-18T11:12:53Z; constituent list stated "updated on Aug 02, 2022").
30 tickers frozen verbatim:

AMKR, ASML, AMD, ADI, AMAT, AZTA, AVGO, ENTG, IIVI, INTC, IPGP, KLAC,
LRCX, LSCC, MRVL, MCHP, MU, MPWR, NVDA, NXPI, ON, POWI, QCOM, QRVO,
SLAB, SWKS, TSM, TER, TXN, WOLF

Disclosure: ~2-month lag between list date (Aug 02, 2022) and window
start (Oct 2022).

## 2. Window and data
Oct 2022 – Oct 2026 (bars 2022-10-03 → 2026-10-13, matching data_4y).
- 19 dropped names: hidden_files/backtests/data_pit/*.csv (fetched
  2026-10-14 via yfinance daily, same 3-header-row positional format
  as data_4y: Date,AdjClose,Close,High,Low,Open,Volume).
- 9 overlap names (AMD AMAT AVGO INTC LRCX MU NVDA QCOM TSM): data_4y.
- IIVI: INCLUDED mapped to COHR bars (data_4y/COHR.csv) — same entity,
  renamed Sep 2022. Frozen choice; no post-hoc switching.

## 3. Inclusion rule (pre-registered)
≥900 daily bars in window. Exclusions with reason:
- QRVO: 5 bars (no yfinance history before 2026-07-29) — excluded.
- WOLF: 263 bars (2025 bankruptcy restructuring; old equity cancelled)
  — excluded. Disclosed limitation: the ideal test includes WOLF's
  2022-2025 ride to zero; excluding it FLATTERS the dropped set, which
  is conservative against the severe-bias hypothesis.

## 4. R2 spec (identical v3.1)
Trigger: close ≥ 1.010 × prior-20D max close. Entry at trigger-bar
close. Stop: exit on close < C20 trigger level. Time exit: +10 bars.
$7,500 notional. Fills: entry ×1.001, exit ×0.999.
FLAT_COST: $75 (1% tier) / $15 (20bps tier). Same loader semantics as
variant_matrix.backtest (positional parse; WARMUP).

## 5. Decomposition (report ALL, both cost tiers)
(a) 19 dropped-side names: AMKR ASML ADI AZTA ENTG IPGP KLAC LSCC MRVL
    MCHP MPWR NXPI ON POWI SLAB SWKS TER TXN + COHR-for-IIVI
    (A-spec-2: 18 data_pit CSVs + IIVI→COHR; QRVO/WOLF excluded per
    inclusion rule).
(b) 13 watchlist-only names: SKHY PLTR SNOW SNDK ARM AAPL MSFT GOOGL
    META AMZN NFLX COHR GLW (data_4y).
(c) 9 overlap names: AMD AMAT AVGO INTC LRCX MU NVDA QCOM TSM (data_4y).
Sanity check: the 19-ticker v3.1 universe run with NO sector filter
must reproduce ≈434 trades / +$14,699 at the 1% tier (A-spec-1:
SKHY/SNDK/ARM excluded per the lab's documented coverage rule).

## 6. Filter versions
- PRIMARY: NO v3.1 sector filter on any group (tests universe
  selection, not sector selection — Watty's point).
- SECONDARY: with v3.1 filter using this FROZEN sector map:
  - broad semis (eligible): AMKR ADI AZTA IPGP LSCC MRVL MCHP MPWR
    NXPI ON POWI SLAB SWKS TXN (+ overlap AMD AVGO INTC NVDA QCOM TSM)
  - semicap equipment: ASML KLAC TER ENTG (+ overlap AMAT LRCX) —
    eligible at 20bps tier ONLY (v3.1)
  - memory: MU (overlap) — eligible
  - optical: IIVI→COHR — EXCLUDED

## 7. Interpretation bands (no discretion after the run)
- dropped net/trade ≥ 50% of watchlist net/trade → selection bias MODEST.
- dropped net ≤ $0 while watchlist net > $0 → bias SEVERE.
- If severe: the point-in-time number becomes the lab's reported 4y
  headline (REPLACES the watchlist number in rulebook provenance).
  No dollar-subtraction of "bias" from +$14,699 is valid (VETO-2).
- Forward paper falsifiers still carry the actual validation burden.

## 8. What M2 does NOT do
It cannot decompose +$14,699 into "real edge" vs "bias dollars." It
produces a parallel, lower-bias estimate. That is the honest answer.
