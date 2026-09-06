---
audio: false
generated: true
image: false
lang: en
layout: post
title: Singapore GA4 Bot Traffic Anomaly
translated: false
type: note
---

Question: **Analyze this GA4 city data. Why is Singapore so huge, and what is the reality behind it?**

Answer: **The Singapore traffic is almost certainly not 28,000 real human readers. It looks like a GA4 bot/spam/automated-traffic anomaly.**

Your CSV is for **Aug 10 – Sep 6, 2026**, and the pattern is extremely strong.

### 1. Singapore completely dominates the dataset

You have:

| City             | Active users |     Share |
| ---------------- | -----------: | --------: |
| Singapore        |   **28,311** | **87.2%** |
| `(not set)`      |          666 |      2.1% |
| Shenzhen         |           57 |     0.18% |
| Shanghai         |           46 |     0.14% |
| Beijing          |           45 |     0.14% |
| Guangzhou        |           43 |     0.13% |
| Los Angeles      |           25 |     0.08% |
| All other cities |       ~3,300 |      ~10% |

So **Singapore alone accounts for ~87% of all active users** in this report.

That would be extraordinary for a technical/AI blog unless you had deliberately launched a Singapore-focused campaign.

But the *behavior* tells us much more.

---

### 2. The Singapore users behave like machines

This is the strongest evidence:

**Singapore:**

```text
Active users:                       28,311
Engaged sessions:                    2,143
Engagement rate:                    7.62%
Engaged sessions / user:            0.0757
Average engagement time / user:     0.0416
Events:                              85,108
```

Compare that with Los Angeles:

```text
Active users:       25
Engagement rate:    77.2%
Engagement time:    153.2
```

And Shenzhen:

```text
Active users:       57
Engagement rate:    52.2%
Engagement time:    64.5
```

The contrast is enormous.

If Singapore were genuine human traffic, you'd expect at least some reasonable engagement.

Instead:

> **28,311 "users" → only 2,143 engaged sessions → ~0.04 seconds average engagement**

That is basically the fingerprint of automated traffic.

---

### 3. There is actually a known GA4 problem involving Singapore

This is particularly interesting.

Google Analytics users have reported a **large wave of anomalous GA4 traffic from China and Singapore** since late 2025.

Google's Analytics community has specifically documented unusual China/Singapore traffic, with users reporting huge spikes and extremely low engagement. Google representatives/community experts have acknowledged gaps where some automated traffic isn't caught by the normal bot filtering. ([Google Help][1])

So your data isn't an isolated weirdness.

The important point is:

**GA4's built-in bot filtering does not mean "all bots are removed."**

Google says known bots/spiders are automatically excluded, but that only covers traffic Google can identify. ([Google Help][2])

---

### 4. Why specifically Singapore?

This is the interesting part.

There are several possible mechanisms.

#### A. Singapore is a major hosting / proxy / network hub

Singapore is a major Internet infrastructure location in Asia.

A bot doesn't necessarily run in the country where its operator lives.

For example:

```text
operator in China
       ↓
cloud/VPS/proxy
       ↓
Singapore IP
       ↓
your GA4 measurement
```

GA4 sees the **source IP**, not the physical identity of the person operating the bot.

Google explicitly says GA4 geography is approximated from the IP address of the traffic. ([Google Help][3])

So:

> "Singapore" in GA4 does **not** necessarily mean "Singaporean person reading my blog."

It means roughly:

> "The IP associated with this traffic geolocates to Singapore."

---

### 5. More importantly, some of this traffic may never have visited your website

This is the really weird part of modern GA4 spam.

An attacker can potentially send events directly to Google's Analytics collection/measurement infrastructure rather than behaving like:

```text
bot → your website → JavaScript → GA4
```

It can instead look conceptually like:

```text
bot
  ↓
GA4 measurement endpoint
  ↓
your Measurement ID
```

So your web server may not even see the traffic.

That explains why **Cloudflare/server logs can sometimes look normal while GA4 says you suddenly have tens of thousands of users**.

Google Analytics community discussions around the China/Singapore anomaly specifically mention this possibility. ([Google Help][4])

---

### 6. Your city distribution actually has another clue

Look at these:

```text
The Dalles          79
Council Bluffs      23
Ashburn             19
Glenview            27
```

Those aren't random cities.

They are strongly associated with **US Internet/cloud infrastructure**.

Then you have:

```text
Singapore            28,311
```

This makes the distribution look much more like:

```text
Internet infrastructure / automated traffic
```

rather than:

```text
real readers geographically distributed around the world
```

Your genuine human traffic seems to be the much smaller population scattered across:

```text
Shenzhen
Shanghai
Beijing
Guangzhou
Hong Kong
Los Angeles
San Jose
...
```

---

## 7. The most important distinction

I would separate your GA4 traffic into:

### Layer 1 — probably genuine users

For example:

```text
Shenzhen
Shanghai
Beijing
Guangzhou
Hong Kong
Los Angeles
San Jose
...
```

These have much more plausible engagement patterns.

For example:

**Los Angeles**

```text
25 users
77.2% engagement
153 seconds/user
3.8 engaged sessions/user
```

That's extremely different from Singapore.

### Layer 2 — suspicious automated traffic

Singapore:

```text
28,311 users
7.6% engagement
~0.04 engagement-time metric
0.0757 engaged sessions/user
```

This is the traffic I would **not use for monetization, audience analysis, SEO conclusions, or business decisions.**

---

## 8. So your real traffic is probably much smaller than GA4 says

This is the key conclusion.

If GA4 tells you:

> **32,461 active users**

I would **not** currently interpret that as:

> "My site has 32k real users."

A much more defensible interpretation is:

```text
GA4 reported users
        ↓
~28k suspicious Singapore traffic
        ↓
remove / segment it
        ↓
remaining traffic ≈ actual audience
```

The remaining ~4k is still not automatically 100% human, but it is much more plausible.

And this matters enormously for the advertising work you've been doing.

If you're applying to **Monumetric / Ezoic / AdSense alternatives**, you should **not present the 32k GA4 number as genuine human traffic** until you've cleaned this anomaly.

---

## 9. Don't simply conclude "Singapore has 28k people reading my blog"

That would be the wrong mental model.

Think of GA4 as:

```text
                    ┌── real users
Browser ────────────┤
                    ├── crawlers
                    ├── automation
                    ├── fake/spam events
                    └── Measurement Protocol abuse
                              ↓
                             GA4
                              ↓
                      "Active users"
```

GA4 is an **event measurement system**, not a ground-truth census of humans.

And its city dimension is only an IP-based approximation. ([Google Help][3])

---

## 10. What I would check next

The CSV you gave me is enough to identify the anomaly, but **not enough to identify exactly what generated it**.

The killer dimensions would be:

```text
City
+
Date
+
Traffic source / medium
+
Landing page
+
Browser
+
OS
+
Device category
+
Hostname
+
Page path
+
Event name
```

Especially:

```text
Singapore
→ session source / medium
→ browser
→ OS
→ page path
```

If you see something like:

```text
Singapore
direct / none
Chrome
Windows
one-second visits
same page
same user agent
```

or:

```text
Singapore
unknown referral
Chrome
0-second engagement
thousands of users/day
```

then we can almost fingerprint the traffic mechanism.

### Bottom line

**I would treat the Singapore 28,311 as suspicious/non-human until proven otherwise.**

The strongest evidence isn't simply that it's Singapore. It's the combination:

```text
87% of all users
+
7.6% engagement
+
~0.04 engagement-time metric
+
0.075 engaged sessions/user
+
85k events
+
known 2025–2026 GA4 China/Singapore anomaly
```

That's far too pathological to represent 28k normal readers.

Google's own documentation confirms that city is IP-derived, while Google's Analytics community has documented this specific China/Singapore bot-traffic phenomenon. ([Google Help][3])

References:

* [Google Analytics — Geography dimensions](https://support.google.com/analytics/answer/9268042?hl=en)
* [Google Analytics — China/Singapore bot traffic discussion](https://support.google.com/analytics/thread/378622882/google-analytics-4-bot-traffic-increase-from-china-singapore-on-wordpress-sites?hl=en-GB&utm_source=chatgpt.com)
* [Google Analytics — Filtering and bot traffic](https://support.google.com/analytics/answer/10227574?hl=en&utm_source=chatgpt.com)

If you want, I can next **analyze the CSV statistically and produce a "real users vs suspicious users" estimate, including the top suspicious cities and their behavioral fingerprints**.

[1]: https://support.google.com/analytics/thread/378622882/google-analytics-4-bot-traffic-increase-from-china-singapore-on-wordpress-sites?hl=en-GB "Google Analytics 4 Bot Traffic Increase from China / Singapore on WordPress Sites - Google Analytics Community"
[2]: https://support.google.com/analytics/answer/10227574?hl=en&utm_source=chatgpt.com "Filter, report on, or restrict access to data subsets - Analytics Help"
[3]: https://support.google.com/analytics/answer/9268042?hl=en "[GA4] Predefined user dimensions - Analytics Help"
[4]: https://support.google.com/analytics/thread/407327230/persistent-bot-traffic-spikes-bypassing-standard-ga4-filters?hl=en&utm_source=chatgpt.com "Persistent bot traffic spikes bypassing standard GA4 filters. - Google Analytics Community"
