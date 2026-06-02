---
audio: false
generated: true
image: false
lang: en
layout: post
title: Skip Parallel Testing for Now
translated: false
type: note
---

Summary: Sequential is the right choice here. Your 1860 tests run in ~8s already — parallel adds overhead without benefit at this scale. The `Bad file descriptor` errors in parallel mode suggest some tests do I/O that conflicts with process forking, but everything still passes. If you ever add slower tests (API calls, model loading), you can switch to `-n auto` since xdist is now in dev deps.
