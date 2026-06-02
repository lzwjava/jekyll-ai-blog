---
audio: false
generated: true
lang: zh
layout: post
title: Git储藏
translated: true
type: note
---

以下是关于如何有效使用 `git stash` 以及频繁切换分支/标签时处理未提交变更的方法：

## 使用 `git stash`

`git stash` 是一个功能强大的命令，允许您临时保存未提交的变更（包括已暂存和未暂存的），并将工作目录恢复到最近一次提交的状态。当您需要切换分支或处理其他任务，但又不想提交当前未完成的工作时，这个功能非常有用。

以下是常见的 `git stash` 操作详解：

**1. 暂存当前变更：**

```bash
git stash
```

该命令会保存您的未提交变更，将其存储为新的暂存项，并清理工作目录。您将看到类似如下的消息：

```
Saved working directory and index state WIP on <your_branch>: <commit_hash> <commit_message>
```

**2. 添加描述信息暂存：**

为暂存项添加描述信息很有帮助，特别是在有多个暂存项时：

```bash
git stash save "您的描述信息"
# 或
git stash push -m "您的描述信息"
```

**3. 列出暂存项：**

要查看所有已保存的暂存项列表，请使用：

```bash
git stash list
```

这将显示暂存项列表，通常格式如下：

```
stash@{0}: On <branch_name>: <commit_hash> <stash_message>
stash@{1}: WIP on <another_branch>: ...
```

`stash@{0}` 是最新的暂存项。

**4. 应用暂存项：**

要恢复暂存项中的变更，可以使用 `git stash apply`。这会应用变更但保留暂存项在列表中。默认情况下，它会应用最新的暂存项（`stash@{0}`）。

```bash
git stash apply
# 或应用特定暂存项：
git stash apply stash@{1}
```

**5. 应用并删除暂存项：**

如果您想应用变更并立即从列表中删除暂存项，请使用 `git stash pop`。此操作也默认针对最新暂存项。

```bash
git stash pop
# 或弹出特定暂存项：
git stash pop stash@{1}
```

**6. 查看暂存项详情：**

您可以使用以下命令查看暂存项中的变更摘要：

```bash
git stash show
# 或查看特定暂存项：
git stash show stash@{2}
```

要查看暂存项的完整差异，添加 `-p` 或 `--patch` 标志：

```bash
git stash show -p stash@{0}
```

**7. 暂存未跟踪文件：**

默认情况下，`git stash` 仅暂存已跟踪文件的变更。要包含未跟踪文件，请使用 `-u` 或 `--include-untracked` 选项：

```bash
git stash -u
git stash save -u "包含未跟踪文件的暂存"
```

**8. 同时暂存被忽略的文件：**

要包含未跟踪文件和被忽略的文件，请使用 `-a` 或 `--all` 选项：

```bash
git stash -a
git stash save -a "包含所有文件的暂存"
```

**9. 从暂存项创建分支：**

如果您暂存了一些变更，现在想在新分支上处理它们，可以直接从暂存项创建分支：

```bash
git stash branch <新分支名称> stash@{0}
# 或针对最新暂存项：
git stash branch <新分支名称>
```

此命令基于创建暂存项时的提交创建一个新分支，将暂存的变更应用到新分支，然后丢弃该暂存项。

**10. 删除暂存项：**

* 删除特定暂存项：

    ```bash
    git stash drop stash@{1}
    ```

* 删除所有暂存项：

    ```bash
    git stash clear
    ```

## 频繁切换分支或标签时处理未提交变更

以下是使用 `git stash` 在存在未提交变更时频繁切换分支或标签的方法：

**场景 1：切换到另一个分支**

1. **暂存当前变更：**

    ```bash
    git stash save "当前分支的工作进度"
    ```

2. **切换到目标分支：**

    ```bash
    git checkout <目标分支名称>
    # 或使用较新的 `git switch` 命令：
    git switch <目标分支名称>
    ```

3. **在目标分支上完成您的工作。**
4. **当需要返回原始分支时：**

    ```bash
    git checkout <原始分支名称>
    # 或
    git switch <原始分支名称>
    ```

5. **重新应用暂存的变更：**

    ```bash
    git stash pop  # 如果您想应用并删除暂存项
    # 或
    git stash apply # 如果您想应用但保留暂存项
    ```

6. **解决可能出现的合并冲突**（如果原始分支自您暂存后发生了显著变化）。

**场景 2：切换到标签**

直接切换到标签会使您处于"分离 HEAD"状态，通常不建议在此状态下进行提交。如果您只是想检查特定标签的代码：

1. **暂存当前变更：**

    ```bash
    git stash save "检查标签前的工作进度"
    ```

2. **切换到标签：**

    ```bash
    git checkout <标签名称>
    ```

3. **检查代码。**
4. **返回您的分支：**

    ```bash
    git checkout <您的分支名称>
    # 或
    git switch <您的分支名称>
    ```

5. **重新应用暂存的变更：**

    ```bash
    git stash pop
    # 或
    git stash apply
    ```

**场景 3：基于标签创建新分支并应用暂存变更**

如果您想基于特定标签开始新功能开发或修复，并且有来自先前上下文的暂存变更：

1. **暂存当前变更（如果尚未暂存）：**

    ```bash
    git stash save "工作进度"
    ```

2. **从标签创建新分支：**

    ```bash
    git checkout -b <新分支名称> <标签名称>
    # 或
    git switch -c <新分支名称> <标签名称>
    ```

3. **将暂存变更应用到新分支：**

    ```bash
    git stash pop # 或 git stash apply
    ```

4. **解决可能出现的合并冲突。**

**重要注意事项：**

* **保持暂存项组织有序：** 使用描述性信息以便轻松识别暂存项。
* **暂存项是本地存储：** 暂存项存储在您的本地仓库中，不会推送到远程仓库。
* **可能存在冲突：** 当重新应用暂存项时，如果应用到的分支自创建暂存项以来发生了显著变化，可能会出现合并冲突。您需要手动解决这些冲突。
* **考虑创建临时分支：** 对于尚未准备好提交的长期工作，创建临时分支可能比过度依赖暂存项更好。您可以轻松在分支之间切换并提交进度。

通过有效使用 `git stash`，即使存在未提交的变更，您也可以无缝切换分支和标签，从而实现更灵活高效的工作流程。请记得管理好您的暂存项，并准备好处理可能出现的合并冲突。
