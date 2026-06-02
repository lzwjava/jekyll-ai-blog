---
audio: false
generated: true
image: false
lang: en
layout: post
title: Building VS Code on Windows
translated: false
type: note
---

Here's the full picture for building VS Code on Windows:

**Required tools:**

1. **Node.js 22.22.1** (exact version from .nvmrc)
2. **npm** (ships with Node)
3. **Python 3.x** — needed by `node-gyp` to compile native modules. node-gyp 11.2.0 is used (`build/npm/gyp/package.json`). Python must be on PATH.
4. **Visual Studio Build Tools** (or full VS) with the **"Desktop development with C++"** workload — provides MSVC compiler + Windows SDK that node-gyp invokes for native addon compilation. This is the most commonly missed dependency on Windows.
5. **Git**

**How the build works:**

- TypeScript is compiled via `gulp` (invoked as `node --experimental-strip-types ./node_modules/gulp/bin/gulp.js`)
- Key commands from `package.json`:
  - `npm run compile` — full compile (client + copilot extension)
  - `npm run watch` — incremental dev build
  - `npm run gulp` — direct gulp access
- Electron 39.8.8 is pulled as a devDependency and managed by `build/lib/electron.ts`
- The `preinstall` script (`build/npm/preinstall.ts`) enforces the exact Node version from `.nvmrc`

**Quick setup on Windows:**

```
# 1. Install Node 22.22.1 (via nvm-windows or direct installer)
nvm install 22.22.1
nvm use 22.22.1

# 2. Install Python 3
winget install Python.Python.3.12

# 3. Install VS Build Tools (C++ workload)
winget install Microsoft.VisualStudio.2022.BuildTools
# During install, select "Desktop development with C++"

# 4. Clone and build
git clone https://github.com/microsoft/vscode
cd vscode
npm install        # preinstall checks node version, postinstall runs
npm run compile    # compile TypeScript
npm run watch      # or: incremental dev mode
```

**Or to skip the native tools check** (if you only need TypeScript compilation, not a full Electron build):
```
set VSCODE_SKIP_NODE_VERSION_CHECK=1
npm install
```

The official full guide lives on the wiki: https://github.com/microsoft/vscode/wiki/How-to-Contribute — but the 4 tools above (Node, npm, Python, VS Build Tools) are the essentials. No separate Java, Rust, or Go needed for the main build.
