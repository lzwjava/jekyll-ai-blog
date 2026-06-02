---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Tiger Trade Insufficient Margin Rejection Explained
translated: false
type: note
---

Question: Explain the Tiger Trade rejection message: "201:Order rejected - Reason: YOUR ORDER IS NOT ACCEPTED. IN ORDER TO OBTAIN THE DESIRED POSITION YOUR EQUITY WITH LOAN VALUE [636.45 USD] MUST EXCEED THE INITIAL MARGIN [736.92 USD]"

Answer:

This error message from **Tiger Trade** (Tiger Brokers' platform) means your order was rejected because your account does not have enough equity to meet the **initial margin requirement** for the trade you are trying to open.

### Key Terms Explained

- **Equity with Loan Value (ELV)**: This is the effective equity in your margin account that can be used to support leveraged positions. It typically equals the total value of your assets (cash + securities value) minus certain adjustments (like options values in some cases), and it serves as the base for calculating how much you can borrow or leverage.
- **Initial Margin (IM)**: This is the minimum amount of equity required to **open** a new position when using margin (leverage). It is usually a percentage of the total position value, depending on the asset (e.g., stock, futures, options). For many stocks it might be around 50%, but it can be higher for volatile assets, options, futures, or specific instruments.

The message specifically says your **Equity with Loan Value ($636.45)** is **less than** the required **Initial Margin ($736.92)** for the position you want to open after the trade executes.

### Why This Happens

- You are trading on **margin** (borrowing from the broker to increase position size).
- The proposed trade requires more collateral (initial margin) than your current usable equity provides.
- Your account has insufficient "skin in the game" to safely open the larger leveraged position.
- This is a **risk control** measure — the broker (and regulators) prevent over-leveraging that could lead to quick losses or negative balances.

### Common Causes

- Low account balance relative to the trade size.
- Trying to open a large position (too many shares/contracts).
- Trading a high-margin-requirement instrument (e.g., volatile stock, options, futures).
- Recent losses reduced your equity.
- Intraday profits might not always count fully toward opening new positions (similar to some brokers' rules using previous day's equity in certain cases).
- Currency or cross-market issues if trading in non-base currency.

### How to Fix or Avoid It

- **Deposit more funds** to increase your Equity with Loan Value above the required initial margin.
- **Reduce the order size** (buy/sell fewer shares or contracts) so the required initial margin drops below your current ELV.
- **Close existing positions** to free up margin/equity.
- **Switch to a cash account** (if possible) or avoid margin trades if you don't want leverage requirements.
- Check your account details in the Tiger Trade app: Look at "Account" → margin/equity sections to see current ELV, initial margin requirements, excess liquidity, and buying power.
- Review the specific asset's margin requirement (Tiger provides lists for marginable securities).

In short: Your account's usable equity ($636.45) is too low to support the new position's initial margin need ($736.92). Add funds or trade smaller to resolve it.

References:

- [Tiger Trade Help - Margin & Leverage](https://www.tigertrade.app/help/detail/07532949)
- [Tiger Trade Help - Risk State](https://www.tigertrade.app/help/detail/68026009)
