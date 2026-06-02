---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 从 Git 历史记录中删除文件
translated: true
type: note
---

**Question:** 如何使用 git filter-repo 从 Git history 中删除文件？

**Answer:**

`git filter-repo` 是目前推荐的现代工具（比已弃用的 `git filter-branch` 或 BFG 更快、更安全），用于重写 Git history，包括从仓库的所有 commit 中永久删除特定文件。

### Prerequisites
- 如果尚未安装，请安装 `git-filter-repo`（它默认不包含在 Git 中）。
  安装说明：https://github.com/newren/git-filter-repo#installation
- **首先备份你的 repository**，因为重写 history 是破坏性的，并会改变 commit hashes。
- 建议在一个 **fresh clone** 的仓库上操作，以避免安全检查：
  ```
  git clone <repository-url> myrepo-clean
  cd myrepo-clean
  ```

### Basic Command to Remove a Single File
要从整个 history 中完全删除一个文件（例如 `path/to/secret.txt`）：

```
git filter-repo --path path/to/secret.txt --invert-paths
```

- `--path <file>`：指定目标文件（相对于仓库根目录的路径）。
- `--invert-paths`：保留除指定文件以外的所有文件。如果没有此选项，它将仅保留指定文件并删除其他所有内容。

你可以指定多个文件：
```
git filter-repo --path file1.txt --path file2.config --invert-paths
```

### For Folders/Directories
要删除整个目录（例如 `old_folder/`）：
```
git filter-repo --path old_folder/ --invert-paths
```

对于更复杂的模式（例如所有匹配 glob 的文件）：
```
git filter-repo --path-glob '*.secret' --invert-paths
```
使用 `--path-glob` 处理 globs，使用 `--path-regex` 处理正则表达式，或者如果仅按文件名匹配（忽略路径）则使用 `--use-base-name`。

### Applying to All Branches and Tags
默认情况下，`git filter-repo` 会影响所有 refs。若要明确指定：
```
git filter-repo --path path/to/secret.txt --invert-paths --force
```
（如果需要，`--force` 标志可以绕过“fresh clone”安全检查。）

### After Rewriting History
1. 验证文件已移除：
   ```
   git log --all -- path/to/secret.txt
   ```
   （应当不显示任何结果。）

2. 清理：
   该工具通常会自动执行 repack，但你也可以运行：
   ```
   git reflog expire --expire=now --all
   git gc --prune=now
   ```

3. 将更改推送到 remote（由于 history 已重写，需要 force push）：
   ```
   git push origin --force --all
   git push origin --force --tags
   ```

### Important Warnings
- **History 重写会更改受影响 commit 之后的所有 commit ID**。所有协作者必须重新 clone 仓库或手动恢复（参见 `git filter-repo` 文档中的说明）。
- 与你的团队协调：关闭所有打开的 pull requests，通知其他成员。
- 如果文件中包含敏感数据且已被推送，旧的 commits 在 remote 上可能仍会暂时可被访问（例如 GitHub 会短时间缓存它们）。
- 对于敏感数据删除，如果使用 GitHub，请参考 GitHub 的完整指南。

此过程会从 history 中永久擦除文件，如果该文件很大，还可以减小仓库体积。

**References:**

- [GitHub - newren/git-filter-repo](https://github.com/newren/git-filter-repo)
- [GitHub Docs: Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
