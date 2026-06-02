---
audio: false
generated: true
lang: zh
layout: post
title: 高级Git：变基、合并、冲突解决与压缩提交
translated: true
type: note
---

本指南涵盖 `git rebase` 和 `git merge` 的高级用法、冲突解决、使用 ours 和 theirs 策略以及压缩提交。我将为每个主题提供简明解释和实用示例，重点介绍需要熟悉基本 Git 命令的高级工作流。

## 1. Git Merge：高级用法

`git merge` 将多个开发序列合并为统一的历史记录。高级用法包括处理复杂合并、使用合并策略和管理合并提交。

### 主要合并策略

- **Recursive（默认）**：处理多个共同祖先，适用于大多数合并场景。
  - 示例：`git merge --strategy=recursive 分支名称`
- **Ours**：保留当前分支的更改，丢弃被合并分支的更改。
  - 示例：`git merge --strategy=ours 功能分支`
- **Theirs**：并非真正的策略，但可通过其他方式模拟（参见下文冲突解决部分）。
- **Octopus**：一次性合并多个分支（适用于超过2个分支的情况）。
  - 示例：`git merge 分支1 分支2 分支3`

### 高级合并选项

- `--no-ff`：即使可以快进合并也强制创建合并提交，保留分支历史。
  - 示例：`git merge --no-ff 功能分支`
- `--squash`：将被合并分支的所有提交合并为当前分支上的单个提交。
  - 示例：`git merge --squash 功能分支 && git commit`
- `--allow-unrelated-histories`：合并没有共同历史的分支。
  - 示例：`git merge --allow-unrelated-histories 外部仓库分支`

### 示例：禁用快进的合并

```bash
git checkout main
git merge --no-ff feature-branch
# 创建合并提交，保留功能分支历史
```

## 2. Git Rebase：高级用法

`git rebase` 通过移动或修改提交来重写历史，创建线性历史记录。适用于清理分支历史，但会改变历史记录，因此在共享分支上需谨慎使用。

### 变基类型

- **标准变基**：将当前分支的提交重新应用到基础分支。
  - 示例：`git rebase main`（在 `feature-branch` 分支上操作时）
- **交互式变基**：允许编辑、压缩或重新排序提交。
  - 示例：`git rebase -i main`

### 交互式变基命令

运行 `git rebase -i <基准>`（例如 `git rebase -i HEAD~3` 表示最近3个提交）。这会打开包含以下命令的编辑器：

- `pick`：保留该提交不变
- `reword`：编辑提交信息
- `edit`：暂停变基以修改提交
- `squash`：与前一提交合并
- `fixup`：类似 squash，但丢弃该提交信息
- `drop`：移除该提交

### 示例：交互式变基

压缩最近3个提交：

```bash
git rebase -i HEAD~3
# 在编辑器中将需要合并的提交的 "pick" 改为 "squash" 或 "fixup"
# 保存退出以完成操作
```

### 变基到不同基准

将分支移动到新基准（例如将 `feature-branch` 从 `old-base` 移动到 `main`）：

```bash
git rebase --onto main old-base feature-branch
```

### 保留合并提交的变基

默认情况下变基会扁平化合并提交。要保留它们：

```bash
git rebase -i --preserve-merges main
```

### 中止变基

如果出现问题：

```bash
git rebase --abort
```

## 3. 解决合并/变基冲突

当 Git 无法自动协调更改时会发生冲突。`merge` 和 `rebase` 操作都可能产生冲突，解决方法类似。

### 解决冲突步骤

1. **识别冲突**：Git 暂停操作并列出冲突文件。
   - 合并时：`git status` 显示冲突文件
   - 变基时：在 `git rebase -i` 过程中逐提交解决冲突
2. **编辑冲突文件**：打开文件查找冲突标记：

   ```text
   <<<<<<< HEAD
   您的更改
   =======
   传入的更改
   >>>>>>> 分支名称
   ```

   手动编辑保留所需更改后移除标记
3. **标记为已解决**：
   - 合并时：`git add <文件>`
   - 变基时：`git add <文件>`，然后 `git rebase --continue`
4. **完成流程**：
   - 合并：`git commit`（Git 可能自动生成提交信息）
   - 变基：`git rebase --continue` 直到所有提交应用完成

### 示例：解决合并冲突

```bash
git checkout main
git merge feature-branch
# 发生冲突
git status  # 列出冲突文件
# 编辑文件解决冲突
git add resolved-file.txt
git commit  # 完成合并
```

### 示例：解决变基冲突

```bash
git checkout feature-branch
git rebase main
# 发生冲突
# 编辑冲突文件
git add resolved-file.txt
git rebase --continue
# 重复直至变基完成
```

## 4. 在冲突解决中使用 Ours 和 Theirs

冲突解决过程中可能需要偏向某一方的更改（`ours` 或 `theirs`）。`ours` 和 `theirs` 的具体含义取决于操作类型。

### 合并场景：Ours 与 Theirs

- `ours`：当前分支的更改（例如 `main`）
- `theirs`：被合并分支的更改（例如 `feature-branch`）
- 使用 `--strategy-option`（`-X`）标志：
  - 保留 ours：`git merge -X ours feature-branch`
  - 保留 theirs：`git merge -X theirs feature-branch`

### 变基场景：Ours 与 Theirs

- `ours`：基础分支的更改（例如 `main`）
- `theirs`：被变基分支的更改（例如 `feature-branch`）
- 在变基冲突解决过程中使用：

  ```bash
  git checkout --ours file.txt  # 保留基础分支版本
  git checkout --theirs file.txt  # 保留被变基分支版本
  git add file.txt
  git rebase --continue
  ```

### 示例：合并时使用 Theirs

将 `feature-branch` 合并到 `main` 并优先采用 `feature-branch` 的更改：

```bash
git checkout main
git merge -X theirs feature-branch
```

### 示例：变基时使用 Ours

将 `feature-branch` 变基到 `main` 时，通过保留 `main` 的版本来解决冲突：

```bash
git checkout feature-branch
git rebase main
# 发生冲突
git checkout --ours file.txt
git add file.txt
git rebase --continue
```

## 5. 压缩提交

压缩提交将多个提交合并为一个，创建更清晰的历史记录。通常通过交互式变基实现。

### 压缩提交步骤

1. 对目标提交启动交互式变基：

   ```bash
   git rebase -i HEAD~n  # n = 要压缩的提交数量
   ```

2. 在编辑器中将需要合并的提交的 `pick` 改为 `squash`（或 `fixup`）
3. 保存退出。Git 可能会提示编辑合并后的提交信息
4. 推送更新后的历史记录（如果已共享则需强制推送）：

   ```bash
   git push --force-with-lease
   ```

### 示例：压缩3个提交

```bash
git rebase -i HEAD~3
# 编辑器显示：
# pick abc123 提交1
# pick def456 提交2
# pick ghi789 提交3
# 改为：
# pick abc123 提交1
# squash def456 提交2
# squash ghi789 提交3
# 保存退出
# 按提示编辑合并后的提交信息
git push --force-with-lease
```

### 合并时压缩

在合并分支时压缩所有提交：

```bash
git checkout main
git merge --squash feature-branch
git commit  # 创建单个提交
```

## 最佳实践与技巧

- **变基前备份**：变基会重写历史。创建备份分支：

  ```bash
  git branch backup-branch
  ```

- **避免变基共享分支**：在公共分支上重写历史可能导致协作者出现问题。改用 `merge`
- **安全使用 `--force-with-lease`**：推送重写后的历史时，此选项可防止覆盖他人的更改
- **解决冲突后测试**：确保项目构建和测试通过
- **使用冲突解决工具**：VS Code、SourceTree 或 `git mergetool` 等 GUI 工具可简化冲突解决
- **团队沟通**：在团队协作中，协调变基操作以避免冲突

## 常见陷阱

- **变基中丢失工作**：始终备份或使用 `git reflog` 恢复丢失的提交
- **误用 Ours/Theirs**：仔细检查在合并与变基场景中哪个分支是 ours 与 theirs
- **未经协调强制推送**：强制推送共享分支可能影响团队成员。使用 `--force-with-lease` 并保持沟通

## 错误恢复

- **查看历史**：使用 `git reflog` 查看先前状态并恢复丢失的提交：

  ```bash
  git reflog
  git checkout <提交哈希>
  ```

- **重置到合并前状态**：

  ```bash
  git reset --hard HEAD^  # 撤销最后一次合并提交
  ```

- **中止合并**：如果合并出现问题：

  ```bash
  git merge --abort
  ```

本指南为高级 Git 工作流提供了坚实基础。对于特定场景或错误，请随时告知，我可以深入探讨或搜索实时解决方案！
