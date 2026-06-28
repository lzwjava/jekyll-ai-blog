---
audio: false
generated: true
image: false
lang: en
layout: post
title: Apple vs. Micron Price Battle Heats Up
translated: false
type: note
---

Question: What's the current state of the fight/debate between memory makers (Micron, etc.) and Apple over memory (DRAM/NAND) prices?

Let me search for current info on this.Here's what's happening — this just blew up over the past few days (June 25–27, 2026).

## The setup: "RAMageddon"

The root cause isn't Apple vs. Micron directly — it's AI eating all the memory supply. Samsung, SK Hynix, and Micron control more than 95% of DRAM output, and all three have been shifting capacity toward high-bandwidth memory (HBM), the specialized chips that sit inside Nvidia's AI server clusters. HBM carries roughly 60% margins versus around 40% for commodity DRAM, so every wafer redirected to AI is a wafer pulled away from the LPDDR memory inside phones, laptops, and tablets.

The price math is brutal: DRAM prices rose as much as 98% in Q1 2026 and are set to jump another 58–63% in the current quarter, per TrendForce. Micron's quarter shows where the money went: revenue more than quadrupled, up 346% YoY to $41.46 billion, with gross margin hitting roughly 85% — briefly putting a memory maker ahead of Nvidia on that metric.

## Apple's move

On June 25, Apple raised prices across nearly its entire Mac, iPad, and home device lineup with no new specs to justify the bump. Products across Mac, iPad, Apple TV, HomePod, and Vision Pro all went up; only iPhone, Apple Watch, and AirPods were untouched. Cook framed it as a "hundred-year flood" unlike anything he'd seen in four decades, arguing pricing needed to come back down to earth before Apple's own prices could follow. The market punished them: Apple's stock closed down 6%, its worst single day in over a year, wiping out roughly $265 billion in market value.

## The actual "fight" — Micron's counterpunch

Hours after Apple's hikes, Micron's Chief Business Officer Sumit Sadana fired back in a WSJ interview. The subtext was clear even though he didn't name Apple: Sadana suggested that aggressive customer pricing during the last memory downturn helped weaken industry investment and contributed to today's supply crunch. Micron had told some customers during the previous down cycle that aggressive price pressure was "unconstructive."

Translation: *you device makers squeezed our margins to nothing for years during the gluts, so we under-invested in capacity, so don't act surprised now.* As AppleMagazine put it: the company may now be paying for an industry cycle it helped pressure during cheaper years. Apple is the most visible target because it has long been known for tough supplier negotiations and a supply-chain model built around squeezing costs.

## Why this is structural, not a blip

Micron has locked in the demand side hard: around $100 billion of minimum revenue through take-or-pay contracts running to 2030, meaning hyperscalers have effectively reserved memory supply at elevated prices for years. Mehrotra expects tight conditions to persist beyond calendar 2027, with no line of sight on when supply catches up to demand.

The deeper read: this is the classic memory-cycle whip — buyers extract every cent during gluts, suppliers respond by killing capex, then a demand shock (AI) leaves everyone short and reverses all the negotiating leverage. Apple's pricing-power myth also took a hit — buyers are now paying 15% to 54% more for identical hardware, breaking the "pay more, get more" link Apple's premium pricing rested on.

One angle relevant to your world: this is why local LLM inference on consumer hardware is about to get meaningfully more expensive per GB. Your MI300X's 192GB HBM3 and even the 4070's 12GB are sitting on exactly the supply that's being reallocated. If you're planning hardware buys for training/inference, front-loading them before the Q3 hikes fully land is the rational move.

References:

- [Micron Suggests Apple Helped Cause Memory Price Crisis - MacRumors](https://www.macrumors.com/2026/06/26/micron-suggests-apple-helped-cause-memory-crisis/)
- [Micron Puts Apple's Memory Strategy Under Scrutiny - AppleMagazine](https://applemagazine.com/apple-memory-buying-micron/)
- [Apple raises prices as memory costs skyrocket - Reuters/Investing.com](https://www.investing.com/news/stock-market-news/apple-raises-prices-of-macbooks-ipads-as-memory-costs-skyrocket-4760683)
- [The business logic behind Apple's memory squeeze - Business Model Analyst](https://businessmodelanalyst.com/apple-price-hikes-memory-shortage-2026/)
- [Apple and Microsoft hike prices as AI crunches memory supply - CBC](https://www.cbc.ca/news/business/apple-price-hike-ipad-macbook-ai-memory-chip-2026-9.7248577)
