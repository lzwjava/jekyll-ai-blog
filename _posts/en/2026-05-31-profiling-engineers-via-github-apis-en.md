---
audio: false
generated: true
image: false
lang: en
layout: post
title: Profiling Engineers via GitHub APIs
translated: false
type: note
---

Great question. Here's a systematic framework for profiling an engineer through public APIs:

```
=== How to Know an Engineer Through Their GitHub ===

1. PROFILE API  --  /users/{name}
   curl -s 'https://api.github.com/users/{name}'

   Reveals:
   - bio: self-description (usually 1 line of identity)
   - location: where they're based
   - company: current employer
   - blog: personal site (deep dive into this)
   - created_at: how long they've been on GitHub
   - public_repos / followers / following:
     ratio tells you producer vs consumer
     (many repos, few followers = builder, not promoter)

2. REPOS API  --  /users/{name}/repos?sort=stars&per_page=100
   curl -s 'https://api.github.com/users/{name}/repos?sort=stars&direction=desc'

   Reveals:
   - Languages: what they actually code in (not what they claim)
   - Stars: what the community values from them
   - Descriptions: how they think about their own work
   - Topics: what domains they tag themselves in
   - pushed_at: are they still active? or dormant since 2020?
   - Forks vs originals: contributor or creator?

   Patterns to look for:
   - Dotfiles/config repos = tooling nerd
   - Many tutorial/cheatsheet repos = learner/teacher
   - One big project vs many small ones = deep vs broad
   - Fork of popular project = contributing upstream

3. STARS API  --  /users/{name}/starred?per_page=30
   curl -s 'https://api.github.com/users/{name}/starred?per_page=30'

   This is GOLD. Stars reveal:
   - What they aspire to build (aspirational interests)
   - What ecosystem they're investing in
   - Their taste in tools and frameworks
   - Emerging interests (recently starred)

   Often more honest than repos -- repos show what they
   finished, stars show what they care about.

4. EVENTS API  --  /users/{name}/events?per_page=30
   curl -s 'https://api.github.com/users/{name}/events?per_page=30'

   Reveals:
   - Recent activity: what they're working on RIGHT NOW
   - Push events: which repos are actively developed
   - Issue/PR activity: do they collaborate or solo?
   - Watch events: what communities they follow

5. ORGS API  --  /users/{name}/orgs
   curl -s 'https://api.github.com/users/{name}/orgs'

   Reveals:
   - Company/team affiliations
   - Open source communities they belong to
   - Professional network

6. FOLLOWERS/FOLLOWING  --  /users/{name}/followers
   Reveals their professional network graph.
   Who follows them = who values their work.
   Who they follow = who they learn from.

7. PERSONAL SITE  --  {blog} from profile

   If they have blog/notes (like .github.io):
   - Writing reveals depth of thinking
   - Topics reveal what they care enough to write about
   - Technical posts > "what I learned" posts for skill level
   - Post frequency reveals consistency

8. LANGUAGE DISTRIBUTION

   Don't just count repos -- count RECENT repos.
   A dev with 20 Java repos but last 3 in Rust is
   a Rust developer now, not a Java one.

   Language timeline = career trajectory visible in data.

9. REPO NAMING & DESCRIPTIONS

   - Professional descriptions = corporate background
   - Emoji/quirky descriptions = startup/open-source culture
   - Chinese descriptions = likely China-based, bilingual
   - Academic terms = research background
   - No description = just ships, doesn't market

10. CONTRIBUTION GRAPH (not in API, but visible)

    github.com/{name} shows green squares:
    - Consistent = disciplined, daily coder
    - Bursty = project-driven, deadline-driven
    - Gaps = job change, burnout, or side projects
    - Weekend activity = passion project time

=== What Each Source Tells You ===

  Source          | Reveals
  ----------------+----------------------------------
  Profile bio     | Self-identity (1 line)
  Repos           | What they BUILT
  Stars           | What they ADMIRE / ASPIRE TO
  Events          | What they're doing NOW
  Orgs            | Who they WORK WITH
  Followers       | Who VALUES them
  Blog            | How they THINK
  Languages       | What they actually USE
  Topics          | What DOMAINS they care about
  Forks           | What they CONTRIBUTE TO
  Stars (recent)  | What they're LEARNING
  Created_at      | Seniority (years on platform)

=== Mutual Interest Detection ===

  Compare two engineers:
  1. Language overlap --> shared tech stack
  2. Star overlap --> shared interests (strongest signal)
  3. Topic overlap --> shared domains
  4. Common orgs --> same communities
  5. Common followers --> professional circle overlap

  Star overlap is the most honest signal because:
  - People star what genuinely interests them
  - No social pressure (stars are private-ish)
  - Shows aspiration, not just past work
```

Key insight: **Stars > Repos** for understanding someone's interests. Repos show what they finished under constraints (work, time, opportunity). Stars show what they actually care about — their genuine curiosity. When I profiled nocmk2, the starred repos (hermes-agent, openclaw, langfuse, opencode) painted a much clearer picture of his AI-agent obsession than his 55 repos (many empty or forked).

Want me to turn this into a reusable script or skill that auto-profiles any GitHub user?
