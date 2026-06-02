---
audio: false
generated: true
lang: zh
layout: post
title: Git预添加钩子的替代方案
translated: true
type: note
---

Git 没有内置的 `pre-add` 钩子，但你可以通过以下几种方式实现类似功能：

### 1. **Git 别名（推荐方案）**
创建一个在调用 `git add` 前执行检查的 Git 别名：

```bash
git config --global alias.safe-add '!your-pre-add-script.sh && git add'
```

之后使用 `git safe-add` 替代 `git add`。

### 2. **封装脚本**
在 PATH 环境变量路径下创建名为 `git-pre-add` 的脚本：
1. 执行预添加检查
2. 检查通过后调用 `git add`

```bash
#!/bin/bash
# 在此处编写预添加验证逻辑
if [ 某些判断条件 ]; then
  git add "$@"
else
  echo "预添加检查未通过"
  exit 1
fi
```

### 3. **利用现有钩子**
可通过创新方式利用现有钩子：
- **pre-commit**：虽然此钩子在添加后、提交前运行，但可在此检查暂存区文件
- **prepare-commit-msg**：与 pre-commit 类似但触发时机更早

### 4. **文件系统监控**
如需更高级功能，可使用：
- **inotifywait**（Linux）监控工作目录
- **fswatch**（Mac）实现类似功能

### 预添加检查脚本示例
这是一个防止添加含尾部空白字符文件的简单示例：

```bash
#!/bin/bash
# 保存为 .git/hooks/pre-commit（但作用于暂存区文件）

# 检查空白字符错误
if git diff --cached --check; then
  exit 0
else
  echo "在暂存区文件中发现空白字符错误"
  exit 1
fi
```

注意：请确保钩子脚本具有可执行权限（使用 `chmod +x script.sh`）。

需要针对您的具体使用场景展开说明某个方案吗？
