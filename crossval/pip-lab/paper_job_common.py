"""Local, deterministic research helpers; no network or execution interfaces."""
import csv, json, math
from pathlib import Path
BASE = Path(__file__).resolve().parent
SEMIS = ('NVDA','AMD','AVGO','TSM','INTC','QCOM','ARM')
def load(ticker):
    with (BASE/'data_4y'/f'{ticker}.csv').open(newline='') as f:
        rows = csv.reader(f)
        header = next(rows); next(rows); next(rows)
        assert header == ['Price','Adj Close','Close','High','Low','Open','Volume'], header
        bars=[]
        for r in rows:
            d,a,c,h,l,o,v=r
            vals=list(map(float,(o,h,l,c,a,v)))
            assert all(math.isfinite(x) for x in vals) and min(vals[:5])>0
            bars.append(dict(date=d,open=vals[0],high=vals[1],low=vals[2],close=vals[3],adj_close=vals[4],volume=vals[5]))
    assert all(a['date']<b['date'] for a,b in zip(bars,bars[1:]))
    return bars
def pnl(entry,exit,spread=False):
    return round(7500*(exit*(.999 if spread else 1)/(entry*(1.001 if spread else 1))-1)-75,2)
def summary(ts):
    n=len(ts); net=round(sum(t['net_pl'] for t in ts),2)
    return dict(n=n,net_pl=net,win_rate_pct=round(100*sum(t['net_pl']>0 for t in ts)/n,4) if n else None,avg_net_per_trade=round(net/n,2) if n else None)
def save(stem,result,md):
    (BASE/f'{stem}.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    (BASE/f'{stem}.md').write_text(md+'\n')
    print(stem, json.dumps(result.get('summary',result.get('summaries',result.get('counts')))))
COMMON = 'Positional parser skips three rows; actual CSV order is Date,Adj Close,Close,High,Low,Open,Volume (differs from prompt). Raw Close used, not Adj Close. $7,500 fractional-share notional; $75 per completed trade; close fills, no spreads, slippage, dividends or portfolio constraints. Paper/research only.'
