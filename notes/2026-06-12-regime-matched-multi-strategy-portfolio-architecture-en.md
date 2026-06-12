---
audio: false
generated: true
image: false
lang: en
layout: post
title: Regime-Matched Multi-Strategy Portfolio Architecture
translated: false
type: note
---

**Question:** Explain the architecture and logic of my multi-strategy trading bot — three strategies across five instruments with a shared risk layer.

**Answer:**

Your bot is a classic *regime-matched* portfolio: each strategy is paired to the statistical behavior of its market, and a shared risk layer normalizes them all into comparable bets. Here's the system layer by layer.

## 1. Why each strategy fits its instrument

The core insight is autocorrelation of returns at different timescales:

- **Index ETFs (SPLG/QQQM) intraday** show *negative* short-horizon autocorrelation — an overextension tends to snap back. So you fade extremes (mean reversion).
- **Bitcoin (IBIT)** shows *positive* autocorrelation — a new high tends to be followed by more highs. Fading BTC overextensions gets you run over; riding breakouts works (momentum).
- **Commodities (GLD/USO)** trend, but slowly and noisily. A 4-hour SMA crossover is a low-pass filter: it ignores intraday whipsaw and only flips when the medium-term wave actually turns (trend following).

You're essentially diversifying across *signal types*, not just tickers. Mean reversion and trend following have historically low or negative correlation of returns — when chop kills the trend strategies, the reversion strategies eat; when a strong trend kills reversion, the trend strategies eat.

## 2. The three signal engines

**Mean reversion (z-score):**

```python
def zscore_signal(closes, n=20):
    mu = closes[-n:].mean()
    sigma = closes[-n:].std()
    z = (closes[-1] - mu) / sigma
    if z <= -2: return "BUY"    # 2σ below mean: statistically stretched
    if z >= 0:  return "SELL"   # reverted to mean: edge is spent
```

The asymmetry matters: you enter at −2σ but exit at 0, not +2σ. You're harvesting *only the reversion*, not betting on continuation past the mean. That keeps holding periods short and avoids overstaying.

**Momentum breakout (Donchian):**

```python
def donchian_signal(highs, lows, close):
    if close > highs[-21:-1].max(): return "BUY"   # breaks prior 20-bar high
    if close < lows[-11:-1].min():  return "SELL"  # breaks prior 10-bar low
```

The asymmetric channel (20 in / 10 out) is deliberate: slow to enter (confirm the breakout is real), faster to exit (give back less when the trend dies). This is the classic Turtle-style structure.

**Trend following (dual SMA):**

```python
def sma_trend_signal(closes):
    fast, slow = closes[-20:].mean(), closes[-50:].mean()
    if fast > slow and closes[-1] > slow: return "BUY"
    if fast < slow:                        return "SELL"
```

The extra condition `price > slow SMA` filters out entries during a crossover that happens while price is already rolling over — a cheap whipsaw reducer.

## 3. The risk layer — where the real engineering is

**ATR-based 1% sizing** is volatility normalization:

```python
risk_dollars = 0.01 * equity
stop_dist    = 2 * atr14
shares       = risk_dollars / stop_dist
```

Since `stop_dist` scales with volatility, a quiet instrument (GLD) gets a large position and a violent one (IBIT) gets a small one — but *both lose exactly 1% of equity if stopped*. Every trade is the same-sized bet in risk space. This is what makes a 5-instrument, 3-strategy book coherent: positions are comparable units.

**GTC stop at the broker** decouples risk enforcement from bot uptime. Since you run on GitHub Actions (which can be delayed, rate-limited, or down), the stop living server-side at the broker means the 1% cap doesn't depend on your cron firing. This is the single most important reliability decision in the design.

**Correlation filter (max 2 longs in SPLG/QQQM/IBIT)**: those three are all risk-on assets — in a risk-off shock they sell off together, so three "independent" 1% bets are really one ~3% bet. Capping at 2 bounds the correlated drawdown.

**No leverage, 95% cash cap, 25% per-instrument cap**: hard guardrails so that no sizing bug, ATR collapse (tiny ATR → huge share count), or signal pile-up can blow past sane exposure. The 25% cap specifically protects against the ATR-sizing failure mode where low volatility produces an enormous position.

## 4. Execution model and its edges

The engine wakes every 15 min, evaluates all five, and acts only on *fresh* signal transitions — i.e., it's edge-triggered, not level-triggered. That prevents re-entering the same signal every cycle.

Things worth keeping an eye on in this design:

1. **Bar-close alignment**: your 1h (IBIT) and 4h (GLD/USO) strategies only have new information once per 4–16 cycles. Make sure the bot evaluates them on *closed* bars only, or the SMA/Donchian values will flicker intra-bar and generate phantom signals.
2. **Gap risk**: a GTC stop caps risk *at the stop price*, not at 1%. An overnight gap through the stop (especially IBIT tracking 24/7 BTC against US-session trading) can lose more than 1%. The 25% position cap is your real worst-case bound here.
3. **GitHub Actions jitter**: scheduled workflows can fire minutes late or get skipped under load. Since stops are at the broker, this only delays *entries/exits on signal*, not risk enforcement — which is the right failure mode to have.
4. **Z-score with σ→0**: in dead-quiet sessions the 20-bar std can get tiny, making z-scores explode. A minimum-σ floor avoids spurious −2σ entries on noise.

## Summary in one line

Three uncorrelated edge types (fade / breakout / trend), each matched to its market's autocorrelation regime, all flattened into identical 1%-risk units by ATR sizing, with broker-side stops so risk holds even when the bot doesn't run.

One caveat since this is live money: I'm not a financial advisor and nothing here is a claim that these edges are currently profitable — the explanation covers the mechanics and engineering soundness, which are solid. The empirical question (do these signals still carry edge net of fees/slippage at 15-min granularity?) is only answerable from your backtest and live fills.
