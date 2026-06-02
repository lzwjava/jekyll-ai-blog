---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用 Pre-commit Hooks 强制执行代码格式
translated: true
type: note
---

**Session ID:** ses_31a3b2d28fferzV4nJYpXF4Qrn
**Created:** 3/13/2026, 1:56:47 PM
**Updated:** 3/13/2026, 1:57:01 PM

---

## 用户

对于这样的项目，如何添加 pre-commit 来强制执行严格的代码格式

---

## Assistant (Build · stepfun/step-3.5-flash:free · 2.5s)

_思考：_

用户在询问如何为这个项目添加 pre-commit 来强制执行严格的代码格式。他们提到了“such project”，但没有提供有关项目类型的任何上下文。首先让我探索一下仓库结构，以了解项目类型和现有设置。

我应该：
1. 首先检查当前目录中的文件，以了解项目结构
2. 查看 package.json、setup.py 或其他配置文件，以确定技术栈
3. 根据技术栈提供合适的 pre-commit 配置推荐
4. 向他们展示如何设置 pre-commit hooks 来强制格式化

**工具：glob**

**输入：**
```json
{
  "pattern": "*"
}
```

**输出：**
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

(结果被截断：显示前 100 个结果。请考虑使用更具体的路径或模式。)
```

---

## Assistant (Build · stepfun/step-3.5-flash:free · 6.3s)

_思考：_

从 glob 结果中，我可以看到这是一个 React + TypeScript 项目（基于 Vite，基于 vite.config.ts 和 package.json）。有现有的配置文件，如 eslint.config.js、tsconfig.json、package.json 和 .gitignore。目前还没有 pre-commit 配置（也没有 .pre-commit-config.yaml 文件）。

让我检查 package.json 以更好地了解 TypeScript/JavaScript 设置，然后提供添加 pre-commit hooks 的指导。

我会读取 package.json 和现有配置文件以了解技术栈，然后创建 pre-commit 配置。

**工具：read**

**输入：**
```json
{
  "filePath": "/Users/lzwjava/projects/copilot-web/package.json"
}
```

**输出：**
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

(文件结束 - 总共 31 行)
</content>
```

**工具：read**

**输入：**
```json
{
  "filePath": "/Users/lzwjava/projects/copilot-web/eslint.config.js"
}
```

**输出：**
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

(文件结束 - 总共 23 行)
</content>
```

---

## Assistant (Build · stepfun/step-3.5-flash:free · 5.6s)

_思考：_

这是一个使用 Vite 的 React + TypeScript 项目。它已经具有：
- ESLint 设置，包括 typescript-eslint 和 React hooks 插件
- 严格配置的 TypeScript
- lint 脚本："lint": "eslint ."

要添加 pre-commit hooks 来强制执行代码格式化，我需要：
1. 检查是否已经使用任何格式化工具（如 Prettier）
2. 创建 .pre-commit-config.yaml 文件
3. 安装 pre-commit 框架
4. 可选地添加保存时格式化 hook 或其他 linter

由于项目中没有 Prettier 依赖，我建议使用 ESLint 进行检查（如果需要格式化，则使用 Prettier），或者仅使用 ESLint。让我检查他们是否已经想使用特定格式化工具。

用户想要“add pre-commit to enforce strong code format”。这通常意味着：
- 安装并配置 pre-commit 框架
- 设置在每次提交前运行的 hooks
- 使用 linter/格式化工具如 ESLint、Prettier 等

我会提供逐步方法：

1. 使用 ESLint、TypeScript 类型检查和可选 Prettier 创建 .pre-commit-config.yaml
2. 安装 pre-commit 框架
3. 展示命令

让我创建配置并解释步骤。

基于您的 React + TypeScript 项目和 ESLint，以下是如何添加 pre-commit hooks：

1. **创建 `.pre-commit-config.yaml`：**

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

2. **安装 pre-commit：**

```bash
pip install pre-commit
```

3. **设置 hooks：**

```bash
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push
```

或者，如果您不想要 Prettier（因为您有 ESLint），则省略 Prettier hook，只保留 ESLint 和 TypeScript。

您希望我创建配置文件并安装 hooks 吗？

---
