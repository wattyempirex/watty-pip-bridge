"""R2-TRAIL forward-only paper evaluator. Forged 2026-10-14, session 10.

No network, order routing, ledger writes, or automatic live-book adoption.
CLI: python3 r2_trail.py INPUT.json; python3 r2_trail.py --self-test
INPUT: {trade: {ticker, entry_date, entry_close, c20_trigger_level,
               notional, fills, live_book_exit},
        bars: [{date, close}], price_basis: "raw_close"|"adjusted_close",
        split_factors: {effective_date: price_multiplier}}
Bars include >=20 pre-entry trading sessions. close is the selected series;
entry and C20 must use that same basis. live_book_exit is null while pending,
otherwise {exit_date, exit_close, exit_reason}. Caller enforces entry parity
and skips same-ticker entries while a shadow position is open.
"""
import argparse
import json
import math
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent


def positive(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f'{label} must be numeric')
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f'{label} must be finite and positive')
    return float(value)


def evaluate(trade, bars, *, price_basis, split_factors=None):
    """Return completed exit or explicit pending result plus paired live exit.

    Strict close < stop, with stop taking precedence on day +10. Factors
    are NEW-price / OLD-price (2:1 split => 0.5), applied before that day's
    ratchet/check. For raw closes, prior window prices are also translated
    into current units; for adjusted closes, the supplied history already
    uses one basis and must never be split-adjusted twice (factors prohibited).
    Replaying a split requires entry/C20 in their original entry units and
    raw bars in contemporaneous units. A consistently adjusted series uses
    adjusted entry/C20 and no factors. No fabricated terminal liquidation.
    """
    if price_basis not in ('raw_close', 'adjusted_close'):
        raise ValueError('explicit price_basis required')
    factors = {d: positive(f, 'split factor') for d, f in (split_factors or {}).items()}
    if price_basis == 'adjusted_close' and factors:
        raise ValueError('adjusted series already scales splits; do not double-adjust')
    if not trade.get('ticker'):
        raise ValueError('ticker required')
    entry = positive(trade['entry_close'], 'entry close')
    stop = positive(trade['c20_trigger_level'], 'C20 trigger')
    dates = [b['date'] for b in bars]
    for d in dates:
        if date.fromisoformat(d).isoformat() != d:
            raise ValueError('dates must be ISO YYYY-MM-DD')
    if any(a >= b for a, b in zip(dates, dates[1:])):
        raise ValueError('bars must be strictly chronological and unique')
    if set(factors) - set(dates):
        raise ValueError('split effective dates must be present in bars')
    closes = [positive(b['close'], 'close') for b in bars]
    if trade['entry_date'] not in dates:
        raise ValueError('entry date missing')
    i = dates.index(trade['entry_date'])
    if i < 20:
        raise ValueError('20 pre-entry bars required')
    if entry != closes[i]:
        raise ValueError('entry close must equal entry bar on selected basis')
    # Normalize raw historical bars into entry-day units, including splits
    # before entry, without changing the caller-provided entry or C20.
    history = []
    for k in range(i + 1):
        factor = factors.get(dates[k], 1.0)
        history = [v * factor for v in history]
        history.append(closes[k])
    result = dict(ticker=trade['ticker'], entry_date=trade['entry_date'],
                  price_basis=price_basis, exit_date=None, exit_close=None,
                  exit_reason=None, status='open',
                  paired_live_book_exit=trade.get('live_book_exit'))
    for j in range(i + 1, min(i + 11, len(bars))):
        factor = factors.get(dates[j], 1.0)
        stop *= factor
        history = [v * factor for v in history]
        stop = max(stop, min(history[-20:]))  # excludes current bar
        close = closes[j]
        reason = 'stop' if close < stop else 'time' if j == i + 10 else None
        if reason:
            result.update(exit_date=dates[j], exit_close=close,
                          exit_reason=reason, status='completed', stop_at_exit=stop)
            return result
        history.append(close)
    result.update(stop_at_last_check=stop, last_available_date=dates[-1])
    return result


def self_test():
    from paper_job_common import load
    frozen = json.loads((BASE / 'exit_variants_frozen.json').read_text())
    # Fixed fixtures, not runtime selection. These five are common to A2 and
    # historical V1. Historical V1's different initialization prevents a
    # claim of full parity; see the spec's reference discrepancy notice.
    keys = [('AMAT', d) for d in ('2023-05-17', '2024-01-19', '2024-02-09',
                                  '2024-05-15', '2025-05-12')]
    v1 = {(t['ticker'], t['entry_date']): t for t in frozen['trades']['V1']}
    v0 = {(t['ticker'], t['entry_date']): t for t in frozen['trades']['V0']}
    for key in keys:
        known = v1[key]
        bars = load(key[0])
        i = next(j for j, b in enumerate(bars) if b['date'] == key[1])
        trade = dict(ticker=key[0], entry_date=key[1], entry_close=known['entry_close'],
                     c20_trigger_level=max(b['close'] for b in bars[i-20:i]),
                     live_book_exit={k: v0[key][k] for k in
                                     ('exit_date', 'exit_close', 'exit_reason')})
        actual = evaluate(trade, bars, price_basis='raw_close')
        assert all(actual[k] == known[k] for k in ('exit_date', 'exit_close', 'exit_reason')), key
        assert actual['paired_live_book_exit'] == trade['live_book_exit']
    # Boundary fixtures distinguish A2 from the historical V1 initialization,
    # exclude the current close, check strict inequality, pending, and splits.
    from datetime import timedelta
    dates = [(date(2026, 1, 1) + timedelta(days=k)).isoformat() for k in range(31)]
    bars = [dict(date=d, close=100.0) for d in dates]
    bars[20]['close'] = 110.0
    trade = dict(ticker='TEST', entry_date=dates[20], entry_close=110.0,
                 c20_trigger_level=105.0, live_book_exit=None)
    bars[21]['close'] = 104.0
    assert evaluate(trade, bars, price_basis='raw_close')['exit_date'] == dates[21]
    trade['c20_trigger_level'] = 100.0
    bars[21]['close'] = 99.0
    assert evaluate(trade, bars, price_basis='raw_close')['exit_reason'] == 'stop'
    bars[21]['close'] = 100.0
    assert evaluate(trade, bars[:22], price_basis='raw_close')['status'] == 'open'
    assert evaluate(trade, bars, price_basis='raw_close')['exit_reason'] == 'time'
    bars[30]['close'] = 99.0
    assert evaluate(trade, bars, price_basis='raw_close')['exit_reason'] == 'stop'
    for b in bars[21:]:
        b['close'] = 50.0
    split = evaluate(trade, bars, price_basis='raw_close', split_factors={dates[21]: 0.5})
    assert split['exit_reason'] == 'time' and split['stop_at_exit'] == 50.0
    print('PASS: 5 fixed frozen-trade exits identical; A2 boundary/split checks passed.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?', type=Path)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        self_test()
    elif args.input:
        data = json.loads(args.input.read_text())
        print(json.dumps(evaluate(data['trade'], data['bars'],
                                  price_basis=data['price_basis'],
                                  split_factors=data.get('split_factors')),
                         indent=2, allow_nan=False))
    else:
        parser.error('provide INPUT.json or --self-test')


if __name__ == '__main__':
    main()
