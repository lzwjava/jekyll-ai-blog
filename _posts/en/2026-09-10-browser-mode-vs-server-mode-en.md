---
audio: false
generated: true
image: false
lang: en
layout: post
title: Browser Mode vs Server Mode
translated: false
type: note
---

Question: What are browser mode and server mode (in the context of web development / rendering)?

Answer:

These two modes describe **where** your application's logic and rendering happen:

---

**Browser Mode (Client-Side)**

- Code runs directly in the user's **browser** (via JavaScript)
- The server sends a minimal HTML shell; the browser downloads JS bundles and renders the UI
- Examples: React SPA, Vue SPA
- Pros: Fast interactions after initial load, no server needed for each action
- Cons: Slower first load, SEO challenges, secrets can't be hidden

---

**Server Mode (Server-Side)**

- Code runs on the **server**; the server sends fully-rendered HTML to the browser
- The browser receives ready-to-display content
- Examples: Next.js SSR, Nuxt SSR, traditional PHP/Rails
- Pros: Fast first paint, better SEO, secrets stay on server
- Cons: Every request hits the server, potentially slower interactivity

---

**Quick Comparison**

| | Browser Mode | Server Mode |
| --- | --- | --- |
| Rendering location | Client (browser) | Server |
| First load speed | Slower | Faster |
| SEO | Harder | Better |
| Interactivity | Very fast after load | Depends on hydration |
| Secrets/API keys | Exposed risk | Safe |

---

Modern frameworks like **Next.js** and **Nuxt** let you mix both — some components render on the server, others on the client — giving you the best of both worlds.

References:

- [Client-side vs Server-side Rendering – MDN](https://developer.mozilla.org/en-US/docs/Learn/Server-side/First_steps/Client-Server_overview)
- [Next.js: Server and Client Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
