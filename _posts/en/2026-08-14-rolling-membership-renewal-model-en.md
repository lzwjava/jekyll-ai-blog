---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rolling Membership Renewal Model
translated: false
type: note
---

Question: How should a 299 CNY/year community membership handle different parents joining at different times and yearly renewal?

Answer:

For a community, **do not use calendar-year membership**.

Bad model:

```
Jan 1 - Dec 31
299 CNY/year

Parent joins Nov:
pay 299
only gets 2 months
```

This feels unfair.

Use **rolling 12-month membership**.

Example:

```
Join: 2026-08-14

Payment:
299 CNY

Expire:
2027-08-14
```

Every member has their own renewal date.

This is how most SaaS subscriptions work.

---

Implementation:

Database:

```sql
users
-----
id
name


subscriptions
-------------
user_id
start_date
expire_date
status
```

When payment succeeds:

```python
if user.subscription_expire > now:
    new_expire = old_expire + timedelta(days=365)
else:
    new_expire = now + timedelta(days=365)
```

---

For community psychology, you can also add:

## Founding member

First 100 parents:

```
Founding Member
299 CNY/year forever
(or locked price)
```

This creates urgency.

Example:

```
AI Kids Community

Founding 100 families:
299/year

After:
499/year
```

---

## Another model: monthly + annual

Better for testing:

```
Free:
- read content
- join public events

299/year:
- private WeChat group
- weekly AI workshop
- project sharing

999/year:
- small group mentoring
- monthly child project review
```

---

The important thing:

Don't optimize the payment system first.

The first goal:

```
100 parents
    |
    |
high trust
    |
    |
parents invite friends
```

A 299 CNY/year community is basically a **trust product**.

If parents feel:

> "This community helps my child grow, and I know the people inside."

then 299/year is extremely cheap.

If it feels like:

> "Another AI course advertisement group."

then even 99/year is expensive.

---

A possible growth loop:

```
Free AI newsletter
        |
        v
WeChat public group
        |
        v
Weekly AI family meetup
        |
        v
299/year membership
        |
        v
Kids publish projects
        |
        v
Parents share screenshots
        |
        v
New families join
```

The community itself becomes the marketing channel.
