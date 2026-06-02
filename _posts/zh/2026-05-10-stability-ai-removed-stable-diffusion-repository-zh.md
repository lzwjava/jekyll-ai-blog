---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Stability AI 移除了 Stable Diffusion 仓库
translated: true
type: note
---

**问题：** GitHub 仓库 `git@github.com:Stability-AI/stablediffusion.git`（如 `.git/config` 文件中所示）为何停止工作/被关闭？

**回答：**

## `Stability-AI/stablediffusion` 仓库已被移除

您的本地项目 `~/projects/stablediffusion` 的 Git 远程仓库配置指向 `git@github.com:Stability-AI/stablediffusion.git`。这个远程地址现已**失效**——该仓库在 GitHub 上已不复存在。

### 发生了什么？

`https://github.com/Stability-AI/stablediffusion` 仓库已无法访问，可能是被 Stability AI 删除或设为私有。

根据 Stability AI 的官方说明，原因与**模型弃用和法规合规**有关。Stability AI 正式弃用了 Stable Diffusion 2.0 和 2.1，作为其清理和整合模型产品、并为 2026 年欧盟 AI 法案合规要求做准备的一部分。这些模型已被性能更强、更安全、更对齐的新架构所超越，继续维护它们不符合公司的长期路线图。

### 影响

此次移除仅影响**新建安装**时尝试克隆该仓库的操作。已克隆该仓库的现有安装不受影响。

### 您可以做什么？

由于您的 `.git/config` 仍指向现已删除的仓库，任何针对 `origin` 的 `git fetch`、`git pull` 或 `git push` 都会失败，并显示：

```
remote: Repository not found.
fatal: repository 'https://github.com/Stability-AI/stablediffusion.git/' not found
```

**您的选项：**

1. **使用社区镜像** — AUTOMATIC1111 WebUI 项目已将其安装程序修改为使用社区分支。他们将 stable diffusion 仓库的 URL 从 `https://github.com/Stability-AI/stablediffusion.git` 切换到了分支 `https://github.com/w-e-w/stablediffusion.git`。您可以类似地更新自己的远程仓库：

   ```bash
   git remote set-url origin https://github.com/w-e-w/stablediffusion.git
   ```

2. **保持本地副本不变** — 如果您已有完整的本地克隆，日常工作中无需远程仓库。只是无法拉取上游更新（反正上游已经不存在了）。

3. **切换到维护中的替代方案** — 考虑迁移到积极维护的 SD 仓库，例如：
   - [CompVis/stable-diffusion](https://github.com/CompVis/stable-diffusion)（原始 SD 1.x 代码库）
   - [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
   - [comfyanonymous/ComfyUI](https://github.com/comfyanonymous/ComfyUI)

---

**参考链接：**

- [AUTOMATIC1111 WebUI Issue #17204 – 仓库未找到](https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/17204)
- [AUTOMATIC1111 WebUI Discussion #17212 – 克隆失败的修复](https://github.com/AUTOMATIC1111/stable-diffusion-webui/discussions/17212)
- [HuggingFace Discussion – SD 2.1 弃用声明](https://huggingface.co/spaces/stabilityai/stable-diffusion-3.5-large/discussions/648)
