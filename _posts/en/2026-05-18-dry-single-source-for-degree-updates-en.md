---
audio: false
generated: true
image: false
lang: en
layout: post
title: DRY Single Source for Degree Updates
translated: false
type: note
---

Good optimization — here's why and a post you can copy:

---

**The problem:** The associate degree progress (passed/pending exams) was duplicated in two files — `resume-en.md` and `associate-degree-en.md`. Every time you passed an exam, you had to update both. Inevitably they'd drift.

**The fix:** Resume is now the single source of truth. The associate degree post links to it via a clean anchor `#edu-gdufs`, so readers jump straight to the GDUFS entry. One update, both pages stay in sync.

---

Copy this:

---

I just deduplicated my associate degree progress across my site. Previously, the exam status (13 written passed, 3 practical passed, 5 + 2 pending) was copy-pasted between my resume page and the associate degree progress post. Every exam result meant double edits and drift risk.

Now the resume (`resume-en.md`) is the single source of truth — all detailed progress lives in its Educational Background section under a clean anchor `#edu-gdufs`. The progress post links there with one line:

`See Educational Background → GDUFS for the current exam status.`

One update, both pages stay in sync. Classic DRY for a personal site.

---
