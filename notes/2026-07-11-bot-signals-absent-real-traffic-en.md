---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bot Signals Absent, Real Traffic
translated: false
type: note
---

**Question:** Here's my actual GoatCounter dashboard breakdown (referrers, browsers, OS, locations, device sizes) for lzwjava.github.io — does this traffic profile look like real humans or is it still bot-contaminated?

**Answer:**

This dataset is actually good news — it doesn't look bot-contaminated. Let me break down why, signal by signal.

## The tell-tale bot signatures are absent

Scripted scraping/agent traffic almost always shows a **collapsed, unnatural distribution** — e.g., 95%+ single OS (usually `Linux`), a single fixed screen size, or one browser dominating at 99%. Your data shows the opposite: a naturally spread distribution across every axis:

- **OS**: iOS 31% / macOS 24% / Windows 21% / Linux 15% / Android 7% — this is what a real bilingual (English + Chinese) technical readership looks like, not what `curl`/`requests`/scraper farms produce (those cluster hard on Linux with zero mobile OS presence).
- **Device size**: Phones 39%, Computer monitors 54% — real people switching between reading on desktop and mobile. Headless-browser scrapers (Playwright/Puppeteer) almost always fix one viewport and never vary it.
- **Browser**: Chrome 54% / Safari 43% — matches expected iOS+macOS Safari share plus Chrome majority. No anomalous "Unknown" spike (only 1%), which is what you'd see if raw non-JS bots were slipping past GoatCounter's UA filter.

If this were mass AI-crawler traffic, you would not get this variance for free — most crawlers (GPTBot, ClaudeBot, Bytespider, etc.) don't execute JavaScript at all, so they never fire GoatCounter's beacon in the first place. What you're looking at is close to the true human floor.

## Referrer breakdown — decode the two that look weird

**`weixin110.qq.com` (6%, 225 visits)** — this is not a bot. It's an artifact of how WeChat's in-app browser works: when someone taps a link shared in a WeChat chat/group/Moments, WeChat routes it through its own link-safety-check redirector (`weixin110.qq.com`) before forwarding to the real destination. The `Referer` header your server sees is the redirector, not the actual WeChat share. **Translation: 225 real humans clicked your blog link from inside WeChat.** For someone targeting Greater Bay Area / HK clients, this is a meaningful organic-share signal worth paying attention to — find out *which* post/note is circulating in WeChat groups, because that's currently your highest-conversion discovery channel into the exact market you're targeting.

**Yandex (8%, 317) + ya.ru (1%, 24)** — correlates almost exactly with your Russia location bucket (16%, 619). Crawler traffic from `YandexBot` wouldn't set a `Referer` header at all (crawls don't carry referrers) — a `Referer: yandex.com` only fires on a real click-through from Yandex's search results page. So this is genuine organic search traffic: you apparently rank well in Yandex for some of your deep-learning/GPU notes, and there's a real Russian technical audience reading your English-language content. Not something to filter out — arguably worth understanding (which page ranks there?) since it's free distribution you didn't engineer.

**`chatgpt.com` (2%, 95)** — this is the actual agentic-traffic signal, and it's a *good* one to isolate: ChatGPT's own retrieval/browsing tool for RAG-style answers typically does a raw HTTP fetch (no JS execution), which means it would **never trigger a GoatCounter beacon**. If GoatCounter recorded 95 beacon fires with `Referer: chatgpt.com`, that most likely means 95 real humans asked ChatGPT something, got a link to your blog in the answer, and clicked through in a real browser. That's a legitimate top-of-funnel signal for your AI-consulting brand — people are discovering you through LLM-mediated search, not classic Google SEO.

## Page-level pattern also looks like real evaluation behavior, not crawl behavior

Your top pages (`/`, `/notes-zh`, `/resume-en`, `/ai-portfolio-zh`, `/ai-portfolio-en`, `/index-zh`, `/index-en`, `/portfolio-en`) trace a coherent human journey: land → check notes → check resume/portfolio. A crawler indexing your site systematically would hit pages roughly proportional to your sitemap/internal-link graph, not disproportionately favor `resume` and `ai-portfolio` pages over, say, your 400 blog posts or 8,000 notes pages. This distribution looks like people specifically evaluating you — which is exactly the funnel you want feeding Phase 1 consulting leads.

## What this means for the original 60k vs 4k question

This confirms my earlier read: GoatCounter's 3,832–4,000 is closer to your real human number, and the 60k in Cloudflare is very likely the zone-level **Analytics & Logs / Traffic overview** counting every raw HTTP request (bots, crawlers, AI training scrapers) hitting Cloudflare's edge — not the JS-beacon Web Analytics widget. If you want to confirm precisely instead of estimating, pull the `botScore` distribution for the same 30-day window from Cloudflare's GraphQL API (query from my earlier answer) and sum requests with `botScore > 30` — that subtotal should land close to this ~3,800–4,000 GoatCounter figure. If it does, you've fully closed the loop without needing a third tool.
