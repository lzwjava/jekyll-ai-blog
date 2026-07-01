---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Git Filter Repo 路径选项指南
translated: true
type: note
---

**Question:** git filter-repo 是如何工作的，关于 --path 和 --file 有哪些选项？

**Answer:**

`git filter-repo` 是目前（2025–2026年）推荐且最现代、最快的重写 Git history 的工具（在大多数情况下取代了 `git filter-branch` 和 BFG Repo-Cleaner）。

### git filter-repo 的基本工作原理

1. **读取**：一次性读取整个 repository history（从最早的 commit 到最新的 commit）。
2. **应用规则**：应用你指定的 filtering rules（path filters, blob filters, commit message filters, email filters 等）。
3. **重写**：仅重写匹配或受规则影响的 commits。
4. **重构**：创建一个新的 commit graph（生成新的 commit SHAs）。
5. **更新引用**：更新所有 references（branches, tags）以指向新的 commits。
6. **清理**：丢弃旧的 objects（除非你显式要求保留它们）。

因为它直接操作 **pack-file format** 且避开了 porcelain 层，它通常比 `git filter-branch` 快 **10–50 倍**。

### `--path` / `--file` 最常见的使用模式

```bash
# 1. 仅保留一个目录中的文件（最常见的用例）
git filter-repo --path src/backend/ --path docs/

# 2. 从所有地方删除一个文件（包括重命名后的路径）
git filter-repo --path logs/debug.log --invert-paths

# 3. 删除多个文件或文件夹
git filter-repo --path .env --path docker-compose.override.yml --path tests/ --invert-paths

# 4. 同上，但从文件中读取路径（非常方便）
git filter-repo --paths-from-file keep-these-paths.txt
# 或者
git filter-repo --paths-from-file remove-these-paths.txt --invert-paths
```

### 主要的 `--path` / `--file` 相关选项

| 选项 | 含义 | 最常见用法 | 备注 / 注意事项 |
| ------------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------ |
| `--path <path>` | 仅包含此路径（文件、文件夹、glob） | `--path src/ --path README.md` | 可以多次重复使用 |
| `--paths-from-file <file>` | 从文件中读取路径列表（每行一个），语义与 `--path` 相同 | `--paths-from-file keep.txt` | 处理 10 个以上路径时非常方便 |
| `--invert-paths` | **反转**选择：保留除所列路径之外的所有内容 | `--path secret.txt --invert-paths` | **删除**文件最常用的方式 |
| `--path-glob <pattern>` | 使用 fnmatch 风格的 glob 进行包含/排除 (`*.py`, `ci/*`) | `--path-glob '*/secrets/*' --invert-paths` | 排除操作**不一定**需要配合 `--invert-paths` |
| `--path-regex <regex>` | 使用 regular expression 进行包含/排除 | `--path-regex '.*\.bak$' --invert-paths` | 功能非常强大但容易出错 |
| `--use-base-name` | 使用 `--path` / `--path-glob` 时仅匹配文件名（而非完整路径） | `--path-glob '*.bak' --use-base-name` | 很少需要用到 |
| `--no-blobs-size-limit` | 即使是非常大的 blobs 也进行处理（默认限制约为 2 GiB） | — | 仅当你确定有巨大文件时使用 |

### 典型的实战命令模式 (2025–2026)

```bash
# 从所有位置删除单个敏感文件（包括重命名后的路径）
git filter-repo --path api-keys.json --invert-paths --force

# 删除文本文件中列出的多个文件
git filter-repo --paths-from-file sensitive-files.txt --invert-paths --force

# 仅保留前端代码 + 文档
git filter-repo --path frontend/ --path docs/ --path README.md --path LICENSE --force

# 使用 glob 删除所有 .env* 文件
git filter-repo --path-glob '.env*' --invert-paths --force

# 删除任何 "secrets" 文件夹下的所有内容
git filter-repo --path-glob '*/secrets/*' --invert-paths --force
```

### 几乎每个人都会用到的重要常用选项

- `--force`
  如果你已经在同一个 clone 的仓库中运行过一次 filter-repo，则需要此参数。

- `--dry-run`
  显示将要执行的操作，而不实际重写任何内容。

- `--analyze`
  在第一次运行前非常有用 —— 显示最大的文件、最大的 commits 以及路径统计信息。

- `--target <directory>`
  将过滤后的结果写入单独的目录，而不是覆盖当前 repo。

### 快速记忆模型

可以这样理解：

```
git filter-repo --path ...    →  "仅保留这些路径"
git filter-repo --path ... --invert-paths   →  "删除这些路径"
```

你可以组合使用普通的 `--path`、`--path-glob`、`--path-regex` 和 `--paths-from-file` —— 它们都会被**添加**到包含/排除列表中。

**References:**

- [https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt](https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt)
- [https://github.com/newren/git-filter-repo](https://github.com/newren/git-filter-repo)
