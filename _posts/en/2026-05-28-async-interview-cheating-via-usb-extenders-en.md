---
audio: false
generated: true
image: false
lang: en
layout: post
title: Async Interview Cheating via USB Extenders
translated: false
type: note
---

**Question:** For online coding interviews (HackerRank, LeetCode-style), can candidates cheat by using extended USB cables so a helper in another room controls the mouse/keyboard while the candidate sits visibly on camera?

**Answer:**

Yes, this is a real and known attack vector. Here's the full breakdown:

## The Attack

```
[Interviewer sees]          [What's actually happening]

Candidate on camera    →    Candidate sits idle / acts natural
Candidate's screen     →    Shared to helper via screen share app
                            Helper uses USB KVM extender to type
                            answers on candidate's machine remotely
```

**Hardware needed (~$30-100):**

- USB extension over Cat5/Cat6 (e.g., ATEN UCE3250, runs 50m)
- Or wireless USB extender
- Or simply: two machines + remote desktop (AnyDesk hidden, TeamViewer, etc.)

The hardware approach is almost undetectable because:

- No suspicious software running
- Candidate's hands visible on camera
- Candidate can even look like they're "thinking"

## Common Variants

| Method | Detection Difficulty | Cost |
| --- | --- | --- |
| USB KVM extender (physical cable) | Very hard | ~$50 |
| Remote desktop hidden in background | Medium | Free |
| Second machine with mirrored screen | Hard | Existing hardware |
| Phone propped up streaming screen to helper | Easy (camera angle) | Free |
| AI copilot (Claude/GPT in background) | Medium | $20/mo |

## Why Proctoring Fails Here

Most platforms (HackerRank, Codility, CoderPad) rely on:

- Webcam (only sees face/hands, not helper behind camera)
- Tab-switch detection (irrelevant if helper has own machine)
- Browser lockdown (bypassed by second machine entirely)

None of these catch a physical USB extender at all.

## What Actually Catches It

1. **Live technical interview follow-up** — ask them to explain their own solution line by line, modify it live, debug an edge case. Helper can't whisper fast enough.
2. **Unusual typing patterns** — smooth, no hesitation, no backspacing on hard problems.
3. **No "thinking out loud"** — competent engineers narrate; cheaters go quiet.
4. **Behavioral inconsistency** — aced the async problem, can't explain what a Promise is.
5. **In-person follow-up round** — the classic final filter.

## Industry Reality

Companies like Google, Meta, Jane Street know this. That's why:

- Top-tier companies always have a live human interviewer asking follow-ups
- Final rounds are in-person or via verified video with system share
- Coding screen is just a signal, not the verdict

The arms race between cheating methods and proctoring is basically unwinnable at the pure exam layer — which is why strong interview loops **don't rely solely on the async coding test**.
