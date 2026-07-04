---
audio: false
generated: true
image: false
lang: en
layout: post
title: Model Performance Analysis at Validation 1.42 BPB
translated: false
type: note
---

Done. Results saved to `/mnt/data/zz/fineweb-code-sec-gpt/results.txt`. Quick summary:

**Observations — d12 (step 50k, val_bpb 1.418)**

| Domain | Quality |
| --- | --- |
| **Code (quicksort continuation)** | Good — continued `quicksort` correctly, generated `sort_2`, `sort_n` variants with realistic code structure |
| **Code (React DataFetcher)** | Decent — reproduced the component faithfully, generated a `fetch(url)` function that reuses same pattern |
| **Code (Go/merge sort/SQL)** | Weaker — regressed to prompt-echoing, hallucinated column names (`price_delivered`, `customer_id_delivered`), no real Go code |
| **SEC (revenue, risk)** | Reads plausible — continues SEC text with coherent financial tone, generates `Item 1B` header |
| **SEC (IFRS/GAAP)** | Falls apart — devolves into number repetition (`15,200, 172, 200`) and word salad |
| **General (water cycle)** | Good continuation — correctly adds "Water cycle is always the most common" with coherent reasoning about evaporation states |
| **General (compound interest)** | Weak — does `$10,000 / 30 = 75%` nonsense arithmetic |
| **General (autonomic, photosynthesis)** | Hallucinates — "photometry phototechnique", "pitty" as a branch of the nervous system |

**Conclusion:** At 1.42 val_bpb, the model has learned code syntax structure (indentation, function definitions, React hooks) and SEC document tone, but lacks factual knowledge and arithmetic reasoning. This is typical for a 286M param model — memorization capacity is limited. The code continuation tasks work best because they're pattern-matching on syntax rather than requiring factual recall.
