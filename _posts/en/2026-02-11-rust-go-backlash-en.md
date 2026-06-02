---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Rust and Go Backlash Unfiltered
translated: false
type: note
---

**Question: Analyze this Weibo post in English.**

**Answer:**

The Weibo post (from February 2026 or earlier context) is a strongly opinionated, personal rant by an apparently retired/senior programmer expressing deep frustration and disdain toward the **hype cycles**, **community cultures**, and **technical choices** surrounding two popular modern languages: **Go** (earlier wave) and **Rust** (current wave).

### Core Claims and Arguments

1. **Historical Parallel: Go → Rust**
   The author sees Rust's current dominance and fan enthusiasm as a repeat of what happened with Go around 2010–2015. Both languages experienced (or are experiencing) explosive popularity, heavy marketing through meetups/hackathons, and a community atmosphere the author finds arrogant and unwelcoming.

2. **Technical Criticism**
   - **Go**:
     Solves mainly one thing well (lightweight concurrency via goroutines), but deliberately omits many "good" features from prior languages (generics — added much later; exceptions; etc.). This leads to verbose, repetitive, error-prone code. The author claims Go codebases become chaotic and worse than well-written C in practice. With many older languages now offering async/await or similar lightweight concurrency, Go has lost its unique selling point.
   - **Rust**:
     Overly complex design. The borrow checker and ownership model, while solving memory safety, impose heavy cognitive load and distract from the actual business problem. The author believes it does **not** elegantly solve memory management and instead creates new classes of difficulty.

3. **Community & Culture Critique (Main Theme)**
   - Language-specific meetups repeatedly disappoint: instead of deep technical discussion, they feature self-important speakers who brag about their background (e.g., "I used Haskell before, now Rust makes me elite").
   - Anecdotes:
     - Go meetup attendee condescendingly asking "Why are you here if you don't use Go?"
     - Rust speaker in Tokyo acting dominant (knocking on table).
     - A former "Haskell programmer" colleague who caused long delays, produced questionable designs, and later switched to zealously promoting Rust without delivering useful results.
   - Broader pattern: People who constantly emphasize which language they use tend to be lower-quality engineers. Companies that loudly advertise "We use Go/Rust" often have unpleasant, dogmatic atmospheres.
   - Prediction: Rust will produce similar negative outcomes (over-engineering, toxic internal culture, stalled projects) as previously seen with Scala and Go.

4. **Personal Stance & Motivation**
   The author admits bias (openly calls Go "shit", expects similar for Rust). They have written critical evaluations of Go and Scala before, and some readers (e.g., ex-Twitter employee) later confirmed the Scala critique matched reality.
   Now "retired" and free from job-seeking, the post serves as a warning / catharsis for people still suffering in such environments.
   Invites others to share real Go/Rust experiences to test whether the intuition holds.

### Overall Tone and Style
Very blunt, cynical, and anecdotal — relies heavily on personal stories rather than systematic evidence. Uses strong language ("arrogant", "self-important", "教条主义"/dogmatic, etc.) and shows clear contempt for language evangelism / tribalism.

### Is This View Uncommon?
No — similar complaints have circulated for years in English-speaking communities:
- Go is sometimes called "toxic" when any design criticism appears (defensive reactions).
- Rust has a long-standing reputation in some circles for having an arrogant / unwelcoming community (especially toward beginners on Stack Overflow, Discord, etc.), with frequent "fighting the borrow checker" burnout stories and accusations of zealotry.
- Programming-language tribalism/fanboyism is a well-known phenomenon across many languages (including Haskell, JavaScript frameworks, etc.).
The author's experiences align with recurring online discussions about language evangelism leading to cult-like meetup behavior and poor team cultures in companies that over-identify with one language.

In short, the post is a classic representative of the "old-school grizzled programmer vs. modern language hype" genre — skeptical of fashion-driven adoption, distrustful of communities that tie ego to language choice, and convinced that technical simplicity + pragmatism beats feature-heavy "safe" languages when real-world code quality and team dynamics are considered.

**References:**

- [Why is the Rust community often so arrogant? (Rust Users Forum, 2020)](https://users.rust-lang.org/t/why-is-the-rust-community-often-so-arrogant/51415)
- [Rust's Community Toxicity Is Driving Away Better Engineers Than It Attracts (Medium, 2026)](https://medium.com/@kp9810113/rusts-community-toxicity-is-driving-away-better-engineers-than-it-attracts-2b6df0165380)
- [Why the Go community is so toxic? (Reddit r/golang)](https://www.reddit.com/r/golang/comments/1bvl207/why_the_go_community_is_so_toxic/)
- [Rust vs Go community discussions and comparisons (various sources including Hacker News, forums)](https://news.ycombinator.com/item?id=30442235)
