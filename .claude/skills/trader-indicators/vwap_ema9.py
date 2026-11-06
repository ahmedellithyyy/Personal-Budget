#!/usr/bin/env python3
"""VWAP + EMA 9 read for a list of tickers. Standard library only, free Yahoo data.

Per ticker it prints:
  - last price and today's move vs the previous close
  - session VWAP  : today's 5-minute bars (resets every session)
  - anchored VWAP : daily bars from an anchor date (default: the 60-day closing high)
  - EMA 9         : on daily closes
  - a one-line regime read (price vs each line, EMA 9 slope)

Usage:
  python3 .claude/skills/trader-indicators/vwap_ema9.py TSM ASML ANET AMD MU
  python3 .claude/skills/trader-indicators/vwap_ema9.py TSM --anchor 2026-10-29
  python3 .claude/skills/trader-indicators/vwap_ema9.py TSM --json

Reads and reports only. Not financial advice.
"""
import argparse, json, sys, time, urllib.request
from datetime import datetime, timezone, timedelta

UA = "Mozilla/5.0 (vwap-ema9 reader)"
NY = timezone(timedelta(hours=-5))  # EST; good enough for session bucketing in Nov-Mar


def fetch_chart(sym, rng, interval, timeout=20):
    url = ("https://query2.finance.yahoo.com/v8/finance/chart/%s?range=%s&interval=%s"
           "&includePrePost=false" % (sym, rng, interval))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read().decode("utf-8"))
    res = data["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    bars = []
    for i, ts in enumerate(res.get("timestamp", [])):
        o, h, l, c, v = (q["open"][i], q["high"][i], q["low"][i], q["close"][i], q["volume"][i])
        if None in (h, l, c) or v is None:
            continue
        bars.append({"t": ts, "o": o, "h": h, "l": l, "c": c, "v": v})
    meta = res.get("meta", {})
    return bars, meta


def ema(values, n):
    if len(values) < n:
        return None
    k = 2.0 / (n + 1)
    e = sum(values[:n]) / n            # seed with the SMA of the first n
    for x in values[n:]:
        e = x * k + e * (1 - k)
    return e


def vwap(bars):
    pv = sum(((b["h"] + b["l"] + b["c"]) / 3.0) * b["v"] for b in bars)
    vol = sum(b["v"] for b in bars)
    return pv / vol if vol else None


def session_date(ts):
    return datetime.fromtimestamp(ts, NY).date()


def analyse(sym, anchor=None):
    daily, meta = fetch_chart(sym, "6mo", "1d")
    time.sleep(0.6)
    intra, _ = fetch_chart(sym, "5d", "5m")

    closes = [b["c"] for b in daily]
    ema9_now = ema(closes, 9)
    ema9_prev = ema(closes[:-1], 9)

    # anchor: explicit date, else the date of the highest close in the last 60 bars
    if anchor:
        a_date = datetime.strptime(anchor, "%Y-%m-%d").date()
    else:
        window = daily[-60:]
        a_date = session_date(max(window, key=lambda b: b["c"])["t"])
    a_bars = [b for b in daily if session_date(b["t"]) >= a_date]
    avwap = vwap(a_bars) if a_bars else None

    # session VWAP: bars of the most recent session in the intraday feed
    last_day = session_date(intra[-1]["t"]) if intra else None
    s_bars = [b for b in intra if session_date(b["t"]) == last_day]
    svwap = vwap(s_bars) if s_bars else None

    last = meta.get("regularMarketPrice") or closes[-1]
    # day move: Yahoo's own regular-session change, else last vs the prior daily bar
    move = meta.get("regularMarketChangePercent")
    if move is None and len(closes) > 1:
        prev = closes[-2] if abs(last - closes[-1]) < 1e-9 else closes[-1]
        move = (last / prev - 1) * 100
    prev = last / (1 + move / 100) if move is not None else None
    # pre/post-market print, when Yahoo has one that differs from the regular-session price
    ext = meta.get("fulldayPrice")
    ext_pct = meta.get("fulldayChangePercent")
    if ext is None or abs(ext - last) < 1e-9:
        ext, ext_pct = None, None

    def rel(x):
        return None if x is None else (last / x - 1) * 100

    out = {
        "symbol": sym, "last": last, "prev_close": prev, "move_pct": move,
        "session_vwap": svwap, "vs_session_vwap_pct": rel(svwap),
        "anchor_date": a_date.isoformat(), "anchored_vwap": avwap, "vs_anchored_vwap_pct": rel(avwap),
        "ema9": ema9_now, "vs_ema9_pct": rel(ema9_now),
        "ema9_slope": None if None in (ema9_now, ema9_prev) else ("up" if ema9_now > ema9_prev else "down"),
        "ext_price": ext, "ext_move_pct": ext_pct,
        "session": last_day.isoformat() if last_day else None,
    }
    out["read"] = read(out)
    return out


def read(r):
    above_s = r["vs_session_vwap_pct"] is not None and r["vs_session_vwap_pct"] > 0
    above_a = r["vs_anchored_vwap_pct"] is not None and r["vs_anchored_vwap_pct"] > 0
    above_e = r["vs_ema9_pct"] is not None and r["vs_ema9_pct"] > 0
    if above_e and above_a:
        return "trend intact: above EMA 9 and above anchored VWAP"
    if not above_e and not above_a and r["ema9_slope"] == "down":
        tail = "buyers defended session VWAP" if above_s else "sold below session VWAP too"
        return "momentum broken: below EMA 9 (falling) and below anchored VWAP; " + tail
    if not above_e and above_a:
        return "pullback inside the trend: below EMA 9, still above anchored VWAP"
    return "mixed: above EMA 9 but below anchored VWAP (rally into supply)"


def fmt(x, d=2):
    return "-" if x is None else ("%.*f" % (d, x))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("tickers", nargs="+")
    p.add_argument("--anchor", help="anchored-VWAP start date YYYY-MM-DD (default: 60-day closing high)")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    rows, errors = [], []
    for sym in a.tickers:
        try:
            rows.append(analyse(sym.upper(), a.anchor))
        except Exception as e:  # network, parse
            errors.append("%s: %s" % (sym, e))
        time.sleep(0.6)

    if a.json:
        print(json.dumps({"rows": rows, "errors": errors}, indent=2))
        return
    hdr = "%-6s %9s %7s %10s %7s %10s %7s %10s %7s %-5s" % (
        "sym", "last", "day%", "sessVWAP", "vs%", "aVWAP", "vs%", "EMA9", "vs%", "slope")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print("%-6s %9s %7s %10s %7s %10s %7s %10s %7s %-5s" % (
            r["symbol"], fmt(r["last"]), fmt(r["move_pct"], 1),
            fmt(r["session_vwap"]), fmt(r["vs_session_vwap_pct"], 1),
            fmt(r["anchored_vwap"]), fmt(r["vs_anchored_vwap_pct"], 1),
            fmt(r["ema9"]), fmt(r["vs_ema9_pct"], 1), r["ema9_slope"] or "-"))
        if r["ext_price"] is not None:
            print("       pre/post-market %s (%s%% vs last close)" % (fmt(r["ext_price"]), fmt(r["ext_move_pct"], 1)))
        print("       anchor %s | %s" % (r["anchor_date"], r["read"]))
    for e in errors:
        print("note:", e)
    print("\nChecked %s UTC. Reads and reports only; not financial advice." %
          datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"))


if __name__ == "__main__":
    main()
