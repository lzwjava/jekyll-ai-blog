---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dev Script Points to Wrong File
translated: false
type: note
---

## What Happened

### Why `npm run dev` Failed

The `package.json` dev script was:
```json
"dev": "nodemon --exec ts-node src/index.ts"
```

`src/index.ts` is a **library entry point** — it only exports classes and types, it has no server startup code. Running it does nothing; nodemon started and immediately exited cleanly with no server listening.

### How It Was Fixed

The actual server lives in `src/server.ts`, which contains the `CaptchaServer` class with an Express app and a `.start()` method that calls `app.listen()`. It even has a guard at the bottom:

```ts
if (require.main === module) {
  const server = new CaptchaServer(port, workers);
  server.start();
}
```

Running it directly with:
```bash
npx ts-node src/server.ts
```

...bootstrapped the Express server on port 3000 and the health check responded successfully.

### Root Cause

The `dev` script in `package.json` points to the wrong file (`index.ts` instead of `server.ts`). It should be:
```json
"dev": "nodemon --exec ts-node src/server.ts"
```
