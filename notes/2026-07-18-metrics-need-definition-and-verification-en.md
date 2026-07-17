---
audio: false
generated: true
image: false
lang: en
layout: post
title: Metrics Need Definition and Verification
translated: false
type: note
---

Question: Is the Cloudflare vs GoatCounter traffic difference related to why investors need to verify metrics, like the JPMorgan–Frank case?

Answer:

Yes, your reasoning is basically right. The core lesson is:

**A metric is not valuable until you define exactly what is being counted and prove the quality behind it.**

For website analytics:

* **Cloudflare Web Analytics** usually measures things closer to **page views / requests / visits depending on configuration**.
* **GoatCounter** focuses more on **visitor sessions / visits**.

Example:

```
One person:
    open homepage
    read article A
    click article B
    open article C

Cloudflare:
    3 page views

GoatCounter:
    1 visit
```

So your Cloudflare number can look much larger without being "fake". The measurement unit is different.

The same problem appears in startups:

```
Vanity metric:
    "We have 4 million users"

Investor question:
    "How many active users?"
    "How many verified humans?"
    "How many paid conversions?"
    "Retention after 30/90 days?"
    "Can users be contacted?"
```

The JPMorgan / Frank case you mentioned is exactly this type of failure. JPMorgan Chase acquired student financial aid startup Frank for about $175 million in 2021. JPMorgan believed Frank had around 4.25 million users, but prosecutors alleged the actual usable customer base was much smaller and that fake/synthetic data was created to support the inflated user numbers. ([SEC][1])

The "aha moment" was when JPMorgan tried to use the acquired customer data for marketing. The engagement did not match expectations: many emails bounced, and very few users engaged. ([TechCrunch][2])

This is exactly why due diligence exists:

```
Founder says:
    4.25M users

Acquirer asks:
    Show database
    Show event logs
    Show cohort retention
    Send test campaigns
    Verify random samples
```

A good technical audit would look like:

```sql
-- claimed users
SELECT COUNT(*) FROM users;

-- real engagement
SELECT COUNT(DISTINCT user_id)
FROM events
WHERE event_time > now() - interval '30 days';

-- retention
SELECT
    signup_month,
    count(*) users,
    count(active_users_30d) / count(*) retention
FROM cohorts;
```

The same applies to your blog:

A serious partner/investor should not only ask:

```
Monthly views: 70k
```

but:

```
Where from?
Organic vs bot?
Unique humans?
Returning visitors?
Newsletter subscribers?
Conversion?
Country distribution?
Time on page?
```

Especially now with AI crawlers:

```
Traditional traffic:
human -> browser -> page

AI traffic:
agent -> fetch docs -> summarize -> no human page view
```

Cloudflare seeing crawler activity and a human analytics tool seeing visits can diverge significantly.

So yes: **traffic numbers, follower counts, GitHub stars, downloads, "users" — all need definitions and verification.** The unit of measurement is part of the product story.

References:

* ([SEC][1])
* ([TechCrunch][2])
* ([Business Standard][3])

[1]: https://www.sec.gov/files/litigation/complaints/2023/comp25776.pdf?utm_source=chatgpt.com "Microsoft Word - 2023.07.12.SEC v Javice Amended Complaint v3"
[2]: https://techcrunch.com/2025/03/28/javice-found-guilty-of-defrauding-jpmorgan-in-175m-startup-purchase/?utm_source=chatgpt.com "Javice found guilty of defrauding JPMorgan in $175M startup purchase | TechCrunch"
[3]: https://www.business-standard.com/article/international/how-jpmorgan-was-cheated-of-175-million-by-a-teenage-prodigy-123012200812_1.html?utm_source=chatgpt.com "How JPMorgan was cheated of $175 million by a 'teenage prodigy' | INTERNATIONAL COMPANIES NEWS - Business Standard"
