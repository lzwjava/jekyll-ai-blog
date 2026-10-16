---
audio: false
generated: true
image: false
lang: en
layout: post
title: Developer Circles Live Feed
translated: false
type: note
---

**Fun Live (趣直播) should have a social feed where developers share what they build, learn, discover, and experience.** Think of a combination of WeChat Moments, X, and a developer community like GitHub — but focused on technology, AI, and knowledge sharing across China and the world.

The Chinese concept is **圈子 + 动态**.

- **圈子 (Circles):** Communities organized around interests, technologies, projects, or people.
- **动态 (Feed):** Posts shared by users, including text, images, videos, links, and code.
- **互动 (Interactions):** Likes, comments, reposts, and discussions.
- **直播 (Live):** Real-time technical sharing and interactive sessions.

## 1. Product experience

Imagine opening Fun Live on your phone.

### Home — Dynamic Feed

Users see posts from people they follow and circles they join.

Example posts:

**Zhiwei Li** · 10 min ago

> I've been experimenting with running LLMs on consumer GPUs. Today, I finally got my local inference environment working with an older NVIDIA Tesla card.
>
> Here are my setup and performance results.

📷 Three attached images showing the GPU setup, terminal output, and inference benchmarks.

❤️ 28 Likes · 💬 12 Comments · ↗ Share

---

**Alice Chen** · 1 hour ago

> I just released an open-source AI coding agent. It can execute tools, read files, and run tests locally.
>
> GitHub: [Project link]

📷 Project screenshots

🏷️ `AI Agents` `Open Source` `Python`

❤️ 56 Likes · 💬 19 Comments

---

**Bob Smith** · 3 hours ago

> Looking for developers interested in building an open-source alternative to traditional online education platforms. Let's discuss.

❤️ 15 Likes · 💬 8 Comments

The feed should support both casual social updates and substantive technical content.

## 2. Circles — Interest-based communities

Users can create or join circles.

| Circle | Description |
|---|---|
| 🤖 AI & LLMs | LLM training, inference, agents, and research |
| 🔥 PyTorch | Deep learning engineering and implementation |
| 🖥️ GPU Computing | CUDA, ROCm, GPU hardware, and performance |
| 💻 iOS Development | Swift, SwiftUI, and Apple platforms |
| 🌐 Open Source | Projects, contributions, and collaboration |
| 🚀 Indie Hackers | Startups, products, and independent development |
| 🇨🇳 China × Global | Cross-border collaboration and knowledge sharing |

Each circle has its own feed.

For example, joining the **AI & LLMs** circle lets you see posts from members discussing new models, sharing benchmark results, publishing research, and asking technical questions.

Users can also create private circles for teams or invite-only communities.

**Important distinction:** A circle is a community; a dynamic is an individual post. One user can belong to many circles and publish many dynamics.

## 3. Can users share images and pictures?

Absolutely. Image sharing should be a core feature, not an afterthought.

I would design the publishing interface around a simple question:

**What's happening in your world?**

Users can publish:

| Content type | Examples |
|---|---|
| Text | Thoughts, questions, experiences |
| Images | Screenshots, hardware, whiteboards, photos |
| Multiple images | Project progress, tutorials, benchmark comparisons |
| Videos | Demos, experiments, short tutorials |
| Links | GitHub repositories, blog posts, papers |
| Code snippets | Commands, code samples, technical solutions |
| Live events | Announcements for upcoming technical livestreams |

For images, support uploading multiple pictures in a single post, with an interactive image viewer.

Useful details:
- Automatic image compression and thumbnail generation.
- Full-screen image viewing.
- Multiple-image grids.
- Captions and descriptions.
- Image deletion and post editing.
- Optional image alt text.
- Upload progress and retry handling.

For example, a developer repairing a GPU could post pictures of the PCB, measurements, and final test results. An LLM researcher could share training curves, GPU utilization graphs, and inference benchmarks.

These are valuable contributions to a developer community.

## 4. Three feed views

I would start with three tabs.

**Following**

Posts from people you follow.

This makes Fun Live feel personal, similar to WeChat Moments or X.

**Circles**

Posts from communities you have joined.

This makes it easier to discover discussions about AI, programming, and other technical topics.

**Discover**

Recommended posts from across the platform.

This helps new users find interesting developers, projects, and communities without needing to know anyone beforehand.

You don't need a complicated recommendation algorithm initially. Start with chronological feeds, followed accounts, circle membership, and a basic ranking system.

## 5. How it connects to Fun Live

The most important product decision is that **the social feed should reinforce the livestreaming platform rather than become a completely separate product.**

Consider the relationship:

```text
                 Fun Live
                    |
       +------------+------------+
       |            |            |
    Circles       Feed        Live
       |            |            |
   Communities   Posts       Livestreams
       |            |            |
       +------------+------------+
                    |
               Developers
                    |
       Knowledge sharing and discovery
```

A typical user journey:

1. A developer publishes a post about an interesting PyTorch experiment.
2. Other developers discover it in their feeds.
3. They comment, ask questions, and follow the author.
4. The author announces a livestream explaining the experiment.
5. The livestream attracts an audience.
6. Viewers share their own experiences and continue the discussion in the circle.
7. The community becomes more valuable over time.

This creates a natural growth loop: **posts attract users, livestreams create deeper engagement, and communities encourage users to return.**

It also gives you more opportunities to distribute technical knowledge beyond China.

## 6. Suggested mobile UI

For the iOS app, I would start with this bottom navigation:

```text
┌─────────────────────────────────┐
│ Fun Live                    🔍  │
├─────────────────────────────────┤
│ Following   Circles   Discover  │
├─────────────────────────────────┤
│                                 │
│ 👤 Zhiwei Li                    │
│    10 min ago                   │
│                                 │
│    Experimenting with local     │
│    LLM inference on GPUs...     │
│                                 │
│    ┌──────────┬──────────┐      │
│    │  GPU     │ Terminal │      │
│    │  Photo   │ Results  │      │
│    └──────────┴──────────┘      │
│                                 │
│    ♡ 28     💬 12     ↗ Share   │
│                                 │
├─────────────────────────────────┤
│                                 │
│ 🏠 Home  ◉ Circles  ＋  🔔  👤 │
└─────────────────────────────────┘
```

The central `+` button opens the publishing interface.

Users can choose to publish a post, upload pictures, share a link, or announce a livestream.

The feed itself should feel familiar, with readable typography, clean image layouts, and lightweight interactions.

## 7. MVP: What I would actually build

Don't build an entire social network on day one.

Start with these features:

1. User profiles and following.
2. Create, edit, and delete posts.
3. Text and multiple-image uploads.
4. Likes and comments.
5. Create and join circles.
6. Circle feeds and the personal following feed.
7. Share posts and livestream announcements.
8. Basic reporting, blocking, and moderation.

Defer complex recommendation algorithms, private messaging, elaborate badges, and sophisticated gamification.

For your existing iOS project, native SwiftUI is a reasonable choice if you want a polished Apple experience. A backend API can serve both iOS and a future web client.

A minimal data model might look like this:

```sql
CREATE TABLE posts (
    id          BIGSERIAL PRIMARY KEY,
    author_id   BIGINT NOT NULL,
    content     TEXT NOT NULL DEFAULT '',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE post_media (
    id          BIGSERIAL PRIMARY KEY,
    post_id     BIGINT NOT NULL REFERENCES posts(id),
    media_url   TEXT NOT NULL,
    media_type  TEXT NOT NULL,
    position    INT NOT NULL DEFAULT 0
);

CREATE TABLE circles (
    id          BIGSERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT ''
);

CREATE TABLE circle_members (
    circle_id   BIGINT NOT NULL REFERENCES circles(id),
    user_id     BIGINT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (circle_id, user_id)
);

CREATE TABLE post_circles (
    post_id     BIGINT NOT NULL REFERENCES posts(id),
    circle_id   BIGINT NOT NULL REFERENCES circles(id),
    PRIMARY KEY (post_id, circle_id)
);
```

Add separate tables for follows, likes, comments, and livestreams.

For media, store the actual images in object storage rather than PostgreSQL. The database holds their URLs and metadata.

One design decision worth making early: **allow a post to belong to multiple circles, or publish it to a user's general feed.** This gives developers flexibility without forcing every post into a single community.

---

## My recommendation

Position the feature as **Fun Live Circles: a global community for developers to share knowledge, projects, and everyday technical discoveries.**

WeChat Moments provides a familiar social interaction model. GitHub inspires technical collaboration. Reddit demonstrates the value of interest-based communities. Fun Live can connect these experiences with technical livestreaming and AI-powered translation.

The differentiator isn't simply that people can post pictures. It's that a developer in China can share an experiment, a developer in the US can discover it, and both can learn from each other or meet through a livestream.

**I'd next turn this concept into a concrete SwiftUI screen specification for your existing `live-ios` app, including the feed, circle detail, image composer, and post detail screens.**