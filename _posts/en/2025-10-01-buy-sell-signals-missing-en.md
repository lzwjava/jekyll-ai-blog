---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Buy Sell Signals Missing on Yearly Charts
translated: false
type: note
---

### Issue with Buy/Sell Signals on K-Line Chart in Tiger Trade Global Mobile App

It sounds like you're encountering a display issue where buy/sell signals (e.g., technical indicators for trading signals like RSI crossovers or MACD signals, or perhaps trade feed markers for buy/sell volumes/ executions) appear on weekly or monthly timeframe K-line charts but disappear on the yearly view. In the Tiger Trade app (version 9.4.0.2 as of September 2025), this behavior may be due to app design limitations—longer timeframes like yearly have fewer data points (e.g., aggreg Powerated into monthly candles), which can cause indicators to not compute properly, appear cluttered, or be hidden altogether to avoid inaccuracies.

### Why It Happens

- **Data Granularity**: On yearly charts, the K-lines represent months recycled or years, so technical indicators (e.g., RSI requiring ~14 data points) may not trigger signals due to insufficient bars. Shorter timeframes (weekly/monthly) have more bars, allowing clear signals.
- **App Settings**: In mobile versions, buy/sell signals from "trade feed" (real-time buy/sell volume ticks or indicators) are enabled for shorter periods in quotes/page charts to prevent overload. Updates like 9.2.4 added trade feed signals, but they may default to apply only on intraday/week/month views [1].
- **Performance/UI Reasons**: Displaying dense signals on yearly views could slow the app or confuse users, so they are conditionally hidden.

### How to Resolve or Work Around It

1. **Switch Timeframes as You've Done**: For reliable buy/sell signals, stick to weekly or monthly views on the K-line. In the chart tab on the stock page, tap the timeframe selector (e.g., "Week" or "M" for month) to toggle—signals should reappear.

2. **Check Indicator Settings**:
   - Open the stock page > Chart/K-Line tab.
   - Tap the edit/settings icon (⚙️ or wrench) on the chart.
   - Ensure your indicators (e.g., RSI, MACD) are enabled. If signals still hide on yearly, the app may restrict them—try re-adding or clearing cache in Profile > Settings > Clear Cache.

3. **Enable Trade Feed Signals (If Applicable)**:
   - In the latest 9.4.0.2, trade feed (buy/sell volume indicators overlayed on K-lines) may not show on yearly. Go to Profile > Settings > Quotes or Chart settings to toggle "Display Trade Feed" if available (newer updates emphasize this on timeframe charts [1]).
   - If it's about executed trade markers (dots/lines on chart), the mobile app generally doesn't show them on charts; check the "Positions" or "Orders" tab for executed buys/sells instead.

4. **App Update and Tips**:
   - Ensure you're on 9.4.0.2 (check Profile > About in the app). Older versions may have bugs; update via app store.
   - If signals vanish persistently, restart the app or log out/in. For desktop Tiger Trade, you can enable full marker displays via Chart Settings, but mobile lacks this [2] [3].
   - For custom indicators like buy/sell arrows, visit support.tiger.com for mobile FAQs—apps don't support self-written indicators on mobile.

If this persists or you need signals specifically on yearly charts, contact Tiger Brokers support via the app (Profile > Help) or forums, as it could be a bug in the global mobile version. For detailed indicator guides, watch the "Adding Indicators to the K Chart" video on YouTube [4].

Citations:
[1] <https://www.itiger.com/about/app/update>
[2] <https://support.tiger.com/english/frequently-asked-questions/questions-about-indicators>
[3] <https://support.tiger.com/english/windows/chart/chart-settings>
[4] <https://www.youtube.com/watch?v=5xgmRavEkFE>
