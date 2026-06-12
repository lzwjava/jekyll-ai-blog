---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLM as Veto, Not Originator
translated: false
type: note
---

Good instinct to analyze first — this idea has a sound version and a dangerous version, and they look similar.

## The dangerous version: LLM decides what to buy

Replacing the mechanical signals with "read news hourly, then decide" would quietly destroy the three properties that make the current bot worth running:

1. **No edge in public news.** By the time a headline reaches a feed an LLM can read, the price moved minutes or hours ago. Trading on already-public news usually means buying pops and selling dips — systematically late. An hourly loop is an eternity in news time.
2. **It reintroduces discretion.** The original pitch for this bot was "doesn't tilt, doesn't revenge trade." An LLM reading scary headlines is discretion again, just outsourced. It will flip-flop on the same facts phrased differently, and you can't distinguish a bad-luck loss from a bad-judgment loss.
3. **You can't backtest it.** The current rules can be tested against years of data (still on our to-do list). "What would the LLM have said about this headline in March" is unanswerable, so you'd never know if the system has an edge or you're just flipping expensive coins.

## The sound version: LLM as advisor and veto, never originator

There are three places where an hourly news read genuinely helps, all of which keep order placement 100% mechanical:

1. **News veto on entries.** Mean reversion's known failure mode is catching falling knives: INTC drops 2 standard deviations, the bot buys — but the drop was an earnings warning, and it keeps falling. Before each entry, ask the LLM: *"Any major company-specific news on AAPL today — earnings, guidance, lawsuit, downgrade? Answer SAFE or VETO with one reason."* A VETO skips the entry; nothing else changes. This is a documented improvement to mean-reversion systems, and a wrong answer can only make the bot *more* conservative.
2. **Earnings-day filter.** Never enter a stock on its earnings date (the gap risk we discussed). The LLM can check this as part of the same veto call.
3. **Readable reports.** Your 7am/9pm messages become actual briefs — "Nasdaq fell on chip export headlines; the bot's INTC entry was vetoed because of X" — instead of raw numbers. Zero trading risk since reports place no orders.

The hard rule that makes this safe: **the LLM can only say "no" to a trade the rules already wanted, never "yes" to one they didn't.** Sizing, stops, the PDT guard, and the funds guard all stay outside the LLM's reach.

Two practical notes on your pasted code: it fits this design fine (I'd add it as `bot/llm.py` roughly as-is), but OpenRouter models don't browse the web by default — for actual news we'd either use OpenRouter's `:online` model suffix (built-in web search, ~$0.02/call) or fetch free RSS headlines ourselves and pass them in the prompt (cheaper, more controllable). Cost either way is trivial: roughly 6 veto checks per day ≈ a few dollars a month. It also needs an `OPENROUTER_API_KEY` secret in GitHub Actions, and one new failure mode to handle: if the LLM call fails, the bot should fall back to trading the mechanical signal (availability) — or skipping the entry (caution); I'd pick skipping, since missed trades are cheaper than bad ones.

My recommendation: build the veto + earnings filter + smart reports, keep signal generation mechanical. Want me to go ahead with that? (If yes, tell me whether you have an OpenRouter key ready and which model you'd like — something cheap like `google/gemini-2.5-flash:online` is well-suited for this.)
