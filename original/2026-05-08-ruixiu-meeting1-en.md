---
audio: false
generated: false
image: false
lang: en
layout: post
title:  A Mentor-Mentee Conversation on AI Research, Programming Growth, and Life Direction
translated: false
---

> This article is compiled from the audio transcript of an online meeting. The two participants were a senior programmer and a high-school AI researcher (Ruixiu Zhang). Because the original transcript lost speaker labels, the content below is reorganized from a third-person perspective ("they"), preserving the colloquial style and core ideas of the original conversation, while removing repetition, small talk, and unrelated fragments, and grouping things by topic.

---

## 1. Communication Efficiency and the "Project Walkthrough" as an Opener

The meeting opened with a very practical observation: **repeated communication is inefficient**.

The senior mentioned that he had just finished an interview where he opened his blog and walked through who he was in about ten minutes — that, in his view, is what efficient communication looks like. He suggested they record this meeting, transcribe it, and the next time a middle- or high-school student came along with the same questions (how to do projects, how to package a resume), they could simply send over the organized material instead of explaining everything from scratch.

He pointed this out specifically: a lot of what you say to professors and to many other people is the same content repeated over and over. That state of affairs is fundamentally inefficient.

For the meeting tool itself, they were on Tencent Meeting, but the senior recommended switching to **Teams** next time, mentioning he also has Zoom. The reasoning: these are products built with hundreds of millions, even billions of dollars — getting comfortable with an industrial-grade collaboration tool is itself part of "living in the future."

---

## 2. Why "Low-Level Algorithms" and "Building Products" Are Two Different Paths

On direction, the senior first shared an observation about another kid (Yangyang): that person works on **optimization within the NVIDIA stack** (VRAM, memory movement, kernel-level engineering). That work is essentially ops and engineering — it isn't research that makes AI "smarter or more useful."

Ruixiu Zhang's stance was clear:

- He prefers digging into and thinking about **algorithm-level innovation**;
- For example, studying attention, studying RoPE (he mentioned Su Jianlin's work of "rotating" attention), and thinking about what would happen if you "tilted a particular attention to 90 degrees";
- As for the line that "you'll only end up doing products," he disagreed — building products is a different track aimed at applying AI to every area of life, while he wants to go a step further down, closer to the model itself.

The senior's view: **both paths are valid, but you have to know clearly which one you're on.**

He then said something fairly blunt — paraphrasing: growing up in the Chinese environment means a lot of effort already goes in, but there is always sky beyond the sky. Compared with the top 16-year-olds in Silicon Valley, the gap mainly shows up in two places:

1. **Practical English expression** — extremely proficient, as fluent as Chinese;
2. Computer skills are roughly comparable, but in a high-intensity communication environment like OpenAI, if your English comprehension isn't as efficient as your Chinese, you'll be a bit slower explaining "very complicated transformer discussion" — and that alone can let another candidate edge past you, even if their thinking isn't sharper or their AI fundamentals aren't more solid. **Communication is itself a hard metric.**

So he kept emphasizing: **English fluency isn't about English — it's about not suffering in the future.**

---

## 3. Tree of Thoughts Project: A Full Code Walkthrough

The technical core of the meeting was Ruixiu Zhang sharing his own **Tree of Thoughts** physics-problem-solving system. He ran it locally and walked through the architecture step by step.

### 3.1 Model Division of Labor: Four Roles

The system is a collaboration of four kinds of models:

| Role | Size | Responsibility |
|------|------|------|
| **Planning Model (Orchestrator)** | Large (120B) | Decompose the problem into meta-task → task, planning step by step |
| **Modeling Model** | Medium (9B) | Strictly follow the planner's instructions, **never shown the full problem** |
| **Review Model** | Small (0.5B / 4B) | Inspect each step's logic, decide noise / send back / pass |
| **Evaluation Model** | Small | Subjective scoring, e.g. whether the final formula is clean enough |

Ruixiu explained a key design decision: **why must the Modeling Model not see the full problem?**

> If you let it see the original problem plus the decomposed sub-task, it can't help itself — it will try to "solve the whole thing in one shot" instead of following the decomposition. So you must feed it only the instruction for the current step.

The senior's comment: "That's exactly right — you have to give it something precise, strip out everything it doesn't need, otherwise it will misunderstand you."

### 3.2 Why FSM (Finite State Machine) Instead of a Simple Data Structure

Review uses an FSM-based state-management approach. Ruixiu's reasoning:

- A node doesn't just store "what number was computed" — it stores **the boundary conditions, parameters, the skill that was called, and the constraints of this modeling step**;
- When solving physics problems, every intermediate answer has a domain of applicability, and the FSM is the carrier that stores those domains alongside the answers;
- This is also why he later abandoned the DAG (directed acyclic graph) merging idea — different branches almost never share the same prior assumptions (e.g. one branch assumes ideal fluid, another adds a bunch of correction terms); even if both compute the same number, you can't merge them.

### 3.3 On "Diverging" and "Converging"

He encourages the model to **diverge as much as possible at the earliest nodes**, e.g. generating 5–7 different approaches; later on, if a branch is just adding a correction term (such as drag), there's no need to diverge further — the review model decides this on its own.

A humanities problem might have the opposite shape: in the stage of rebutting an existing argument, you may actually need to diverge more late in the process. **So the shape of the "thought tree" is itself a reflection of the discipline's character.**

### 3.4 Skill System and External SQL

He externalizes all "domain knowledge":

- Fluid-mechanics formulas, work-and-energy formulas, etc. — **the model is not allowed to memorize them**, they're written into skills;
- The model only invokes; it isn't allowed to compute on its own;
- This avoids the model "guessing wildly" in places where there are no rule-based constraints.

### 3.5 Limitations of the Orchestrator and Why Start with a Small Model

The final answer the demo produced wasn't especially accurate (e.g. one problem ended with something like `v_eff × h`, a form that wasn't precise enough). He was upfront about it:

> "Open-source small models are still too weak. If I called an API, the result would definitely be better."

But he stressed a working method that the senior strongly endorsed:

> **First, get the entire harness running on a local small model, instead of jumping straight to an API.**
>
> Small models expose the small pitfalls you'd never see when calling an API; once the whole pipeline is running, switching to a bigger model can only make it better, not worse.

---

## 4. Code Organization and Codex / Copilot Habits

They went through several files together: `backend / scheduler / models / planning_model / utils`. Some observations:

- Some modules in the project (e.g. `merge`) are AI-generated but currently unused — he chose to keep them, with the reasoning "maybe useful for other disciplines, almost not used in physics";
- Ruixiu uses **Codex (the higher Copilot tier, the $140 plan)**, with GPT-5.4 plus high-intensity tasks; running an entire project only consumed about 7-something percent of his quota;
- He grants Codex **auto-approve permissions**, so it doesn't need a confirmation for each command. His judgment: the model itself won't do anything harmful, and giving up that control significantly improves efficiency;
- His use of Codex is closer to "collaboration" — letting it run tests back and forth and iterate on its own — rather than treating it as a one-shot Q&A tool.

Tooling suggestions from the senior:

- Try **Ghostty** for the terminal;
- Switch every interface in VSCode to English; long-term exposure to English UIs is intentional training;
- When asking questions, **paste the code whenever you can** — descriptions alone are often inaccurate;
- For newer dependencies, just clone the code locally and ask questions against the real source via something like Cloud Code — far more accurate than letting the model do a web search.

---

## 5. Mini-LLM Project: A nanoGPT-Style Training Implementation

Next they looked at the second project — a mini-LM training implementation modeled on nanoGPT.

### 5.1 Multiple Versions and Hardware Adaptation

The reason there are several versions in the repo: he ran the same code on different hardware:

- MacBook (Flash Attention isn't usable);
- His own 3090;
- A classmate's 5090;
- Cloud A100 and A800.

Different hardware requires different precision, batch size, and parallelism strategies; the version he kept is the A100 one.

### 5.2 A Few Details Quizzed on the Spot

The senior ran through Transformer details quiz-style:

- **RoPE (Rotary Positional Embedding)**: turns position into a rotatable vector so each token interacts better with the others; in the autoregressive case, sine/cosine is used for positional encoding, registered as a buffer that doesn't participate in parameter updates and is saved alongside;
- **KQV**: K is what this token "is looking for"; Q is the token's own information; V is what this token can contribute to the relationships between tokens;
- **Flash Attention / mask**: he didn't write the mask by hand because PyTorch already handles a lot of that internally;
- **Transformer Block**: a LayerNorm + residual connection on each side, with self-attention and feed-forward in between;
- **Training loop**: Adam optimizer, loss backward, gradient update, zero-grad — three lines of code together. The senior's view: even if you don't usually write your own optimizer, understanding the semantics of those three lines is critical when tuning hyperparameters or debugging.

### 5.3 Data Scale and Hardware Upgrade

- Ruixiu's training data is around a dozen GB; the senior has used 60GB;
- He back-calculates the parameter ceiling from the token count, stopping right after he's halfway over the line;
- He just placed an order for the **NVIDIA Pro 6000** to replace the 3090 (reasoning: the 3090 is too constrained for training, Blackwell optimization isn't great yet, but VRAM size is a hard requirement); his father is helping with the build;
- Next on his list: a **natively multimodal model**.

---

## 6. The Third Project: An Agentic Coding Experiment

This is a mini "multi-agent collaborative coding" system Ruixiu built, inspired by Cloud Code:

- Uses ddgs (DuckDuckGo Search) for web retrieval;
- The Orchestrator **splits the big task across multiple coders** (note: this is the opposite of the Tree of Thoughts approach of "I only think about the first step" — here it subdivides directly);
- After each coder finishes, a reviewer first does static checks (e.g. catching low-level mistakes like a missing C++ semicolon); if there are problems, send it back **for a rewrite** (because small models only get worse the more they edit);
- Once it passes review, throw it into a sandbox to run;
- Sandbox errors go back to the orchestrator; after several rounds without success, the orchestrator will **modify the corresponding coder's system prompt** so it stops making the same mistake — he calls this "controlled CSM evolution."

He rates this project as a one-off exploration that he didn't continue maintaining, but he did get small tasks like "Snake game code" running through it.

---

## 7. On "Proving Your Level" — Important Advice from the Senior

When the conversation turned to RoPE and KQV, the senior asked a slightly pointed question:

> "Ruixiong, you're saying you're stronger than that Deng Mingyang or the Kimi guy, but I'm actually skeptical."

He elaborated: it isn't that he doesn't believe in the potential; the point is that **outsiders have no credible way to judge it**. To get others to believe you're stronger than some 0xy / IOI medalist, there are usually a few paths:

1. Have **repeated conversations** with someone who already knows you reasonably well, so they can see your grasp of LM knowledge across multiple points in time;
2. Let the resume speak for itself — at a glance, the reader knows this person is stronger than X;
3. Get **identified on the spot** in an interview by a sufficiently senior interviewer (he gave the example of his own morning interview that day for a Standard Chartered overseas role — half an hour in, the interviewer signaled he had passed).

The point of saying this isn't to deflate, it's to remind: "your level" can't stay as a private feeling. **It needs a vehicle others can see.**

He also touched on something interesting — **a name itself can become a brand**:

> "When people hear 'Zhang Ruixiu' and immediately know you're a top-tier person, you've fully arrived — your name becomes your brand."

---

## 8. On "Reversing Myopia" — A Side Research Topic of the Senior's

Mid-meeting, the senior shared a non-mainstream topic he'd been working on for years — **reversibility of myopia**. The brief points:

- Core mechanism: wear glasses 100–150 degrees lower than your current prescription so the eye is constantly in a "needs to slightly self-focus" state, slowly adjusting axial length;
- How to do it: full prescription in class or when looking at distant things; the lower-100-degree pair for daily near work; cycle back and forth;
- Glasses recommendation: thirty-to-fifty-yuan ones from Pinduoduo are fine;
- He has been tracking this for three years: myopia down 50 degrees, astigmatism down 75–100 degrees, with rebounds along the way but a downward trend overall;
- Recommended resources: **Todd Becker's** site, and the **endmyopia** community.

He drew a parallel: this is essentially the same as how he understands GPT —

> "In 2017 there weren't many people discussing Transformers either; the things that genuinely work are, in their early stages, only known to a small number of people."

And he reminded Ruixiu that as a high-school student doing heavy near-work, this is worth a few minutes of attention even more than the project work.

---

## 9. On Network, Foreign-Language Environment, and Independent Thinking

They went down Ruixiu's WeChat group roster line by line:

- **Lin Zhen** (postdoc at Tsinghua, BUPT alum, willing to lend him compute): the senior knew him, called him "well-resourced and warm-hearted";
- **Yangyang** (Hong Kong, the same-age person doing NV stack optimization): Ruixiu admitted that area itself isn't really of interest to him;
- He has very few foreign friends and rarely speaks English in daily life — the senior emphasized this is a part Ruixiu **needs to make up for actively**.

When the conversation turned to **Wang Yin** (Wang Yin), **Daniel P. Friedman**, and *The Little Schemer*, the senior spent a lot of time explaining what he means by "independent thinking":

- Someone like Wang Yin, in his sixties and still pivoting to write a book on AI, represents the principle that **depth has no shortcut** — it isn't about chasing papers, it's about **thinking the problem through yourself**;
- Many famous American schools, Cornell among them, are in his view places where "they let you swim to shore and then throw rocks at you" — they assign work but don't teach the real thing;
- The point of projects like mini-Kanren isn't paper publication, it's "the idea was generated by you, so you actually know how it came to be";
- Quoting Wang Yin: "Better to teach someone to fish than to give them a fish."

He directed this point at Ruixiu: **why so many things must be thought up by yourself rather than copied from others — that is the foundation of everything that comes later.**

---

## 10. The Senior's Own Founding Experience (As a Reference Point)

To put a footnote on "project credibility," the senior described a WeChat mini-program live trivia project he ran around 2016:

- Did the backend himself, half the front end, payments, and user ops;
- Ran it for over a year, eventually reaching **30,000 users**;
- Used a LeanCloud-style platform, with long-lived connections (WebSocket) for "next question" sync messages, decoupled from the video stream (RTMP);
- Similar apps later (he cited "live trivia shows with tens of millions of users") were shut down for content-compliance reasons — his point: **the larger your user base, the more compliance and regulation matter**.

He then told the early-Airbnb story — the founders meeting with an investor over coffee, the investor leaving for the bathroom and never coming back. He wasn't complaining; he wanted Ruixiu to know in advance:

> "The world is very transactional. When you don't have a name, the cold rejections will be many — you have to be mentally prepared for that."

---

## 11. A Quick Math Quiz

A short quiz session was sprinkled in:

- **SVD (Singular Value Decomposition)**: factor a matrix into U Σ Vᵀ;
- The relationship between **eigenvalue decomposition** and SVD;
- The "semantics" of matrix multiplication: a kind of **information exchange**;
- One conclusion: **"There is no intelligence in artificial intelligence, and no neurons either; what's actually doing the work is calculus."** Ruixiu's amendment: at the LLM layer there's an extra layer of stochasticity, but the underlying mathematical skeleton is indeed that;
- Training, in his view, is essentially "guess high or low": guess too low and gradients push it up, guess too high and they push it down — iterate.

---

## 12. AI Tools and Development Habits Summary

Scattered but valuable points:

- **OpenRouter**: actually useful — lets you horizontally compare "the best models on the market" on your specific problem;
- **One-shot / Few-shot**: model input = model = output; giving a single example can substantially improve accuracy;
- **Cloud Code's skill / "Lobster"** (likely a misheard name, possibly Lobster or another extension): Ruixiu hasn't used much of this;
- **Hermes**: also rarely used;
- **iCloud + small homemade tools**: the senior wrote a crude but working PDF highlighting tool — using this, he reinforced the methodology that "**building a minimal version naturally teaches you the whole picture.**"

---

## 13. Collaboration Plan and Next Meeting

As the meeting wound down, the senior put forward a concrete collaboration idea:

> "I've already trained GPT-2 myself. We should team up and train a GPT-3. If we can also train a GPT-4 (at the 2022 level), we'd be near the front of the AI field."

Ruixiu's reply kept its engineering sobriety: scale up the parameters and you no longer need a single machine — you need **a cluster**. The senior thinks platforms like Runpod can handle the cluster side; the bottleneck remains the same three things — data, compute, algorithms.

For the next meeting, they agreed:

1. Switch to **Teams**;
2. Walk through **Transformer / KQV** again — that is the part most often asked in interviews;
3. Ruixiu to send a **myopia exam report**;
4. Ruixiu to finish reading the few Wang Yin articles the senior recommended.

---

## Closing

This conversation covered a wide range: from a 16-year-old's Tree-of-Thoughts physics-reasoning framework, to live questioning on RoPE and KQV, to a Silicon Valley founder anecdote, to myopia reversal and a methodology of "independent thinking."

If you had to compress it into one line, it would be roughly this:

> **Capability itself is necessary; but beyond capability, you need a vehicle that lets others see it — a resume, a project, a name, English fluency, and the steady judgment others form of you across multiple meetings.**

On the technical side, both agreed: **first get the pipeline running on a small model, then switch to a bigger one; let the model perform within the boundaries you design, instead of letting it think on your behalf.** Whether building Tree of Thoughts or a mini-LLM, fundamentally these are the same thing.
