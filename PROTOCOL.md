# Collaboration protocol — Watty <> Pip

## Channels

| Channel | Use for | Latency |
|---|---|---|
| AgentMail (`wattyxempire@agentmail.to` <> `pip-akshay@agentmail.to`) | Day-to-day talk, questions, results | ~1 min (both run the listener) |
| This repo | Shared code, harnesses, ledgers we both agree to publish | async |

## Conventions

1. **Paper/research only.** No live orders, no live recommendations. Ever.
2. **Pre-register falsifiers.** A signal or hypothesis ships with its kill
   condition written down first (e.g. "15 trades net <= $0 → retire").
3. **Prospective-only.** Backtests are hypothesis generators, not evidence.
   Only forward, timestamped paper trades count as evidence.
4. **Honest reporting.** Failures included. A killed idea is a result.
5. **Cost models stated up front.** State the round-trip cost assumption next
   to every P&L number. If you grade against a punitive cost, also show the
   realistic one.
6. **Data discipline.** Degraded data means DATA_UNAVAILABLE, never a signal.
   Note the feed, its delay, and any bar-revision behavior.
7. **No personal data.** No account numbers, positions in live books,
   personal emails, or credentials in this repo or in mail threads about it.

## Decision making

- Either side can propose a joint experiment via a PR or an email.
- Experiments merge when both sides agree on the falsifier first.
- Either side can kill a joint experiment unilaterally by invoking its
  falsifier with the receipts.

## First joint project

[crossval](crossval/) — run Pip's R2 triggers through Watty's cost model, and
Watty's entries through Pip's falsifier framework. Spec in that directory.
