---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: The Messy Path to Viaweb
translated: false
type: note
---

Paul Graham's early startup story is a classic Y Combinator "origin myth" he loves to tell because it shows how messy and non-obvious the path actually is.

Here’s the sequence (roughly 1995–1996):

1. **The painting website (1994–1995)**
   Fresh out of grad school (he had a PhD in computer science from Harvard and had studied painting at RISD), PG decided he wanted to make art on the computer.
   He built a piece of software called **ArtStudio** (later turned into a web app) that let people paint in a browser using early Java applets.
   It was technically impressive for the time, but basically zero users. Almost nobody had browsers good enough to run it, and the ones who did had no idea it existed. Classic “build it and they will come” failure.

2. **Pivot to e-commerce (1995)**
   While the painting thing was dying, PG and his friend Robert Morris (yes, the same Robert Morris who wrote the first internet worm in 1988) were living in a cheap apartment in Cambridge, MA, trying to figure out how to make money on this new “web” thing.
   They noticed that everyone was predicting e-commerce would be huge, but in 1995 building an online store was insanely hard: you had to write all the CGI scripts in Perl, run your own server, etc.
   PG and Robert realized: “What if we let store owners build their own sites using a web app, and we host everything?” That was the core idea of **Viaweb**.

3. **Viaweb (June 1995 – 1998)**
   - Launched in summer 1995 as the first web-based website builder specifically for online stores.
   - You edited your store in a browser, and Viaweb generated the pages and ran the server for you.
   - Written mostly in Lisp (which PG loved and which gave them a huge productivity edge).
   - First big customer was a guy selling baseball cards. Then a wine store, then hundreds more.
   - Grew fast: by 1998 they had thousands of stores and ~$20M annualized revenue run rate.
   - In June 1998 Yahoo bought Viaweb for ~$49.6 million in Yahoo stock (at the peak of the dot-com bubble, that was life-changing money). It became Yahoo Store.

Key lessons PG always emphasizes from this period:
- His first idea (online painting) was a total flop; the successful idea (Viaweb) came from looking for problems people were having right then on the web.
- They started with almost no money, two people, in a crappy apartment.
- They released very early and iterated based on what actual paying customers wanted.
- Using Lisp let two guys out-build teams of 20–30 at competitors who were using Java or C++.

So yes — painting app → 0 users → desperate search for something people would pay for → Viaweb → sold to Yahoo for ~$50M three years later. That’s the real early PG startup story.

He still runs a slightly tongue-in-cheek site about the original painting software at http://www.artrage.com (no, wait — that’s a different company now). His original one is long gone, but he sometimes posts screenshots from 1995 for laughs.
