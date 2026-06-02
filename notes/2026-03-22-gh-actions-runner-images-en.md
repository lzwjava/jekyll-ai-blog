---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Runner Images for GitHub Actions
translated: false
type: note
---

Fixed. Here's what changed:

### The Problem

The old runner labels used `node:16-bullseye` — a bare Node.js image with no Python, no toolcache, nothing useful for GitHub Actions workflows. When `actions/setup-python` tried to install Python 3.13.2, it couldn't find a compatible prebuilt binary for that environment.

### The Fix

Switched to **[catthehacker/ubuntu](https://github.com/catthehacker/docker_images)** images — these are purpose-built for GitHub Actions emulation:

| Label | Image | Pre-installed |
|---|---|---|
| `ubuntu-latest` | `catthehacker/ubuntu:act-latest` | Node, Python, Go, Java, Ruby, PHP, etc. |
| `ubuntu-22.04` | `catthehacker/ubuntu:act-22.04` | Same, Ubuntu 22.04 base |
| `ubuntu-20.04` | `catthehacker/ubuntu:act-20.04` | Same, Ubuntu 20.04 base |

All three images are pre-pulled and cached. Runner is back online. Re-trigger your workflow — Python 3.13.2 should install fine now. 🦞
