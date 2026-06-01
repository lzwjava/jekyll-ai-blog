---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GitHub存档到HF同步
translated: true
type: note
---

## 摘要

### 1. 将 GitHub 远程仓库从 HTTPS 切换为 SSH
- 将 `origin` 从 `https://github.com/lzwjava/zz.git` 改为 `git@github.com:lzwjava/zz.git`
- 使用 `git pull --rebase` 拉取——远程没有新提交，因此无操作
- GitHub 仓库 `lzwjava/zz` 处于**归档**状态（只读）——这是有意为之，保持现状

### 2. 使用 Hugging Face 进行身份验证
- `huggingface-cli` 已弃用 → 迁移至 `hf` CLI
- 使用 `hf auth login --token hf_...` 登录
- Token 已保存至 `~/.cache/huggingface/token`

### 3. 配置 HF 远程仓库
- 最初添加的 HF 远程仓库指向 `datasets/lzwjava/zz`——错误（仓库未找到，且 datasets 类型不正确）
- 修正为 **models 仓库**：`https://huggingface.co/lzwjava/zz`
- 添加为名为 `hf` 的远程仓库

### 4. 解决历史分叉问题
- HF 仓库有 3 个独立的提交（通过 HF 网页界面/上传创建）：
  - `3dbedad` 初始提交
  - `0980be1` 使用 huggingface_hub 上传文件夹
  - `3894b4d` 更新 README
- 本地历史完全不同（不相关的根提交）
- **强制推送**本地 `main`（8977f51）到 HF，覆盖 HF 的旧提交

### 当前状态
```
origin  → git@github.com:lzwjava/zz.git  （已归档，只读）
hf      → https://huggingface.co/lzwjava/zz  （活跃，已同步）
```

本地分支 `main` 与 HF 同步。未来工作流：`git push hf main` 进行同步。