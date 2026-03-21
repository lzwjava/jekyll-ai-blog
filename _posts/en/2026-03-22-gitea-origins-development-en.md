---
audio: false
generated: true
image: false
lang: en
layout: post
title: Origins and Development of Gitea
translated: false
type: note
---

**Question:** Who made Gitea, especially the self-hosted version?

**Answer:**

## Origins: Gogs → Gitea

Gitea did not start from scratch. It originated as a fork of **Gogs** in 2016. While Gogs was open-source, its repository was controlled by a single maintainer. This single-maintainer bottleneck frustrated contributors who wanted faster development and a more open governance model.

In response to these limitations, the Gitea developers decided to fork Gogs in **November 2016**, creating a community-driven development model. Gitea had its official **1.0 release in December 2016**.

---

## Who Made It

The key figures behind Gitea are:

- **Lunny Xiao** — one of the original core developers and maintainers of Gitea, and previously involved with Gogs.
- **Matti Ranta** — another core maintainer.

In **October 2022**, maintainers **Lunny Xiao** and **Matti Ranta** founded the company **Gitea Limited** with the goal of offering hosting services using specialized versions of Gitea that were not released as open-source. This commercialization move caused controversy in the community.

Beyond these founders, Gitea is developed under a community-driven development model, meaning it has many open-source contributors across the world, not just a single owner.

---

## What Is It (Self-Hosted)

Gitea is a painless, self-hosted, all-in-one software development service. It includes Git hosting, code review, team collaboration, package registry, and CI/CD. It is similar to GitHub, Bitbucket, and GitLab.

The goal of the project is to make the easiest, fastest, and most painless way of setting up a self-hosted Git service. As Gitea is written in **Go**, it works across all the platforms and architectures that are supported by Go, including Linux, macOS, and Windows on x86, amd64, ARM, and PowerPC architectures.

It is free, self-hosted, and licensed under the **MIT license**, giving users full control, unlimited users and repositories.

---

## The Forgejo Fork (Community Reaction)

In response to the founding of Gitea Limited and its non-open-source specialized versions, **Codeberg** — one of the major forges using Gitea at the time — forked Gitea into **Forgejo**. Forgejo is now a popular purely community-driven alternative for those who want a 100% open governance model.

---

## Summary Table

| Item | Detail |
|---|---|
| Original fork from | Gogs (November 2016) |
| Key founders | Lunny Xiao, Matti Ranta |
| Language | Go + TypeScript |
| License | MIT |
| Company | Gitea Limited (founded 2022) |
| Community fork | Forgejo (by Codeberg) |

**References:**

- [Gitea - Wikipedia](https://en.wikipedia.org/wiki/Gitea)
- [Gitea Official Documentation](https://docs.gitea.com/)
- [Gitea GitHub Repository](https://github.com/go-gitea/gitea)