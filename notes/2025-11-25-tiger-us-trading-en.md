---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Tiger Brokers US Stock Day Trading
translated: false
type: note
---

Yes, that's correct for Tiger Brokers (the trading platform, which I assume you mean by "Tiger Global" based on context—likely referring to their US stock trading under the T+1 settlement cycle effective May 2024). Let me break it down clearly to confirm.

### Key Concepts in Tiger Brokers for US Stocks (T+1 Settlement)
- **T+1 Settlement**: Trades settle on the next business day (e.g., buy today = funds/shares available tomorrow). This is standard now for US equities, but it affects *availability* of funds/shares, not the trading rules themselves.
- **Day Trading (T+0)**: You can freely buy and sell the same stock on the *same calendar day* without restrictions on frequency or capital in Tiger accounts. This is explicitly allowed and doesn't trigger any "count" limits like in some other markets (e.g., China's A-shares, where T+1 prohibits same-day sells after a buy).
- **What "Counts" as a Day Trade**: In US margin accounts (including Tiger's), a day trade is any *round-trip* transaction—buying and then selling (or short-selling and buying to cover) the same security on the **same day**. This is tracked for the Pattern Day Trader (PDT) rule:
  - If you do 4+ day trades in 5 business days and your account is under $25,000 equity, you'll be flagged as a PDT and restricted.
  - But if your account is over $25,000, you can day trade unlimited times without issue.

### Your Scenarios
1. **Sell First, Then Buy Back (Same Day)**:
   - This is a round-trip: Sell (close existing position) + Buy (open new position) = **Counts as 1 day trade**.
   - Example: You own 100 shares, sell them at 10 AM, buy 100 back at 2 PM. That's one full round-trip on the same day, so it counts toward your PDT tally.
   - Why? It's opening and closing a position in the same session, regardless of order.

2. **Buy First, Then Sell (Same Day)**:
   - This is also a round-trip: Buy (open) + Sell (close) = **Counts as 1 day trade**.
   - Example: Buy 100 shares at 10 AM, sell at 2 PM. Same as above—full round-trip, counts as one.

In both cases, it's the *completion of the round-trip on the same day* that "counts." A single buy (without sell) or single sell (without buy back) doesn't count as a day trade—it's just a one-way trade. T+1 only means you can't use unsettled sale proceeds to buy more until the next day (good faith violations can occur if you do), but it doesn't change the day trade counting.

### Quick Tips for Tiger Brokers
- Check your account type: Cash accounts have stricter rules (no day trading at all if under $25k), but margin accounts (common in Tiger) follow PDT.
- Monitor in-app: Tiger's app shows your day trade counter and equity to avoid flags.
- No same-day restrictions like T+1 sell bans: Unlike HK/China stocks on Tiger, US stocks allow unlimited same-day trades.

If this is about a different market (e.g., HK stocks on Tiger, which are T+0 but have other rules) or Tiger Global Management (the VC firm, not the broker), clarify for more details!

**References**:
- [Tiger Brokers US Market Rules](https://www.itigerup.com/help/detail/usscgz?lang=en_US)
- [FINRA T+1 Settlement Guide](https://www.finra.org/investors/insights/understanding-settlement-cycles)
- [Pattern Day Trading Explanation](https://centerpointsecurities.com/understanding-the-pattern-day-trading-rule/)
