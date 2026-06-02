---
audio: false
generated: true
lang: zh
layout: post
title: 预提交钩子中的阶段变更
translated: true
type: note
---

若要在预提交钩子中将 `update_notes_link.py` 脚本的更改整合到当前提交（而非创建独立提交），需修改钩子逻辑：仅暂存更新文件而不单独提交。这样 Python 脚本的更改就会包含在用户的提交中。以下是修改后的预提交钩子脚本实现方案。

### 核心调整
- **取消独立提交**：钩子不再执行 `git commit`，而是通过 `git add` 暂存更新文件使其归入用户提交
- **保留原始提交信息**：不创建新提交可确保用户原提交信息不被覆盖
- **错误处理**：若 Python 执行失败，钩子将以非零状态退出终止提交

### 预提交钩子脚本

```x-shellscript
#!/bin/bash

# 运行 update_notes_link.py 脚本并捕获输出
OUTPUT=$(python scripts/generate/update_notes_link.py 2>&1)
EXIT_CODE=$?

# 检查 Python 脚本执行状态
if [ $EXIT_CODE -ne 0 ]; then
    echo "错误：update_notes_link.py 执行失败，退出码 $EXIT_CODE"
    echo "$OUTPUT"
    exit 1
fi

# 检查目标文件是否被更新
if echo "$OUTPUT" | grep -q "Updated original/2025-01-11-notes-en.md"; then
    echo "笔记链接已更新，正在为当前提交暂存更改"

    # 暂存相关文件
    git add original/2025-01-11-notes-en.md
    git add _posts/en/*.md

    # 验证文件暂存状态
    if ! git diff --cached --quiet; then
        echo "更改已成功暂存"
    else
        echo "暂无需要暂存的更改"
    fi
else
    echo "original/2025-01-11-notes-en.md 无更新，无需暂存附加文件"
fi

# 正常退出以继续提交流程
exit 0
```

### 脚本逻辑解析

- **Shebang声明**：确保脚本在 Bash 环境中运行
- **执行Python脚本**：运行 `python scripts/generate/update_notes_link.py` 并同步捕获输出及退出码
- **错误处理**：检测 Python 退出码（`$EXIT_CODE`），非零值时终止流程并输出错误信息
- **输出检查**：通过 `grep` 验证 `original/2025-01-11-notes-en.md` 的更新状态
- **文件暂存**：对指定文件（`original/2025-01-11-notes-en.md` 与 `_posts/en/*.md`）执行 `git add` 操作
- **取消提交**：跳过 `git commit` 使用户原始提交命令能包含已暂存更改
- **状态反馈**：输出提示信息告知用户暂存操作结果
- **退出处理**：返回 `0` 状态码允许提交继续执行（Python 脚本失败情况除外）

### 钩子配置流程

1. **创建钩子文件**：
   - 将脚本保存至仓库的 `.git/hooks/pre-commit`

2. **设置可执行权限**：
   ```bash
   chmod +x .git/hooks/pre-commit
   ```

3. **测试验证**：
   - 修改文件或确保 Python 脚本会更新 `original/2025-01-11-notes-en.md`
   - 执行 `git commit -m "提交说明"`
   - 通过 `git diff --cached`（提交前）或 `git show`（提交后）验证更新文件是否已包含

### 使用 pre-commit 框架（可选方案）

若倾向使用 `pre-commit` 框架，可通过 `.pre-commit-config.yaml` 实现相同逻辑：

1. **安装框架**：
   ```bash
   pip install pre-commit
   ```

2. **创建配置文件**：

```yaml
repos:
- repo: local
  hooks:
  - id: update-notes-links
    name: 更新笔记链接
    entry: bash -c '
      OUTPUT=$(python scripts/generate/update_notes_link.py 2>&1);
      EXIT_CODE=$?;
      if [ $EXIT_CODE -ne 0 ]; then
        echo "错误：update_notes_link.py 执行失败，退出码 $EXIT_CODE";
        echo "$OUTPUT";
        exit 1;
      fi;
      if echo "$OUTPUT" | grep -q "Updated original/2025-01-11-notes-en.md"; then
        echo "笔记链接已更新，正在为当前提交暂存更改";
        git add original/2025-01-11-notes-en.md;
        git add _posts/en/*.md;
        if ! git diff --cached --quiet; then
          echo "更改已成功暂存";
        else
          echo "暂无需要暂存的更改";
        fi;
      else
        echo "original/2025-01-11-notes-en.md 无更新，无需暂存附加文件";
      fi'
    language: script
    files: ^(original/2025-01-11-notes-en\.md|_posts/en/.*\.md)$
    stages: [commit]
```

3. **安装钩子**：
   ```bash
   pre-commit install
   ```

4. **功能测试**：
   - 提交匹配 `files` 正则表达式的文件变更（如 `original/2025-01-11-notes-en.md` 或 `_posts/en/*.md`）
   - 确认钩子正常执行，必要时暂存更改并包含至提交

### 与原 GitHub Actions 的差异

- **提交机制**：GitHub Actions 会创建新提交，而钩子将更改整合至现有提交
- **推送操作**：钩子在本地运行，需用户手动执行 `git push`
- **错误控制**：通过退出码检测确保 Python 脚本不会静默失败
- **用户配置**：无需设置 `git config user.name` 与 `user.email`，直接沿用用户本地配置

### 注意事项

- **脚本依赖**：确保 `scripts/generate/update_notes_link.py` 存在且具备可执行权限，检查环境变量与依赖可用性
- **路径验证**：确认 `original/2025-01-11-notes-en.md` 和 `_posts/en/*.md` 路径与仓库结构匹配
- **故障防护**：Python 脚本失败时将阻止提交，避免部分更新被误暂存
- **全面测试**：通过 `git commit` 验证更改正确暂存且未产生额外提交，使用 `git show` 检查提交内容

### 验证步骤

1. 修改文件或触发 Python 脚本更新 `original/2025-01-11-notes-en.md`
2. 执行 `git commit -m "测试提交"`
3. 运行 `git show` 确认更新文件已包含至提交且保留原提交信息
4. 确认未产生额外提交（如 `chore(notes): Update notes links` 类提交）

如需进一步调整（如特定错误处理或扩展暂存文件范围），可随时提出优化需求！
