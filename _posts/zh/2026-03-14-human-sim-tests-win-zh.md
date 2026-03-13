---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 人类模拟测试总是获胜
translated: true
type: note
---

问题：对于像 OpenClaw 这样的 AI agent，是运行最终 integration test（模拟人类用户）作为最佳验证方法，而不是只是做事情或运行 unit tests 吗？

回答：

是 — **模拟真实人类交互的最终 integration testing 是验证 deployments 的金标准**，特别是对于像 OpenClaw 这样的 AI agents。这是为什么：

## 为什么模拟人类的 Integration Tests 胜出

### “只是做事情”的问题
当 AI agent 仅执行动作（deploy、restart、open port）而没有从**用户的视角**验证结果时，它会产生一种虚假的完成感。上面的 agent 打开了端口 5000 并声明成功 — 但从未确认 frontend 实际加载并端到端工作。

### Unit Tests 的问题
Unit tests 检查孤立组件：
- “API 返回 200 吗？” ✅
- “DB insert 成功吗？” ✅
- 但它们会遗漏：**browser CORS 失败、firewall 阻塞、DNS resolution、frontend JS 错误** — 正是本次失败的情况。

### 为什么 Integration Tests（人类模拟）更好

| 方法 | 是否捕捉真实问题？ | 用户视角？ |
|---|---|---|
| 只是部署并声明完成 | ❌ | ❌ |
| 仅 unit tests | 部分 | ❌ |
| **模拟人类的 integration test** | **✅** | **✅** |

OpenClaw 的适当最终 integration test 应该：
1. **在 browser/headless browser 中打开实际 URL**（Playwright、Selenium）
2. **像真实用户一样点击 UI**
3. **提交 form、创建 task、验证它出现**
4. **确认 database record 存在**
5. **从外部向内的视角报告 pass/fail**

## 关键原则

> Agent 应该证明系统从**人类坐的位置**工作，而不是从 server 坐的位置。

这正是测试“本地通过”但“用户失败”的原因 — agent 从 firewall 内部测试，而不是从外部。真正的模拟人类测试会立即捕捉到端口 5000 阻塞。

## 推荐的 OpenClaw Workflow

```
部署 → 运行模拟人类的 integration test → 
  如果 FAIL → 诊断并修复 → 重新运行 test → 
  如果 PASS → 向用户报告成功
```

绝不要跳过最终 integration test 或用只是检查 logs/unit tests 替代它。**Integration test 是 acceptance criteria。**