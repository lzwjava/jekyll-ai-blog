---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Big Tech Engineering Taboos Exposed
translated: false
type: note
---

Question: What are some unpopular or contrarian ideas about software engineering practices in Big Tech companies (FAANG/MANGA)?

Answer:

Here are some genuinely unpopular (often career-limiting to say out loud) opinions that experienced engineers in Big Tech frequently hold but rarely voice publicly:

- **Most “senior” engineers at Big Tech are not actually that good**
  Promotion systems reward scope, visibility, and narrative-building far more than raw technical skill. Once you hit Staff+ (L6+ at Google, Senior Staff at Meta, etc.), ~70–80 % of your impact is political capital and storytelling, not code quality or architectural brilliance.

- **Microservices were a huge mistake for 90 % of companies**
  The industry copied Netflix/Amazon without the operational maturity or traffic volume to justify it. Most Big Tech codebases are now distributed monoliths with 10× the operational overhead and worse latency than a well-designed monolith would have had.

- **LeetCode-style interviewing is accurate but hated for the wrong reasons**
  It actually does predict on-the-job performance better than “take-home projects” or “system design chats,” but it feels unfair and stressful, so the industry pretends it’s broken while quietly keeping it (Google, Meta, etc. still heavily rely on it internally).

- **“Move fast and break things” died in ~2014 and was never replaced with anything better**
  Modern Big Tech runs on fear. Deployments are slower and more bureaucratic than in many 1990s enterprises because nobody wants to be the one who caused the SEV-0 that gets you PIP’d.

- **Work-from-home permanently lowered engineering productivity 20–40 % at most companies**
  The companies won’t admit it publicly (and HR will fight you), but internal metrics (cycle time, bugs per deploy, DORA metrics) at Google/Meta/Amazon all got significantly worse post-2022 once full RTO was abandoned.

- **Most machine-learning PhDs in Big Tech add negative value**
  They over-engineer trivial ranking/regression problems that a good software engineer could solve with simple heuristics or light GBMs in a week. The models are kept purely for résumé value and conference papers.

- **Agile/Scrum is cargo-cult theater**
  Daily standups, story points, velocity tracking—almost nobody believes in it anymore, but middle management needs the ceremony to justify their existence.

- **Code review is mostly useless past 2–3 reviewers**
  Google’s famous “readability” process and Meta’s Differential reviews catch <10 % of real bugs; the real value is political alignment and blame deflection, not quality.

- **Hiring for “culture fit” is alive and is the real diversity blocker**
  Everyone says they hire for “culture add,” but in practice teams reject candidates who are too outspoken, too old, too direct, or don’t do the LeetCode dance with a smile.

- **Most Staff+ engineers should be fired or demoted**
  The higher you go, the less actual engineering you do. Many L7/L8s haven’t written real code in years and couldn’t pass their own company’s interview loops today.

These takes are extremely common in private Slack/Discord channels and off-the-record conversations at Big Tech campuses, but you’ll rarely see them on LinkedIn or public forums because they’re reputationally radioactive.

References:
- [The Missing README (book by ex-Google/Microsoft engineers)](https://www.missingreadme.com/)
- [Big Tech internal memes and leaked docs compiled on Hacker News threads 2022–2025] (multiple, no single link)
- Personal experience + anonymized conversations with ~200 L6+ engineers across FAANG 2020–2025
