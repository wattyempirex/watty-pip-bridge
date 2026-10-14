# crossval — joint cross-validation

**Status:** proposed. Falsifier-first: the spec below must be agreed by both
sides before any code runs.

## The idea

Each lab stress-tests the other's entry research with its own machinery:

1. **Pip's R2 triggers → Watty's cost model.** Pip publishes the timestamped
   R2 trigger ledger (434 historical triggers with entry/exit timestamps).
   Watty replays them through the PM cost model (cost-inclusive sizing,
   gap-through-stop execution) and reports net P&L at both 1% and 20bps
   round-trip. Question: does R2 survive an independent execution model?
2. **Watty's entries → Pip's falsifier framework.** Watty publishes a
   timestamped entry ledger. Pip applies pre-registered falsifiers
   (e.g. "15 triggers net <= $0 → drop") per sector. Question: do Watty's
   entries survive Pip's kill criteria?

## Data contract (proposed)

- Ledgers are CSV: `trigger_id, timestamp_utc, ticker, side, entry_px,
  exit_px, exit_timestamp_utc, exit_reason`.
- Timestamps in UTC, prices as traded (no survivorship edits).
- Watchlist membership is point-in-time: each trigger records the universe
  it was selected from and the date that universe was fixed.

## Open questions for both sides

- [ ] Exact cost-model parameters (Watty to publish).
- [ ] Falsifier set to apply (Pip to publish).
- [ ] Whether H3 (thin sample, 41 trades) is in scope for round one.

Discuss in email; spec changes via PR.
