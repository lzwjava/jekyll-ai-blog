---
audio: false
generated: true
image: false
lang: en
layout: post
title: PyPI Namespaces and Typosquatting Risks
translated: false
type: note
---

No, not quite. Here's how PyPI (the official Python Package Index) works:

**Anyone can publish packages, but only to their own namespace:**

- You create a free account at pypi.org
- You can publish any package with a name that isn't already taken
- Once you own a package name, only you (and collaborators you grant access to) can publish new versions

**What prevents abuse:**

- Package names are first-come, first-served
- You can't publish to a name someone else owns
- PyPI has policies against name squatting and typosquatting
- Malicious packages get reported and removed, but there's no pre-screening

**The real risk — typosquatting:**

- Attackers register names similar to popular packages (e.g., `reqeusts` instead of `requests`)
- This is a known supply chain attack vector
- PyPI has tooling to detect and remove obvious cases, but it's reactive not proactive

**So the answer is:** Yes, anyone can publish packages, but you can't overwrite or hijack an existing package you don't own. The danger is in new/similar names, not in taking over established ones.

This is why `pip install` from untrusted sources or with typos can be risky.
