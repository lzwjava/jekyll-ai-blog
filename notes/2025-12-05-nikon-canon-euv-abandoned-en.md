---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Nikon and Canon Abandoned EUV Development
translated: false
type: note
---

Question: Nikon and Canon dominated deep ultraviolet (DUV) lithography but abandoned extreme ultraviolet (EUV) development after spending billions due to unachievable yields—how accurate is this story?

Answer:

The story is largely accurate, with some nuances around the exact reasons for abandonment and the scale of costs. Nikon and Canon were indeed dominant in DUV lithography during the 1990s and early 2000s, holding significant market share for tools using wavelengths like 193nm ArF (argon fluoride) and earlier KrF systems. However, they both exited EUV development—Nikon more definitively and Canon earlier—due to insurmountable technical hurdles, including low yields, unreliable light sources, and escalating R&D expenses that reached billions collectively across the industry. This paved the way for ASML to monopolize EUV, now essential for sub-7nm chip production.

### Historical Context

- **DUV Dominance**: In the 1980s–2000s, Nikon and Canon controlled over 80% of the lithography market at times, excelling in step-and-scan tools for DUV processes down to ~65nm nodes. Nikon, for instance, was a key supplier to Intel, while Canon focused on broader semiconductor equipment.
- **Shift to EUV**: EUV (13.5nm wavelength) promised to extend Moore's Law beyond DUV limits but required vacuum operation, multilayer mirrors (no lenses), and plasma-based light sources—far more complex than DUV. Early consortia like Japan's EUVA (involving Nikon and Canon) and the U.S.-led EUV-LLC explored it from the 1990s.

### Why They Gave Up

- **Technical Challenges and Yields**: EUV's biggest issues were power output (initial sources produced mere watts, needing hundreds for viable throughput) and defect rates, leading to yields below 50% in prototypes—unacceptable for high-volume manufacturing (HVM). Contamination, pellicle (protective film) failures, and overlay precision further eroded yields.
- **Costs**: Industry-wide EUV R&D exceeded $10–15 billion by 2010, with Nikon alone investing ~$1–2 billion on alpha/beta tools (EUV1/EUV2 prototypes shipped to Selete and Intel in 2007). Canon spent hundreds of millions on early EUV but shifted focus sooner. Escalating tool costs (~$100M+ per unit) and funding shortfalls (exacerbated by the 2008 financial crisis) made it unsustainable.
- **Timelines**:
  - **Canon**: Ceased major EUV efforts by ~2006 after shipping a small-field R&D tool to Selete. They pivoted to nanoimprint lithography (NIL) in 2004, citing EUV's risks.
  - **Nikon**: Delayed beta tools in 2009 and fully exited in 2011, citing "escalating costs" and inability to hit 2012 shipment goals. They briefly explored electron-beam lithography as an alternative but abandoned that too.
- **IP Barriers**: U.S. Department of Energy licensing via EUV-LLC favored ASML (and acquired SVG Lithography), denying Nikon and Canon full access to foundational IP—partly to counter Japan's market dominance. This left them years behind.

### Aftermath and ASML's Rise

ASML, with Intel/Samsung funding (~$7B+), persisted through 20+ years of delays, shipping first HVM EUV tools in 2017. Today, ASML's EUV revenue dwarfs competitors; Nikon/Canon hold <10% of the overall lithography market, focusing on mid/low-end DUV and alternatives like Canon's NIL (which promises 10x cheaper operation but still lags in yields).

In short, the billions spent yielded prototypes but no production tools—validating the story's core claim of yield-driven failure. This saga underscores how strategic bets (ASML's persistence) and geopolitics (IP controls) reshaped the semiconductor supply chain.

References:

- [Extreme Ultraviolet Lithography - Wikipedia](https://en.wikipedia.org/wiki/Extreme_ultraviolet_lithography)
- [Tracing the Emergence of Extreme Ultraviolet Lithography - CSET Policy Brief](https://cset.georgetown.edu/wp-content/uploads/CSET-Tracing-the-Emergence-of-Extreme-Ultraviolet-Lithography.pdf)
- [Nikon Said to Be Delaying EUV Lithography Development - EDN](https://www.edn.com/nikon-said-to-be-delaying-euv-lithography-development/)
- [The Counterattack of the Underdog in the Lithography Machine Field - 36Kr](https://eu.36kr.com/en/p/3392244236306567)
- [ASML: The Most Successful Tech Company You've Never Heard Of - Tech Monitor](https://www.techmonitor.ai/technology/future-of-asml-photolithography-semiconductor-chip-euv/)
