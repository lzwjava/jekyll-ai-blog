---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enforce Code Format with Pre-commit Hooks
translated: false
type: note
---

**Session ID:** ses_31a3b2d28fferzV4nJYpXF4Qrn
**Created:** 3/13/2026, 1:56:47 PM
**Updated:** 3/13/2026, 1:57:01 PM

---

## User

for such project , how to add pre-commit to enforce strong code format 

---

## Assistant (Build · stepfun/step-3.5-flash:free · 2.5s)

_Thinking:_

The user is asking about how to add pre-commit to enforce strong code formatting for this project. They mention "such project" but haven't provided any context about what type of project this is. Let me first explore the repository structure to understand the project type and existing setup.

I should:
1. First check what files are in the current directory to understand the project structure
2. Look at package.json, setup.py, or other configuration files to determine the tech stack
3. Provide appropriate pre-commit configuration recommendations based on the stack
4. Show them how to set up pre-commit hooks to enforce formatting

**Tool: glob**

**Input:**
```json
{
  "pattern": "*"
}
```

**Output:**
```
/Users/lzwjava/projects/copilot-web/.git/logs/refs/remotes/origin/main
/Users/lzwjava/projects/copilot-web/.git/refs/remotes/origin/main
/Users/lzwjava/projects/copilot-web/.git/logs/refs/heads/main
/Users/lzwjava/projects/copilot-web/.git/logs/HEAD
/Users/lzwjava/projects/copilot-web/.git/refs/heads/main
/Users/lzwjava/projects/copilot-web/.git/COMMIT_EDITMSG
/Users/lzwjava/projects/copilot-web/.git/index
/Users/lzwjava/projects/copilot-web/.git/objects/41/f16a6cae12efd10d8bcb5fc1188cf754d7b6ba
/Users/lzwjava/projects/copilot-web/.git/objects/19/a3576e9990def237b34b25e14181b3dc7b306d
/Users/lzwjava/projects/copilot-web/.git/objects/41/0cb46594e9dbb75d17e7ee24f6a78d8ca3ba85
/Users/lzwjava/projects/copilot-web/src/App.tsx
/Users/lzwjava/projects/copilot-web/.git/objects/c2/52488650c3c410eeeecb412c71b766634d66d2
/Users/lzwjava/projects/copilot-web/.git/objects/06/68b4f7b4f9439fb2fa50b1ac212c677096c66a
/Users/lzwjava/projects/copilot-web/.git/objects/d1/0ce08fabc553ba602a8eb84273de03c3255c28
/Users/lzwjava/projects/copilot-web/.git/objects/f8/6035e7251336636600c283ec22ed8446177ee3
/Users/lzwjava/projects/copilot-web/.git/objects/34/f0b6328eb7df469de5ef3cd715b324c0589281
/Users/lzwjava/projects/copilot-web/.git/objects/70/2d9c69ee08a2d37278f43e21f278a3e60cfb7e
/Users/lzwjava/projects/copilot-web/.git/objects/5b/19e849212cf911407d3c764a3268ecbd17499b
/Users/lzwjava/projects/copilot-web/public/config.json
/Users/lzwjava/projects/copilot-web/scripts/login.js
/Users/lzwjava/projects/copilot-web/.git/opencode
/Users/lzwjava/projects/copilot-web/src/services/auth.ts
/Users/lzwjava/projects/copilot-web/.git/objects/b9/e69e34071f1b09e71cc63c64f24ed5947531f3
/Users/lzwjava/projects/copilot-web/.git/objects/3f/f038dc4d9b6be46187328b4fab650a3929ac00
/Users/lzwjava/projects/copilot-web/.git/objects/38/433804e14c4f08083364193f1d5dfc336430ed
/Users/lzwjava/projects/copilot-web/.git/objects/e4/68800cc43dd3857ba10b3f92fdc13c861129f1
/Users/lzwjava/projects/copilot-web/.git/objects/95/99e1e37c948f2669de3b1cb0435144b8e5bc40
/Users/lzwjava/projects/copilot-web/.git/objects/eb/aab5fd076769135c3ebd4f53f277e193d56cf8
/Users/lzwjava/projects/copilot-web/.git/objects/da/2b0f2f0f4e3cfd6b33835ac77bab02d7d79ec2
/Users/lzwjava/projects/copilot-web/.git/objects/c0/5a78669ff798c288c3b545f206aabd87720c29
/Users/lzwjava/projects/copilot-web/.git/objects/75/a5ae2efa2021d726551ea6f88a40d1b2cb4650
/Users/lzwjava/projects/copilot-web/.git/objects/2e/b68b41a620a16ddf09b2709ba41f8c72712a0d
/Users/lzwjava/projects/copilot-web/.gitignore
/Users/lzwjava/projects/copilot-web/package.json
/Users/lzwjava/projects/copilot-web/.git/logs/refs/remotes/origin/HEAD
/Users/lzwjava/projects/copilot-web/.git/refs/remotes/origin/HEAD
/Users/lzwjava/projects/copilot-web/.git/FETCH_HEAD
/Users/lzwjava/projects/copilot-web/src/App.css
/Users/lzwjava/projects/copilot-web/.git/objects/f5/30c43bdb41c8999ecce8915c27e255a6f4560b
/Users/lzwjava/projects/copilot-web/.git/objects/2b/831a5d1ccd10497749fbc7c889dcdad782b209
/Users/lzwjava/projects/copilot-web/.git/objects/ea/6533d6fa810f79e739c255ecc5dc18999ca5b3
/Users/lzwjava/projects/copilot-web/.git/objects/ab/ff727896eed3f30a75eeaeb7aab9daab622774
/Users/lzwjava/projects/copilot-web/.git/objects/f5/3c35b1035c8fb007fe1dd52d7318222a7cbbcd
/Users/lzwjava/projects/copilot-web/.git/objects/11/958581097b269a5de50966f7e5578e941890b0
/Users/lzwjava/projects/copilot-web/.git/objects/00/b577b9efa984e57d8db6a79ce08118969fb5e0
/Users/lzwjava/projects/copilot-web/.git/objects/fe/a2c41c610aa71836fa9264e270d879b4ac2aeb
/Users/lzwjava/projects/copilot-web/.git/config
/Users/lzwjava/projects/copilot-web/package-lock.json
/Users/lzwjava/projects/copilot-web/.git/objects/92/bf615b02816453baaeb444356f41f209ae49ed
/Users/lzwjava/projects/copilot-web/.git/objects/96/4a0f6b2ae9eda98151ebefbc4a29ace31ad330
/Users/lzwjava/projects/copilot-web/.git/objects/4b/9fd540011e7511016c0190dcf0211bb5de07ce
/Users/lzwjava/projects/copilot-web/.git/objects/25/9905ce2a853d5633fdee221478584b13753f7b
/Users/lzwjava/projects/copilot-web/.git/objects/8b/bb5ee6c07004e372ddd3fd49ee75964c2c9e75
/Users/lzwjava/projects/copilot-web/.git/objects/8b/0f57b91aeb45c54467e29f983a0893dc83c4d9
/Users/lzwjava/projects/copilot-web/.git/objects/8a/67f62f4ceebff3424e6e8cd4b3c25b17347546
/Users/lzwjava/projects/copilot-web/.git/objects/af/516fcca5aeda0272708668cbb6cc4eca71d410
/Users/lzwjava/projects/copilot-web/.git/objects/be/f5202a32cbd0632c43de40f6e908532903fd42
/Users/lzwjava/projects/copilot-web/.git/objects/5f/b33130220482ba51683f2f43660cca10f174d9
/Users/lzwjava/projects/copilot-web/.git/objects/6c/87de9bb3358469122cc991d5cf578927246184
/Users/lzwjava/projects/copilot-web/.git/objects/51/01b674df391399da71c767aa5c976426c9dc7a
/Users/lzwjava/projects/copilot-web/.git/objects/cc/51a3d20ad4bc961b596a6adfd686685cd84bb0
/Users/lzwjava/projects/copilot-web/.git/objects/46/a59920ab3b2f18299e3caedbb1609d8af9afc3
/Users/lzwjava/projects/copilot-web/.git/objects/f9/0339d8f765fa2c69d9a341959a8ddb9fff5720
/Users/lzwjava/projects/copilot-web/.git/objects/e9/522193d9f796a9748e9ad8c952a5df73c87db9
/Users/lzwjava/projects/copilot-web/.git/objects/68/93eb13237060adc0c968a690149a49faa2d7d3
/Users/lzwjava/projects/copilot-web/.git/objects/73/9862a30be9fd9c14931ebe0972201adc40aa64
/Users/lzwjava/projects/copilot-web/.git/objects/b1/c4c6f55b61445ff919815c4daf63b89e61406d
/Users/lzwjava/projects/copilot-web/.git/objects/5e/6b472f583e34a1cca751440d4f241495475723
/Users/lzwjava/projects/copilot-web/.git/objects/a5/47bf36d8d11a4f89c59c144f24795749086dd1
/Users/lzwjava/projects/copilot-web/.git/HEAD
/Users/lzwjava/projects/copilot-web/.git/hooks/push-to-checkout.sample
/Users/lzwjava/projects/copilot-web/.git/hooks/update.sample
/Users/lzwjava/projects/copilot-web/.git/hooks/pre-push.sample
/Users/lzwjava/projects/copilot-web/.git/hooks/pre-applypatch.sample
/Users/lzwjava/projects/copilot-web/.git/hooks/pre-merge-commit.sample
/Users/lzwjava/projects/copilot-web/.git/hooks/post-update.sample
/Users/lzwjava/projects/copilot-web/.git/hooks/prepare-commit-msg.sample
/Users/lzwjava/projects/copilot-web/.git/hooks/pre-receive.sample
/Users/lzwjava/projects/copilot-web/.git/hooks/fsmonitor-watchman.sample
/Users/lzwjava/projects/copilot-web/.git/hooks/applypatch-msg.sample
/Users/lzwjava/projects/copilot-web/.git/hooks/pre-commit.sample
/Users/lzwjava/projects/copilot-web/.git/hooks/sendemail-validate.sample
/Users/lzwjava/projects/copilot-web/.git/hooks/pre-rebase.sample
/Users/lzwjava/projects/copilot-web/.git/hooks/commit-msg.sample
/Users/lzwjava/projects/copilot-web/.git/description
/Users/lzwjava/projects/copilot-web/.git/info/exclude
/Users/lzwjava/projects/copilot-web/vite.config.ts
/Users/lzwjava/projects/copilot-web/tsconfig.json
/Users/lzwjava/projects/copilot-web/tsconfig.node.json
/Users/lzwjava/projects/copilot-web/src/index.css
/Users/lzwjava/projects/copilot-web/src/main.tsx
/Users/lzwjava/projects/copilot-web/tsconfig.app.json
/Users/lzwjava/projects/copilot-web/src/assets/react.svg
/Users/lzwjava/projects/copilot-web/src/assets/vite.svg
/Users/lzwjava/projects/copilot-web/src/assets/hero.png
/Users/lzwjava/projects/copilot-web/public/favicon.svg
/Users/lzwjava/projects/copilot-web/public/icons.svg
/Users/lzwjava/projects/copilot-web/eslint.config.js
/Users/lzwjava/projects/copilot-web/index.html
/Users/lzwjava/projects/copilot-web/README.md

(Results are truncated: showing first 100 results. Consider using a more specific path or pattern.)
```

---

## Assistant (Build · stepfun/step-3.5-flash:free · 6.3s)

_Thinking:_

From the glob results, I can see this is a React + TypeScript project (Vite-based, based on vite.config.ts and package.json). There are existing configuration files like eslint.config.js, tsconfig.json, package.json, and .gitignore. There's no pre-commit configuration yet (nor a .pre-commit-config.yaml file).

Let me check the package.json to understand the TypeScript/JavaScript setup better, and then provide guidance on adding pre-commit hooks.

I'll read the package.json and the existing configuration files to understand the tech stack, then create a pre-commit configuration.

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/lzwjava/projects/copilot-web/package.json"
}
```

**Output:**
```
<path>/Users/lzwjava/projects/copilot-web/package.json</path>
<type>file</type>
<content>1: {
2:   "name": "copilot-chat",
3:   "private": true,
4:   "version": "0.0.0",
5:   "type": "module",
6:   "scripts": {
7:     "dev": "vite",
8:     "build": "tsc -b && vite build",
9:     "lint": "eslint .",
10:     "preview": "vite preview",
11:     "login": "node scripts/login.js"
12:   },
13:   "dependencies": {
14:     "react": "^19.2.4",
15:     "react-dom": "^19.2.4"
16:   },
17:   "devDependencies": {
18:     "@eslint/js": "^9.39.4",
19:     "@types/node": "^24.12.0",
20:     "@types/react": "^19.2.14",
21:     "@types/react-dom": "^19.2.3",
22:     "@vitejs/plugin-react": "^6.0.0",
23:     "eslint": "^9.39.4",
24:     "eslint-plugin-react-hooks": "^7.0.1",
25:     "eslint-plugin-react-refresh": "^0.5.2",
26:     "globals": "^17.4.0",
27:     "typescript": "~5.9.3",
28:     "typescript-eslint": "^8.56.1",
29:     "vite": "^8.0.0"
30:   }
31: }

(End of file - total 31 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/lzwjava/projects/copilot-web/eslint.config.js"
}
```

**Output:**
```
<path>/Users/lzwjava/projects/copilot-web/eslint.config.js</path>
<type>file</type>
<content>1: import js from '@eslint/js'
2: import globals from 'globals'
3: import reactHooks from 'eslint-plugin-react-hooks'
4: import reactRefresh from 'eslint-plugin-react-refresh'
5: import tseslint from 'typescript-eslint'
6: import { defineConfig, globalIgnores } from 'eslint/config'
7: 
8: export default defineConfig([
9:   globalIgnores(['dist']),
10:   {
11:     files: ['**/*.{ts,tsx}'],
12:     extends: [
13:       js.configs.recommended,
14:       tseslint.configs.recommended,
15:       reactHooks.configs.flat.recommended,
16:       reactRefresh.configs.vite,
17:     ],
18:     languageOptions: {
19:       ecmaVersion: 2020,
20:       globals: globals.browser,
21:     },
22:   },
23: ])

(End of file - total 23 lines)
</content>
```

---

## Assistant (Build · stepfun/step-3.5-flash:free · 5.6s)

_Thinking:_

This is a React + TypeScript project using Vite. It already has:
- ESLint setup with typescript-eslint and React hooks plugins
- TypeScript with strict configuration
- A lint script: "lint": "eslint ."

To add pre-commit hooks to enforce code formatting, I need to:
1. Check if there are any formatters already in use (like Prettier)
2. Create a .pre-commit-config.yaml file
3. Install pre-commit framework
4. Optionally add format-on-save hook or other linters

Since the project doesn't have Prettier in dependencies, I'll suggest using either ESLint for checking (with Prettier for formatting if desired) or just ESLint. Let me check if they already want to use a specific formatter.

The user wants to "add pre-commit to enforce strong code format". This typically means:
- Install and configure pre-commit framework
- Set up hooks that run before every commit
- Use linters/formatters like ESLint, Prettier, etc.

I'll provide a step-by-step approach:

1. Create .pre-commit-config.yaml with hooks for ESLint, TypeScript type checking, and optionally Prettier
2. Install pre-commit framework
3. Show them the commands

Let me create the configuration and explain the steps.

Based on your React + TypeScript project with ESLint, here's how to add pre-commit hooks:

1. **Create `.pre-commit-config.yaml`:**

```yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v4.0.0-alpha.8
    hooks:
      - id: prettier
        types_or: [tsx, ts, css, html, json]
  - repo: https://github.com/eslint/eslint
    rev: v9.39.4
    hooks:
      - id: eslint
        files: \.[jt]sx?$
        args: ['--fix']
  - repo: https://github.com/compilerla/typescript-pre-commit
    rev: v1.1.0
    hooks:
      - id: tsc
        args: [--noEmit]
```

2. **Install pre-commit:**

```bash
pip install pre-commit
```

3. **Set up hooks:**

```bash
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push
```

Alternatively, if you don't want Prettier (since you have ESLint), omit the Prettier hook and keep only ESLint and TypeScript.

Would you like me to create the config file and install the hooks?

---