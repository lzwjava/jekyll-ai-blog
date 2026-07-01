---
audio: false
generated: true
image: false
lang: en
layout: post
title: Confluence Alternatives for Public Wikis
translated: false
type: note
---

**Question:** Does Confluence have a public/world-accessible version like GitHub does? What's the closest alternative — Substack, Medium, Quora?

**Answer:**

## Confluence: No Public "World" Version

Confluence is **purely enterprise** — Atlassian never made a public-facing, community-hosted variant. GitHub has github.com where anyone can create free repos. Confluence has no equivalent. Your options are:

- **Confluence Cloud** (atlassian.net) — enterprise SaaS, behind auth walls
- **Confluence Data Center** — self-hosted, still private by default
- No "public.confluence.com" equivalent exists

## What Confluence Actually Is (Functionally)

Structured, hierarchical **wiki + knowledge base** with:

- Spaces → Pages → Child Pages
- Rich embeds (Jira tickets, diagrams, code blocks)
- Team collaboration, comments, page history
- Access control per space/page

## Closest Public Alternatives, Ranked by Use Case

| Tool | Best For | Confluence Overlap |
| ------ | ---------- | ------------------- |
| **Notion** (notion.so) | Wiki + docs, public pages possible | Highest — spaces, databases, hierarchy |
| **GitBook** | Technical docs, public by default | High — dev teams use this as public Confluence |
| **GitHub Wiki** | Per-repo docs | Medium — markdown-only, no rich structure |
| **GitHub Pages / Jekyll** | Published static docs/blog | Medium — what you're already doing at lzwjava.github.io |
| **Obsidian Publish** | Personal knowledge base, public | Medium — your notes-en use case exactly |
| **BookStack** | Self-hosted wiki | High structural match |
| **Wiki.js** | Self-hosted, public-friendly | High |

## Substack / Medium / Quora — Not Really

These are **content publishing platforms**, not knowledge bases:

- **Substack** → newsletter-first, linear posts, no hierarchy
- **Medium** → articles, no structured wiki concept
- **Quora** → Q&A, crowd-sourced, not your knowledge

They overlap with Confluence's "page" concept only superficially. No spaces, no nested hierarchy, no version-controlled structured docs.

## For Your Specific Use Case

You're already doing the right thing — **lzwjava.github.io** (Jekyll/GitHub Pages) is effectively your public Confluence alternative. It's:

- Version-controlled (Git)
- Hierarchical (categories, tags)
- Publicly indexable
- Free and self-owned

If you wanted richer structure, **GitBook** (free tier, public spaces) or **Obsidian Publish** ($8/mo) would be the closest upgrades. GitBook in particular is what most open-source projects use when they need "Confluence but public."
