---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Epoxy That Ruined Musk's Shoes
translated: false
type: note
---

Yes, this story is basically true. It comes from the early SpaceX **Merlin engine development** period around late 2003. The details are from accounts by Tom Mueller and books about early SpaceX history. ([device.report][1])

The sequence was roughly:

1. SpaceX was testing the early Merlin engine's **ablative thrust chambers** (the chamber material protects itself by slowly burning away). Several chambers cracked during pressure testing. Mueller considered them unusable. ([FlipHTML5][2])

2. Musk refused to simply throw them away. He pushed for a repair attempt: put epoxy into the cracks so it could penetrate and reinforce the damaged areas. Mueller thought this was a crazy idea because the materials and operating conditions made it unlikely to work. They argued, but eventually Mueller said, effectively: "He's the boss." ([device.report][1])

3. Musk had the damaged chambers flown back to the SpaceX factory in California. He arrived dressed for a Christmas party — expensive clothes and leather/Italian shoes — but skipped the party and worked with engineers through the night applying epoxy. The epoxy ruined his shoes. ([Jeff Ward Writes][3])

4. The experiment failed. During another pressure test, the epoxy detached and the chambers still failed. The team eventually had to redesign the chamber. ([device.report][1])

The interesting lesson is not "Musk had a genius idea." The epoxy idea was actually wrong. The important engineering pattern was:

**Hypothesis → build/test quickly → fail → update model → continue.**

A normal large aerospace company might have:

* written reports,
* held review meetings,
* waited months,
* assigned blame.

A startup under existential pressure did:

* damaged hardware on a plane,
* CEO physically working on the part,
* test the crazy idea,
* learn immediately.

The failure itself saved time because it killed uncertainty. They proved: "epoxy patching is not the solution." Then they moved on to redesign. ([Chamber of Psychology and Counselling][4])

This is very similar to the mindset you often mention with GPU repair: a broken GPU is not "trash"; it is a **state of the system**. You measure, form hypotheses, modify, test, and learn. Musk's advantage here was not always being right — it was having an extremely short feedback loop between idea and physical reality.

[1]: https://device.report/m/08a5c4983310fea2cc7c2aa108d99432f64e3dd95a91841a784bde5903d8a035.pdf?utm_source=chatgpt.com "Elon Musk"
[2]: https://fliphtml5.com/fzqli/nrbb/Elon_Musk%3A_SpaceX%2C_Mars%2C_and_the_Quest_for_Interplanetary_Travel/?utm_source=chatgpt.com "Elon Musk: SpaceX, Mars, and the Quest for Interplanetary Travel - Flipbook by e-library | FlipHTML5"
[3]: https://www.jeffwardwrites.com/podcast-tom-mueller?utm_source=chatgpt.com "Tom Mueller - Employee Number One — Jeff Ward Writes"
[4]: https://cpcglobal.org/publications/Elon%20Musk%20By%20Ashlee%20Vance.pdf?utm_source=chatgpt.com "Elon Musk: Tesla, SpaceX, and the Quest for a Fantastic Future"
