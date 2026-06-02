---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Android Naming Conventions for Readability
translated: false
type: note
---

I agree! Android's naming conventions are excellent examples of clear, readable code. Here are the key principles they follow:

## Why Whole Words Work Better

**Good examples from Android:**
- `wrap_content` not `wrp_cnt`
- `match_parent` not `mtch_prnt`
- `onClickListener` not `onClkLstnr`

**The benefits:**
- **Instantly readable** - no mental translation needed
- **Searchable** - you can grep for `wrap_content` easily
- **Self-documenting** - new developers understand immediately
- **Avoids ambiguity** - `btn` could be "button" or "between"

## The Sweet Spot: Short AND Clear

The best names are both concise and complete:
- `src` vs `source` - `src` is universally understood
- `temp` vs `temperature` - context makes `temp` clear
- `config` vs `configuration` - common abbreviation, widely known
- `id` vs `identifier` - `id` is the standard

## When Abbreviations Are Okay

Abbreviations work when they're:
1. **Domain standard** - `html`, `json`, `api`, `url`
2. **Universally known** - `max`, `min`, `avg`
3. **Very common** - `num`, `str`, `err`

## When to Use Full Words

Always prefer full words for:
- **Business logic** - `calculateInvoiceTotal` not `calcInvTot`
- **Domain concepts** - `customerAddress` not `custAddr`
- **Less common terms** - `threshold` not `thrshld`

The guiding principle: optimize for reading, not writing. Code is read 10x more than it's written.
