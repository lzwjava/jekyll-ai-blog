---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 重复注释检测 — pre-commit 与 CI
translated: true
type: note
---

## 问题

`notes/` 目录中存在 5 对重复笔记——内容相同，文件名不同。之所以出现这种情况，是因为笔记管道在生成内容时没有检查已有的内容。

## 变更内容

**新增 pre-commit 钩子**（`.pre-commit-config.yaml`）：
```yaml
- id: duplicate-notes-check
  name: Duplicate notes check
  entry: python3 -m unittest tests.workflow.test_duplicate_notes -v
  language: system
  pass_filenames: false
  always_run: true
```

**保留 CI 单元测试**（`.github/workflows/gh-pages.yml`）：
```yaml
- name: Run Unit Tests
  run: python -m unittest discover -s tests/workflow
```

**从 `notes/` 中移除了 5 对重复笔记**。

## 为什么这样有效

**Pre-commit 在本地提交前即可捕获重复内容。** 测试按日期（YYYY-MM-DD 前缀）对笔记进行分组，然后使用快速字符相似度比较每组内笔记的前 200 和后 200 个字符。若相似度超过 90%，则标记为重复。

**CI 仍然运行完整的测试套件**——包括重复检查在内的全部 15 个工作流测试。这是对任何绕过 pre-commit 的内容（直接推送、机器人提交、CI 生成的笔记）的安全网。

**两个层次服务于不同目的：**
- Pre-commit：快速反馈循环，在坏提交离开你的机器之前阻止它们
- CI：捕获任何漏网之鱼（机器人、直接推送、强制推送）

## 为什么可能无效

**误报。** 相似度检查使用前 200 和后 200 个字符。两篇关于同一主题但内容不同的笔记如果开头相似，可能会触发检查。90% 的阈值设置得比较激进。

**性能。** 对于 9,884 条笔记，按日期分组比较很快（约 0.3 秒）。但如果笔记数量增长 10 倍，每个日期组内的 O(n²) 比较可能会变慢。

**绕过路径。** Pre-commit 可以通过 `git commit --no-verify` 跳过。CI 测试套件会捕获这种情况，但只有在提交已经推送之后。

**机器人生成的内容。** 笔记管道在 CI（gh-pages.yml）中运行并生成新笔记。如果它创建了重复内容，CI 会在下一次运行时捕获——但重复内容已经被提交并推送了。

## 目前有效的部分

- Pre-commit 钩子在提交时阻止重复笔记
- CI 运行完整工作流测试套件作为安全网
- 清理了 5 对重复笔记
- 测试运行时间约 0.3 秒（足够快以适应 pre-commit）

## 可以改进的地方

- 笔记管道应在生成前检查重复，而非生成后
- 在 CI 工作流中（提交前）增加去重步骤，可以防止机器人生成的重复
- 相似度阈值可根据实际误报率进行调整