---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Remote Branch Renaming
translated: false
type: note
---

Fixed. Here's the summary:

  Failed repo:  /Users/lzwjava/projects/rust (rust-lang/rust)
  Root cause:   Remote renamed default branch from `master` → `main`
                Your local `master` tracked `origin/master` which no longer exists,
                and the fetch refspec was hardcoded to `master` only.

  What I fixed:
    1. Renamed local branch:    master → main
    2. Fixed fetch refspec:     +refs/heads/master:... → +refs/heads/*:refs/remotes/origin/*
    3. Shallow-fetched origin/main (repo is ~3GB, full fetch times out)
    4. Set upstream tracking:   main → origin/main

  Status: now tracking origin/main (ahead 168, behind 1 due to shallow fetch).

Note: next time you do a full `git pull` on this repo it may take a while (rust-lang/rust is huge). A `git pull --depth=1` or `git fetch --depth=1` is faster if you don't need full history.