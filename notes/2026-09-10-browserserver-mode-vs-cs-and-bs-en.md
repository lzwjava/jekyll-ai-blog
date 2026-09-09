---
audio: false
generated: true
image: false
lang: en
layout: post
title: Browser/Server Mode vs C/S and B/S
translated: false
type: note
---

Question: How do browser/server mode compare to C/S (Client/Server) and B/S (Browser/Server) architecture?

Answer:

They are actually **closely related concepts** — browser/server mode is essentially the modern, fine-grained version of the classic B/S vs C/S architectural distinction.

---

## Classic Architecture Models

**C/S (Client/Server)**
- A dedicated **native client app** (desktop app) communicates with a server
- Examples: Outlook desktop, WinForms apps, native mobile apps
- Logic split between a fat client and backend server
- Requires installation on each machine

**B/S (Browser/Server)**
- The **browser acts as the universal client** — no installation needed
- All UI is delivered via HTTP as HTML/CSS/JS
- Examples: Web apps accessed via Chrome/Firefox/Safari
- Server handles most logic; browser just renders

---

## How They Map to Browser/Server Mode

| Concept | Maps To | Explanation |
|---|---|---|
| C/S architecture | — | Native client; not typically "browser mode" at all |
| B/S architecture | **Both** browser & server mode | B/S is the umbrella; the *mode* decides where rendering happens |
| Browser mode | B/S + client-side rendering | Browser does the heavy lifting after first load |
| Server mode | B/S + server-side rendering | Server does the heavy lifting, sends ready HTML |

---

## Key Insight

```
C/S  →  Fat native client + backend server
B/S  →  Browser as client + backend server
         ├── Browser Mode  (logic runs IN the browser)
         └── Server Mode   (logic runs ON the server, result sent to browser)
```

> B/S architecture **replaced** C/S for most web apps.
> Browser/Server *mode* is a **subdivision within B/S**, describing where rendering and logic live.

---

## Practical Differences

| | C/S | B/S (Server Mode) | B/S (Browser Mode) |
|---|---|---|---|
| Client type | Native app | Browser | Browser |
| Installation | Required | None | None |
| Rendering | Client app | Server | Browser JS |
| Network dependency | Moderate | High | High (initial only) |
| SEO friendly | N/A | ✅ Yes | ⚠️ Harder |
| Offline support | ✅ Often | ❌ No | ⚠️ Partial (PWA) |
| Example | WPF, Qt app | PHP, Rails, Next.js SSR | React SPA, Vue SPA |

References:
- [Client–server model – Wikipedia](https://en.wikipedia.org/wiki/Client%E2%80%93server_model)
- [Browser/Server vs Client/Server Architecture](https://developer.mozilla.org/en-US/docs/Learn/Server-side/First_steps/Client-Server_overview)
- [Next.js Rendering Strategies](https://nextjs.org/docs/app/building-your-application/rendering)
