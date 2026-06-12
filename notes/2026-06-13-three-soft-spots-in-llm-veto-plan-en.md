---
audio: false
generated: true
image: false
lang: en
layout: post
title: Three Soft Spots in LLM Veto Plan
translated: false
type: note
---

**Question:** What's your assessment of this plan — keeping the trading bot's signals mechanical, but adding an hourly LLM news read as a veto layer plus report generation?

**Answer:**

The analysis is directionally right — veto-only, never originator, is the correct architecture. But it has three soft spots worth fixing before you build.

**1. The veto is also unbacktestable — the analysis applies its own critique unevenly**

It says the "LLM decides" version fails because you can't backtest it. True. But "what would the LLM have vetoed in March" is equally unanswerable. The veto is *bounded-risk* unbacktestable rather than unbounded, which is better, but you still won't know if it helps. The fix is cheap: ship it in shadow mode first.

```python
# bot/llm_veto.py
import re, json, time

VETO_RE = re.compile(r"^\s*(SAFE|VETO)\b", re.I)

def check_news_veto(symbol: str, shadow: bool = True) -> dict:
    prompt = (
        f"Any major company-specific news on {symbol} in the last 24h — "
        "earnings, guidance cut, lawsuit, downgrade, fraud? "
        "First word of your reply MUST be SAFE or VETO, then one short reason."
    )
    try:
        text = "".join(stream_openrouter_api(prompt, model=MODEL, max_tokens=100))
        m = VETO_RE.match(text)
        decision = m.group(1).upper() if m else "VETO"  # unparseable -> conservative
    except Exception as e:
        text, decision = f"ERROR: {e}", "VETO"           # API down -> skip entry

    record = {"ts": time.time(), "symbol": symbol, "decision": decision,
              "raw": text, "shadow": shadow}
    with open("veto_log.jsonl", "a") as f:
        f.write(json.dumps(record) + "\n")

    return {"veto": (decision == "VETO") and not shadow, "record": record}
```

Run with `shadow=True` for 4–6 weeks: the bot trades as if the LLM doesn't exist, but you log every decision. Then join `veto_log.jsonl` against actual trade P&L and ask one question: *did vetoed entries underperform non-vetoed ones?* If yes, flip the flag. If no, you just saved yourself from adding a lossy filter. This converts an article of faith into a measured component — same discipline you'd apply to any eval.

**2. "Wrong answers only make it more conservative" is true for risk, false for edge**

Mean reversion's profit *is* buying fear. A 2-sigma drop frequently comes with a scary headline attached — that's why the price dropped. An LLM that vetoes every alarming headline will preferentially veto the trades with the most fear priced in, which may be exactly the ones that pay. Over-vetoing doesn't blow up the account; it quietly bleeds the edge to zero while looking prudent. The shadow-mode data answers this empirically, but tighten the prompt too: you want it vetoing *regime-changing* news (earnings miss, guidance cut, fraud, delisting risk), not *sentiment* news ("analysts worry about…"). Enumerate the veto categories explicitly in the prompt and tell it everything else is SAFE.

**3. The earnings filter shouldn't use an LLM at all**

Earnings dates are structured, scheduled, public data. A calendar lookup is deterministic, free, backtestable, and never hallucinates — an LLM call is strictly worse for this. Alpaca's API exposes corporate actions, and Finnhub/FMP have free earnings-calendar endpoints:

```python
import requests, datetime as dt

def has_earnings_today(symbol: str, api_key: str) -> bool:
    today = dt.date.today().isoformat()
    r = requests.get("https://finnhub.io/api/v1/calendar/earnings",
                     params={"from": today, "to": today, "symbol": symbol,
                             "token": api_key}, timeout=10)
    return bool(r.json().get("earningsCalendar"))
```

Reserve the LLM for the genuinely unstructured part (breaking news interpretation) and use boring lookups for structured facts. Right tool per layer.

**Two more hardening notes**

- **Prompt injection surface.** With `:online` models the LLM ingests arbitrary web text that can contain instructions. The strict output contract above (`SAFE|VETO` as first token, anything else → VETO) means the worst an injected page can do is cause a skipped trade — never a placed one. Keep it that way: the veto function must return a bool, and nothing downstream should ever parse the reason text for action.
- **Pin and log everything.** Pin the model string, set `temperature: 0`, log raw responses. When a veto looks wrong in three weeks, you want to replay the exact input/output, not guess.

So: yes to veto + reports, with shadow mode as a mandatory first phase; no to LLM-based earnings checking. The hard rule from the analysis stands — LLM can say no, never yes — and the shadow log is what eventually tells you whether the "no"s are worth their false-positive cost.
