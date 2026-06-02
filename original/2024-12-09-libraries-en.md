---
audio: false
generated: false
image: false
lang: en
layout: post
title: Consider Upgrades When Using Libraries
type: post
---

I used CodeIgniter in my startup project, [Fun Live](https://github.com/lzwjava/live-server). Although the project ended, after several years, I wanted to revive it to commemorate it. However, back in 2016, I used CodeIgniter 3, while the latest version is now CodeIgniter 4.

Upgrading has proven troublesome because my code is closely coupled with the CodeIgniter framework. Following the upgrade guide at  [https://codeigniter4.github.io/CodeIgniter4/installation/upgrade_4xx.html](https://codeigniter4.github.io/CodeIgniter4/installation/upgrade_4xx.html) shows that it requires significant effort to update the codebase.

This experience taught me an important lesson: when writing code, we should carefully consider how to handle future updates. It's crucial to think about which parts of the code we control and which parts are controlled by third-party dependencies.
