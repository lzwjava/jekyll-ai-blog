---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes更新节点依赖停滞
translated: true
type: note
---

问题：为什么 `hermes update` 会在“→ 正在更新 Node.js 依赖项...”处卡住？

回答：

这是 `hermes update` 的一个**已知问题**。该进程在 `→ 正在更新 Node.js 依赖项...` 步骤卡住，因为它底层运行的是 `npm install --silent`，而 `npm install` 可能由于多种原因变慢或看似卡住：

---

## 根本原因

在 `hermes_cli/main.py` 中，当找到 `package.json` 时，更新脚本会运行：
```python
subprocess.run(["npm", "install", "--silent"], cwd=PROJECT_ROOT, check=False)
```
`--silent` 标志会抑制所有输出，因此即使它正在积极工作，看起来也像是冻结了。

这是它*看似*卡住的主要原因——没有进度输出，而且 `npm install` 可能需要很长时间（几分钟）来解析和下载完整的 Node.js 依赖树。

---

## 实际卡住或非常慢的常见原因

1. **npm 注册表速度慢** — `npm install` 从 npm 注册表获取包，根据你的网络或地区，这可能会很慢。

2. **依赖树庞大** — 运行后，`npm install` 可能在 `package-lock.json` 中产生 2000+ 行的差异，表明依赖树庞大复杂，需要时间解析。

3. **lockfile 不一致** — 提交的 `package-lock.json` 可能与 `package.json` 不完全一致，因此 `npm install` 会默默重新解析整个依赖图，而不是快速安装。

4. **Node.js 版本不匹配** — 仓库要求 `node >=20`，所以如果你使用的是旧版 Node.js，安装可能会静默失败或行为异常。

---

## 如何修复/解决方法

**选项1：耐心等待**
它很可能只是在默默工作。给它 3–5 分钟再断定它真的卡住了。

**选项2：手动运行 npm install 并显示输出**
```bash
cd ~/.hermes/hermes-agent
npm install
```
这将显示进度和错误，与静默的子进程调用不同。

**选项3：使用 `npm ci`（更快、确定性）**
GitHub issue 中推荐的修复方法是将 `npm install --silent` 替换为 `npm ci --silent`，后者完全按照 lockfile 安装，无需重新解析依赖——这样更快且不会弄脏工作树。

你可以手动执行：
```bash
cd ~/.hermes/hermes-agent
npm ci
```

**选项4：检查你的 Node.js 版本**
```bash
node --version
```
确保它是 **v20 或更高版本**（推荐使用 v22 LTS）。

**选项5：运行 `hermes doctor`**
```bash
hermes doctor
```
这将检查 Node.js 依赖项并显示任何具体问题。

---

## 总结

在大多数情况下，更新**并非真正冻结**——只是由于 `--silent` 而没有可见输出。底层的 `npm install` 正在重新解析庞大的依赖树。最安全的即时修复方法是手动执行 `cd ~/.hermes/hermes-agent && npm ci` 来查看实际情况。

参考：

- [Bug: hermes update runs npm install instead of npm ci · Issue #4048](https://github.com/NousResearch/hermes-agent/issues/4048)
- [Bug: npm install hangs at "Installing Node.js dependencies" · Issue #8145](https://github.com/NousResearch/hermes-agent/issues/8145)
- [Hermes Agent FAQ & Troubleshooting](https://hermes-agent.nousresearch.com/docs/reference/faq)