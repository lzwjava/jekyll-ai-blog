---
audio: false
generated: true
lang: en
layout: post
title: Using BrowserSync
translated: false
type: note
---

BrowserSync is a fantastic tool for streamlining front-end development by synchronizing browser actions, auto-reloading files, and providing a local development server. Here’s a step-by-step guide on how to use BrowserSync in your front-end workflow:

---

### 1. **Install Node.js and npm**
BrowserSync is a Node.js tool, so you’ll need Node.js and npm (Node Package Manager) installed. If you don’t have them yet:
- Download and install from [nodejs.org](https://nodejs.org/).
- Verify installation:
  ```bash
  node -v
  npm -v
  ```

---

### 2. **Install BrowserSync**
You can install BrowserSync globally or locally in your project.

#### Option 1: Global Installation
Run this command in your terminal to install BrowserSync globally:
```bash
npm install -g browser-sync
```
This lets you use the `browser-sync` command from anywhere.

#### Option 2: Local Installation (Recommended for Projects)
If you prefer to keep dependencies tied to a specific project:
```bash
npm install browser-sync --save-dev
```
This adds BrowserSync to your project’s `node_modules` and lists it in `package.json`.

---

### 3. **Start BrowserSync**
Depending on your setup, you can use BrowserSync in different ways:

#### Basic Usage (Static Files)
If you’re working with static HTML, CSS, and JS files, navigate to your project folder and run:
```bash
browser-sync start --server --files "*.html, css/*.css, js/*.js"
```
- `--server`: Runs a local server (serves files from the current directory).
- `--files`: Watches these files for changes and reloads the browser automatically.

For example, if your folder structure is:
```
my-project/
├── index.html
├── css/
│   └── style.css
└── js/
    └── script.js
```
Running the command above will:
- Start a server at `http://localhost:3000` (default port).
- Open your default browser.
- Reload the page whenever `index.html`, `style.css`, or `script.js` changes.

#### Proxy Mode (Existing Server)
If you’re using a backend server (e.g., Node.js, PHP, or Python), use the proxy option:
```bash
browser-sync start --proxy "http://localhost:8000" --files "*.html, css/*.css, js/*.js"
```
- `--proxy`: Proxies requests to your existing server (replace `http://localhost:8000` with your server’s URL).
- BrowserSync will overlay its features (like auto-reload) on top.

---

### 4. **Key Features**
Once BrowserSync is running, you get:
- **Live Reloading**: Changes to watched files trigger an instant browser refresh.
- **Cross-Device Sync**: Scroll, clicks, and form inputs sync across all connected devices (e.g., desktop, phone, tablet).
- **UI Dashboard**: Access a control panel at `http://localhost:3001` (default) to tweak settings or stop the server.

---

### 5. **Integrate with Build Tools (Optional)**
If you use tools like Gulp or Webpack, BrowserSync can integrate seamlessly.

#### Example with Gulp
Install Gulp and BrowserSync:
```bash
npm install --save-dev gulp browser-sync
```
Create a `gulpfile.js`:
```javascript
const gulp = require('gulp');
const browserSync = require('browser-sync').create();

gulp.task('serve', function() {
  browserSync.init({
    server: './', // Serve files from the current directory
  });

  gulp.watch(['*.html', 'css/*.css', 'js/*.js']).on('change', browserSync.reload);
});

gulp.task('default', gulp.series('serve'));
```
Run it:
```bash
gulp
```

---

### 6. **Common Commands and Options**
- Change port: `--port 8080`
- Disable auto-open: `--no-open`
- Watch specific files: `--files "path/to/files/*"`
- Full list: Run `browser-sync --help`

---

### 7. **Troubleshooting**
- **Port in use**: Change the port with `--port <number>`.
- **No reload**: Ensure file paths in `--files` match your project structure.
- **Permissions**: If globally installed, you might need `sudo` (e.g., `sudo npm install -g browser-sync` on Linux/macOS).

---

That’s it! BrowserSync is now ready to supercharge your front-end development. Start with the basic command, tweak as needed, and enjoy a smoother workflow. Let me know if you’d like help with a specific setup!
