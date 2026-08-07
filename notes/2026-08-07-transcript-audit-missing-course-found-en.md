---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Transcript Audit: Missing Course Found"
translated: false
type: note
---

Checked the official transcript `011222300077-3.pdf` (printed 2026-08-07). Here's what's going on:

## The difference is exactly one course: 08074

The official 考生信息简表 for **610201 计算机应用技术** lists **17 passed courses: 14 written + 3 practical**. Your blog table lists **16: 13 written + 3 practical**.

| # | Course | Score | Session | In blog? |
|---|--------|-------|---------|----------|
| 14 | **08074 计算机高级程序设计** (Advanced Computer Programming) | **74** | **202604** | ❌ missing |

All 13 blog written courses (00012, 00342, 02142, 02323, 00022, 02120, 02316, 00040, 02318, 15042, 08553, 13167, 14567) appear on the transcript. The only extra one is **08074, 74 points, 2026.04**.

## What happened

- **08074 is a bachelor-degree course** — it's in your `2026-02-05-bachelor-degree-en.md` under the 080901 Computer Science plan (with 08075 practical), and it was in your **April 2026 exam plan**.
- You passed it (74) in the 2026.04 session, and Guangdong recorded it on your **associate transcript** too (same 准考证号), so it shows up here.
- Side note: your bachelor file's "Passed Courses" table records this pass as **"13793 Fundamentals of Computer Programming, 74, 202604"** — that code is wrong; the official record says **08074** (13793 is the associate's new code). Worth fixing.

## Other discrepancy (small)

- The 3 practical courses on the transcript show exam time **202605** (May), but the blog says **202604**. Grades match (优秀/及格/及格). The "Detailed Exam Results" pass dates should also be 202605.

## What to do

1. **Verify on the official system** (<www.eeagd.edu.cn/selfec>, verification code `ZKI202608070112223000771701`) whether 08074 counts toward the associate degree via substitution — the transcript is authoritative either way.
2. If it counts, add `08074 | Advanced Computer Programming | 202604 | Exam | 74 | 3` to the blog's Passed courses table. GPA would tick up slightly: **2.22 → 2.23** (adds 2.4 × 3 = 7.2 pts → 127.2/57).
3. Fix the practical dates to 202605, and fix the bachelor file's 13793 → 08074 mislabel.

Want me to apply these updates to the blog and bachelor files?
