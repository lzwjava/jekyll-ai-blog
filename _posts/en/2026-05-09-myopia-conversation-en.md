---
audio: false
generated: false
image: false
lang: en
layout: post
title: "A Conversation on Reversing Myopia"
translated: false
---

## Summary

Two friends — one a designer, the other an engineer who has spent roughly three years experimenting on himself — sit down to talk about myopia. The engineer shares a thesis he's been refining: most people are over-corrected for the way they actually live, and wearing a fully sharp prescription while staring at phones and laptops all day quietly accelerates how fast their eyes get worse. His practical recommendation is to own more than one pair of glasses, with a "near work" pair that is roughly 150–200 degrees weaker than the full distance prescription. The designer pushes back, asks questions, and offers product ideas and framing advice. They also detour through Jony Ive, Dieter Rams, the nature of "genius," and a minor car crash caused by wearing the wrong glasses.

---

## The Core Idea: Match the Glasses to the Scenario

The engineer opens with the angle he wishes opticians would lead with. When people get fitted, they almost always ask to be corrected to maximum sharpness — the assumption being that "clearer is better." But most adult life is not driving or watching a faraway blackboard. Most adult life is office work, phones, and reading at arm's length. Wearing a fully corrected prescription for those near tasks forces the lens of the eye to work harder than it needs to, and combined with bad habits, that's exactly the load that drives prescriptions deeper year after year.

His pitch, in one sentence: most people should own at least two pairs of glasses — a stronger pair for distance (driving, etc.) and a weaker pair for everything close-up (work, reading, phones).

This reframing is the part he wants to emphasize. He notes that pitching it as "reversing myopia" sounds like a sales gimmick and triggers people's skepticism, but pitching it as "different scenarios need different prescriptions" is something almost anyone will accept on first hearing. Once that idea lands, the slower-progression benefit follows naturally.

## Why This Should Work, Mechanically

The engineer walks through his mental model. The eye's lens (晶状体) is dynamic — it flexes to focus at different distances, similar to a camera lens or a piece of glass changing shape. If you're wearing a 5.0-diopter prescription strong enough to make a blackboard sharp at three to five meters, then when you bring a phone or laptop up close, the lens has to flex hard to compensate. Hours and hours of that strain, every day, year-round, is what he believes drives progression. Reduce the prescription for near tasks and you reduce that constant load.

He's careful to note he's still hazy on whether the lens technically gets "flatter" or "more curved" in that scenario — he wants to read more on the optics — but the directional intuition (more correction at distance = more lens work up close) is what the argument rests on.

## The Designer's Recent Experience — Possibly Accidental Evidence

The designer mentions that a few weeks earlier, after dyeing his hair back to black, his newer 550-degree glasses didn't suit the look anymore, so he had dug out a pair from about three years ago — roughly 450 degrees, about 100 degrees weaker than his current prescription. He'd had a small worry that wearing under-corrected glasses might hurt his eyes, but a few weeks in, nothing felt wrong. His prescription had been stable at 550 for several years running, so when he next gets an eye exam he'll have a chance to see whether the weaker pair has nudged anything.

He acknowledges this isn't a controlled experiment — if his eyes test slightly better, it doesn't prove the weaker glasses caused it; if they test worse, that doesn't disprove the theory either. But he's curious enough to follow up after his next exam.

The engineer's reaction: a 100-degree reduction is in the right direction but probably not aggressive enough. From his own years of trial — 175, 200, 225, 250 degrees of reduction, each tested for months at a time — his preferred recommendation lands around **175 degrees below the full prescription**, with **150 to 200 degrees** as the workable range. Pick whichever number inside that range feels comfortable in daily use.

## How Long to Test

The designer asks, half-jokingly, whether he tested each setup for half a day. His answer: months — sometimes half a year — per configuration. He treats it as a slow self-experiment, not an A/B test.

## The Failed Experiment: Bifocals / Progressive Lenses

About a year before this conversation, the engineer tried to solve the multi-pair problem with a single pair of bifocals. He explains the configuration in detail: a bifocal prescription requires top and bottom diopters, matching astigmatism on each side, an inter-pupil distance, and a "progression" parameter (the minimum allowed difference between the top and bottom regions, around 75–125 degrees) plus an SP / focal-center spacing value that determines how the gradient is laid out — analogous, he points out, to specifying the direction of a gradient when designing a UI background.

He tried multiple configurations over a couple of months. They cost noticeably more than his usual pairs (around 80 yuan online vs his usual 60). The reason it didn't work for him was practical: in real life, his head and posture don't reliably line up with the lens zones. Lying or reclining with a phone, he often wants the lower (near) zone, but a slight shift of posture pushes his gaze through the upper zone. The lower-near region of a progressive lens is also a relatively narrow curved area — maybe a third of the lens — and you can't customize how much of the lens it occupies. He eventually abandoned the approach.

The designer's instinctive objection arrives at the same place from a different angle: glasses slide down the nose, especially for men or anyone sweating outdoors, which means the focal zones drift relative to where you're actually looking. For him, that alone would be a deal-breaker.

## Product Ideas From the Designer

Once he understands what the engineer is trying to solve, the designer floats a couple of product directions:

- **Clip-on supplementary lens.** Like the lenses optometrists stack during an exam, or like clip-on 3D-movie lenses: you wear one base pair, and snap on a small additional lens when you need the stronger distance correction. A small, easy-to-carry second piece of optics rather than a second pair of glasses. (He notes existing solutions of this type are too heavy, but as a proof of concept the principle is already validated.)
- **Adjustable / liquid-filled lens.** Imagine the cross-section of a lens: the curvature of its two surfaces determines how light bends. If the lens were thin shells with a liquid layer between them, you could change the curvature and therefore the diopter on demand. The product story would be "one pair of glasses, ever — the prescription updates with you," which is also conveniently aligned with a slow-progression / reversal narrative.

The engineer is enthusiastic and agrees this is exactly the kind of direction worth prototyping, especially since it solves the very use case that bit him recently.

## A Cautionary Tale: Two Pairs Comes With Friction

The two-pair lifestyle is not free. The engineer recounts a recent incident: his household has two cars and two people, glasses get left in whichever car they were last used in, and one day he ended up driving with the weaker (–150-degree) pair. To make it worse, the car's AC fogged the windshield briefly. Coming out of an intersection, he didn't see clearly and clipped a road-divider barrier. The municipal repair bill in Guangzhou came to 1,000 RMB for the barrier; insurance covered it, and his own car needed only minor repair. The lesson he draws is that the multi-pair approach genuinely creates failure modes — you can be caught in a situation that demands the sharper pair without it on your face.

The designer extends the point: in a small fraction of cases — spotting a license plate, identifying a face at a distance, reacting to a truck on the highway — even a 100-degree reduction can matter, and a 150–200-degree reduction probably more so. Worth knowing, even if those moments are statistically rare.

## Hyperopia as a Sanity Check

To bolster the underlying premise — that near and far really do want different prescriptions — the engineer points out that prescription glasses for **hyperopia (farsightedness)** are commonly built the inverse way: top lens flat (no correction, since distance vision is fine), bottom lens carrying ~150 degrees of correction for reading newspapers and other close work. A quick search on Amazon for hyperopia readers shows the pattern. If the optical industry already accepts that one pair of eyes wants two zones for hyperopia, the same logic — applied in reverse — supports the multi-pair approach for myopia.

The point both end up agreeing on, and treating as the foundation: **near vision and far vision do want different prescriptions. That alone is uncontroversial.** The disagreement, if any, is only about how aggressive the difference should be.

## Choosing Your Working Distance

The engineer offers a concrete heuristic for choosing the weaker prescription. Identify your most common workspace setup. If you work mostly on a laptop screen, that's relatively close. If you work on a desktop with an external monitor (his case, and the designer's primary setup, ~70/30), the screen sits noticeably farther away.

Use whichever monitor you're at most often as the **outer bound**: pick the weakest prescription that still lets you read that screen clearly. Anything closer — phone, laptop screen, book — will then be comfortably in range automatically. He frames this as the "perfect pair" for daily life: sharp enough for the most distant thing you need to read, weak enough to relieve everything closer.

## Pricing & Practical Tips

The engineer keeps costs low by ordering online (around 60 RMB per pair vs around 100 RMB at brick-and-mortar shops in Guangzhou). The designer is mostly fitted in person; he suggests asking the optician at his next visit whether they'll let him try a lower-prescription pair on the spot, though he's skeptical that a few minutes in the shop is long enough to actually feel the difference. The engineer agrees — testing meaningfully takes days to weeks of real use, not minutes.

## A Detour: Genius, Designers, and Influences

Midway through the conversation, the topic drifts. The engineer credits a Chinese commentator (referred to as "Wang Yin / 网瘾", whose recent posts are now locked) with shaping his outlook — particularly the idea that "geniuses don't exist," which gave him permission to plug away at self-study (English, IELTS, prepping for an associate degree on his way toward AI research) rather than resent his trajectory after graduating from a less prestigious school. He notes the commentator was right about many things and wrong about others (notably underestimating modern AI), but the influence was meaningful.

The designer disagrees, gently but firmly: in his experience, real outliers do exist. He defines them carefully — someone of similar or younger age who, with comparable or less effort, produces work clearly beyond what you can produce. He softens it on a second pass: those people still combine real talent with enormous effort, and a large dose of timing and circumstance ("had I been placed in their conditions, perhaps I'd have arrived somewhere similar"). But the talent component, in his view, is real.

On designers specifically:

- **Jony Ive** — he will not be talked into the idea that anyone alive is more influential. Across all design disciplines, not just industrial design, he doesn't see anyone in the 21st century with comparable reach. The combination of Ive's own ability, his own effort, *and* an unrepeatable opportunity (Apple, at that scale, at that time, influencing not only Apple users but every shanzhai and copycat downstream) is, in the designer's view, simply unmatched in any category.
- **Dieter Rams** — historically top-tier. Easily top five in industrial-design history; he'd argue top two. A personal favorite.
- **Don Norman** ("Don Newman" in the transcript), *The Design of Everyday Things* — he owns the book but hasn't read it, partly because he heard Jobs once fired Norman and figured it might not be especially useful for him. He acknowledges it's widely regarded as foundational reading on interaction design.

The engineer mostly listens and accepts his ranking.

## Framing Advice From the Designer

Returning to the main thread, the designer gives his clearest piece of feedback. The pitch "I can help reverse your myopia" sounds, to a regular listener, like a scam — exactly like the language of an English-tutoring sales ad promising to raise an IELTS score by 100 points in a year. People reflexively distrust it.

But the pitch "different scenarios call for different prescriptions, and being slightly under-corrected for near work probably slows progression" is approachable, almost obvious in retrospect, and actually invites the listener to keep talking. The slowdown — "instead of gaining 50 degrees a year, you might gain 50 degrees over five years" — is, for many people who are tired of ever-thicker lenses and ever-pricier thin-lens upgrades, more than enough motivation on its own.

The engineer accepts this framing advice readily. He agrees that the "reversal" language is what makes the idea sound like marketing rather than a careful observation, and that leading with the multi-pair / scenario framing is the better way in.

## Where They Land

The designer doesn't commit to anything. He's happy to keep wearing the older, ~100-degree-weaker pair he dug out and to ask about a 150-degree-reduction pair at his next visit; he wants to feel it for himself before going further. He admits he finds the broader project — three years of patient self-experimentation, careful articulation, willingness to keep refining the pitch — genuinely admirable, regardless of where the science ultimately lands.

The engineer is satisfied. He's been sharing this pitch with friends and acquaintances for a while; nobody has come back with trouble, and he himself has had only minor inconveniences (the wrong-glasses car incident being the worst of them). He treats this conversation as another data point, and as confirmation that the framing he should be using is "scenario-based prescriptions," not "reversal."
