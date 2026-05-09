---
audio: false
generated: true
image: false
lang: en
layout: post
title: Thariq Shihipar Prefers HTML over Markdown
translated: false
type: note
---

Question: How did Thariq Shihipar say that many of his peers on the Claude Code team no longer use Markdown?

Answer:

The specific claim about "many peers on the Claude Code team won't use Markdown" does not appear to be a direct quote from Thariq in any of his published writing. However, based on what the search results reveal, here is the full context of Thariq's position on Markdown vs. HTML, published on May 8, 2026:

## Who Is Thariq?

Thariq Shihipar is a member of the Claude Code team at Anthropic. He is a former YC founder who joined Anthropic about a year ago and bridges engineering, content, and customer feedback. His most notable engineering contribution is the "ask user question" tool that enables Claude to interactively elicit requirements in plan mode.

## What Thariq Actually Said

On May 8, 2026, Thariq posted: "HTML is the new markdown. I've stopped writing markdown files for almost everything and switched to using Claude Code to generate HTML for me." He published a companion essay titled **"The Unreasonable Effectiveness of HTML"** explaining why.

## Why He Argues Against Markdown

He argued that Markdown has clear limitations: files longer than 100 lines are hard to read, visual expression such as visualisation, colour, and diagrams are limited, sharing is inconvenient, and people edit files directly less often since editing is often delegated to Claude — so Markdown's biggest advantage has disappeared.

He cited four key advantages of HTML over Markdown:

1. **Information density** — HTML can represent tables, CSS design, SVG illustrations, JavaScript interactions, spatial data, and images. The inefficiency of Claude roughly expressing colours with Unicode characters or drawing ASCII diagrams in Markdown disappears in HTML.
2. **Ease of sharing** — Markdown is not natively rendered by browsers, so it must be sent as an attachment. HTML can be shared with a single link if uploaded to a place such as S3, making the likelihood that colleagues will actually open planning documents, reports, and PR manuals much higher.
3. **Two-way interaction** — In an HTML document, sliders or buttons can be added to adjust design options directly and paste the results back into Claude Code, which is not possible in Markdown.
4. **Deeper engagement** — He said: "Using HTML makes me much more deeply involved in what Claude does. I was worried that not reading planning documents in detail would mean having to leave decisions to Claude, but now I understand what Claude is doing much better than before."

## How He Uses HTML

He uses HTML for planning (placing draft options side by side in a single file for comparison), code reviews (an HTML-made guide better than GitHub's default diff view), design prototypes, reports, and custom editing interfaces like draggable cards and form-based settings editors — always with a button to copy the results.

## Downsides He Acknowledges

HTML takes 2 to 4 times longer to generate than Markdown, diffs are complex in version control, and it uses more tokens. His practical rule: ask for HTML when the output needs repeated reading, team review, status tracking, comparison, filtering, or follow-up editing. For disposable notes, stay with Markdown.

## The "Peers" Claim

The specific assertion that "many peers on the Claude Code team won't use Markdown" does not appear in any of the current search results or his published essay. It is possible you may have seen this paraphrased or misquoted in a secondary source, or it may come from a reply thread on X (Twitter) that requires login to access. What is confirmed is that Thariq himself personally made the switch and advocated for it publicly — but whether he explicitly attributed this sentiment to his broader team cannot be verified from publicly available sources.

References:

- [Thariq's HTML examples companion site](https://thariqs.github.io/html-effectiveness/)
- [Simon Willison's summary of the essay](https://simonwillison.net/2026/May/8/unreasonable-effectiveness-of-html/)
- [DigitalToday: Tech Insight — Stop using Markdown, move to HTML](https://www.digitaltoday.co.kr/en/view/54022/tech-insight-stop-using-markdown-move-to-html-why)
- [StableLearn: Claude Code Should Output HTML, Not Just Markdown](https://stable-learn.com/en/claude-code-html-output/)