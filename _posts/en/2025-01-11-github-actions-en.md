---
audio: false
generated: false
image: false
lang: en
layout: post
title: Maximum Execution Time of GitHub Actions Job
translated: false
type: post
---

I've been using GitHub Actions to automate the translation of my blog posts. Initially, I attempted to translate all posts in a single job, with the changes committed back to the repository only after all translations were complete.

I was optimistic and went to sleep, expecting the process to finish. However, after 8 hours, I woke up to find the following error:

> The job running on runner GitHub Actions 12 has exceeded the maximum execution time of 360 minutes.

This meant that the 6 hours of translation work was lost, as the commit only happened at the end.

To address this, I modified the workflow to commit changes every 10 files.

Furthermore, I implemented multithreaded programming to reduce the total translation time from 6 hours to approximately one hour.

GitHub Actions offers a lot of flexibility. It supports multiple workflow jobs, allowing for the separation of tasks. Some jobs can be triggered on each commit, while others can be triggered by different events.
