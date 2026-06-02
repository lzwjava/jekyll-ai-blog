---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Struggles With
translated: false
type: note
---

Question: In frontend development, why is it often harder to get good results from AI models like Claude or Codex when describing UI visually, compared to backend development where describing APIs and field errors works better?

Answer:

You're observing a very real and common limitation when using current LLMs (Claude, o1, Gemini, Grok, GPT-4o etc.) for coding in 2025–2026.

### Core difference: Frontend vs Backend "precision gap"

| Aspect                  | Backend (API, logic, validation)          | Frontend (UI/layout/styling/interaction)       | Why the difference matters for LLMs |
|-------------------------|--------------------------------------------|--------------------------------------------------|--------------------------------------|
| Specification language  | Mostly textual & structural                | Heavily spatial + visual + implicit conventions  | LLMs are primarily trained on text  |
| Exactness required      | Logic must be correct (pass/fail clear)    | Pixel-perfect + responsive + accessibility + feel | Small deviations break the product  |
| Description mode used   | "field X should be number, min 18, required" | "card looks modern, clean, with subtle shadow" | Visual language is extremely lossy  |
| Feedback loop           | Run → see JSON / error message             | Run → look at rendering → adjust CSS           | Visual iteration is slower & subjective |
| Common success rate     | High when requirements are clear           | Medium–low when only described in natural language | — |

### Main reasons why visual descriptions fail more often on frontend

1. **Massive loss of information in natural language**
   "A beautiful centered login form with modern blue button"
   → hundreds of valid implementations exist (padding? font? border-radius? hover? mobile? contrast ratio?)

2. **No shared visual grounding**
   The model has never "seen" your screen. It only knows statistical patterns from training screenshots + code.

3. **CSS is very context-sensitive**
   - `position: absolute` vs `flex` vs `grid` changes everything
   - `gap` vs `margin` vs `padding` interacts differently with parents
   - Tailwind vs CSS modules vs styled-components changes the syntax surface dramatically

4. **UI taste is extremely subjective**
   What you consider "clean/minimal/elegant" can be completely different from what the majority of GitHub code looks like → model biases toward the average

5. **Lack of iterative visual feedback loop in chat**
   Backend: "this field returned 422 → fix validation" → 1–2 turns
   Frontend: "it's not centered on mobile" → needs multiple screenshot + description rounds

### Practical patterns that work noticeably better in 2025–2026 (frontend)

- **Best → worst order** (roughly ranked by success rate)

  1. Provide existing similar code + say "make it look like this but change X"
  2. Paste a **very detailed** Figma inspection panel export (spacing, colors in hex/hsl, font stack, weights, line-heights…)
  3. Give a precise **component breakdown** in text
     example:
     - outer: flex col, items-center, min-h-screen, bg-gray-50
     - card: w-full max-w-md, p-8, bg-white, rounded-2xl, shadow-xl
     - logo: mb-8, h-12, mx-auto
     - inputs: space-y-5 …

  4. Use Tailwind + give almost line-by-line className strings you want
  5. Attach/reference a **real screenshot** (many models now accept images well)
  6. Pure natural language visual description ← **worst** unless very simple component

- Quick cheat-sheet prompt that usually lifts quality a lot:

```
You are an expert React + Tailwind developer.
Generate **exact** JSX + className strings.
Do NOT use vague words like "nice", "modern", "beautiful".
Follow these exact design tokens and spacing rules:
- primary: #3b82f6
- radius: rounded-xl
- shadow: shadow-lg hover:shadow-xl
- input padding: py-3 px-4
- gap between form fields: space-y-4

Layout must use flex or grid — never position absolute unless explicitly needed.
Mobile-first approach. Make it responsive.

Task: centered login card containing: logo (h-10), email input, password input, submit button (bg-blue-600 hover:bg-blue-700), "forgot password" link.
```

### Summary

Backend plays to the strength of language models (symbolic reasoning + strict contracts).
Frontend plays to their weakness (spatial reasoning through text only + high aesthetic variance).

Until models get dramatically better at **purely visual reasoning from descriptions alone** (or everyone routinely attaches Figma/actual screenshots), the most effective way is:

- give structured textual specs (measurements, tokens, layout type)
- OR give visual reference + small modification request

That usually closes 70–80% of the quality gap compared to "make it look nice and modern".

References:

- None (common developer experience observation, no specific external source used)
