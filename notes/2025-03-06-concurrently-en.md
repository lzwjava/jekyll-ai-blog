---
audio: false
generated: true
lang: en
layout: post
title: Using concurrently
translated: false
type: note
---

It seems like you're asking about using "concurrently" in the context of frontend development. However, "concurrently" is typically a Node.js package used to run multiple commands or scripts at the same time, often in a backend or development workflow context rather than directly in frontend code. Did you mean how to use it in a frontend project setup (e.g., running scripts), or were you referring to something else like concurrent operations in frontend JavaScript (e.g., promises, async/await)? I'll assume the former for now, but feel free to clarify!

### Using `concurrently` in a Frontend Project

If you're working on a frontend project (e.g., with React, Vue, or Angular), `concurrently` is commonly used in development to run multiple processes simultaneously—like starting a development server and a build watcher. Here's how you can use it:

#### 1. Install `concurrently`
First, install it as a dev dependency in your project:
```bash
npm install --save-dev concurrently
```

#### 2. Add Scripts to `package.json`
Define the scripts you want to run concurrently in your `package.json`. For example, if you’re running a frontend dev server and a CSS preprocessor like Sass:
```json
{
  "scripts": {
    "start:frontend": "react-scripts start", // or your frontend dev command
    "watch:css": "sass --watch src/styles:dist/styles",
    "dev": "concurrently \"npm run start:frontend\" \"npm run watch:css\""
  }
}
```

- `start:frontend`: Runs your frontend development server (e.g., React, Vite, etc.).
- `watch:css`: Watches and compiles your CSS files.
- `dev`: Uses `concurrently` to run both commands at once.

#### 3. Run the Concurrent Scripts
In your terminal, simply run:
```bash
npm run dev
```
This will start both the frontend server and the CSS watcher simultaneously. You’ll see output from both processes in the same terminal, and `concurrently` keeps them running together.

#### 4. Optional Configuration
You can customize `concurrently` with options like:
- `--kill-others`: Stops all processes if one fails.
- `--names`: Labels each process for clearer output.

Example with options in `package.json`:
```json
"dev": "concurrently --names \"Frontend,CSS\" --kill-others \"npm run start:frontend\" \"npm run watch:css\""
```
Output might look like:
```
[Frontend] Starting frontend server...
[CSS] Watching CSS files...
```

#### Use Case in Frontend Workflow
Imagine you’re building a React app with a separate API server:
- Frontend: `npm run start` (React dev server on port 3000).
- API: `npm run start:api` (e.g., Node.js server on port 5000).
With `concurrently`, you can run both:
```json
"dev": "concurrently \"npm run start\" \"npm run start:api\""
```

### If You Meant Concurrent JavaScript in the Frontend
If you were asking about handling concurrent operations in frontend code (e.g., fetching multiple APIs at once), here’s a quick example using `Promise.all`:
```javascript
async function fetchData() {
  const [userData, postsData] = await Promise.all([
    fetch('https://api.example.com/user').then(res => res.json()),
    fetch('https://api.example.com/posts').then(res => res.json())
  ]);
  console.log(userData, postsData);
}
fetchData();
```
This runs the API calls concurrently and waits for both to resolve.

### Clarify If Needed!
Let me know if you meant something different by "concurrently in frontend"—like a specific library, framework, or use case—and I’ll tailor the answer further!
