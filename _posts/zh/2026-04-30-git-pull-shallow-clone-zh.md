---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 浅克隆中的Git拉取操作
translated: true
type: note
---

问题：如果我使用 `--depth=10` 克隆一个仓库，之后还能运行 `git pull` 获取更多提交吗？

回答：

是的，你可以在浅克隆仓库之后运行 `git pull`。以下是你需要了解的信息：

## 浅克隆基础

`--depth=10` 会创建一个**浅克隆** —— 它仅下载最新的 10 个提交，而非完整历史记录。这使得初始克隆更快且体积更小。

## 后续运行 `git pull`

```bash
git pull
```

该命令可以正常执行，并将**拉取克隆后推送的新提交**。它会保持仓库的浅克隆状态 —— 你仍然只拥有有限的历史记录窗口，但该窗口会随着新提交的到来向前滑动。

## 加深历史记录（可选）

如果后续需要**更多历史记录**，可以加深或完全解除浅克隆状态：

```bash
# 再加深 10 个提交的历史
git fetch --deepen=10

# 完全解除浅克隆（获取完整历史记录）
git fetch --unshallow

# 或等效命令
git pull --unshallow
```

## 关键行为总结

| 命令 | 效果 |
|---|---|
| `git pull` | 获取新提交，保持浅克隆状态 |
| `git fetch --deepen=N` | 向历史记录中添加 N 个提交 |
| `git fetch --unshallow` | 拉取完整历史记录 |
| `git log` | 仅显示浅克隆部分的历史记录 |

## 注意事项

如果尝试执行需要完整历史记录的操作（例如跨深分支进行 `git merge-base`，或某些 `git log` 范围查询），可能会遇到以下错误：

```
fatal: 在完整仓库上使用 --unshallow 没有意义
```

或

```
error: 服务器不允许请求未公布的对象
```

遇到这些情况时，只需先运行 `git fetch --unshallow` 即可。

**简短回答：在浅克隆后运行 `git pull` 完全正常 —— 没有问题。**