---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 调试 Gcloud Run 部署挂起问题
translated: true
type: note
---

Question: gcloud run deploy 命令卡住或挂起，gcloud 有 verbose 选项吗？

Answer:

是的，**gcloud** 支持 `--verbosity` 标志来获取更详细的输出，这在排查部署挂起或耗时异常时非常有用。

### 如何增加详细程度 (Verbosity)

运行命令时加上以下选项之一（级别越高，输出越多）：

```bash
gcloud run deploy blog-server \
  --source . \
  --region asia-northeast1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --verbosity=debug
```

常用级别（从最详细到最简略）：

- `--verbosity=debug`   → 显示详细步骤、API 调用、重试等（推荐用于排查挂起问题）
- `--verbosity=info`    → 比默认多，但比 debug 简洁
- `--verbosity=warning` → 接近默认值
- `--verbosity=error`   → 最少输出

你也可以进行全局设置（影响所有 gcloud 命令）：

```bash
gcloud config set core/verbosity debug
```

（稍后可以使用 `gcloud config set core/verbosity warning` 重置，或者直接在具体命令中省略 `--verbosity`。）

### 为什么在执行 `--source .` 时会卡住/挂起

`--source .` 标志会触发：

1. 将源码上传到 Cloud Build
2. 自动构建 container（如果有 `Dockerfile` 则使用它，否则使用 Cloud Buildpacks）
3. 部署到 Cloud Run

导致长时间挂起的常见原因（尤其是显示 "Uploading sources..." 或 "Building and deploying..." 时）：

- **项目过大 / 文件过多** — Maven 在构建期间下载依赖，巨大的 `target/` 文件夹，git 历史记录，node_modules 等 → 导致上传时间极长。
  - **修复建议**：添加 `.gcloudignore` 文件（类似于 `.gitignore`）来排除不必要的文件/文件夹（例如 `target/`, `.git/`, `node_modules/`, `logs/`）。示例如下：

    ```
    .git
    target/
    *.log
    node_modules/
    .mvn/
    ```

- **网络慢 / 上传文件过大** — 特别是当你处于慢速连接或使用 VPN 时。
- **Build 速度慢** — 如果使用 Maven，它可能正在解析依赖、编译、运行测试等（即使你有 `Dockerfile`，Cloud Build 仍然会运行这些步骤）。
- **已知的 Cloud Build / Cloud Run 后端延迟** — 有时会挂起 10–30 分钟以上，然后报错 "deadline exceeded" 或在很久之后才成功。
- **权限 / Quota (配额) 问题** — Cloud Build 或 Artifact Registry 缺少必要的 role。

### 快速规避方案 / 更快的替代方法

1. **手动 Build & Push 镜像**（避免源码上传缓慢）：

   ```bash
   docker build -t gcr.io/$(gcloud config get-value project)/blog-server:latest .
   docker push gcr.io/$(gcloud config get-value project)/blog-server:latest

   gcloud run deploy blog-server \
     --image gcr.io/$(gcloud config get-value project)/blog-server:latest \
     --region asia-northeast1 \
     --allow-unauthenticated \
     --port 8080 \
     --memory 1Gi
   ```

   对于频繁部署，这种方式通常快得多。

2. **使用 Artifact Registry** 而非 gcr.io（现代推荐做法）：
   创建 repository：`gcloud artifacts repositories create my-repo --repository-format=docker --location=asia-northeast1`
   然后进行 tag/push：`asia-northeast1-docker.pkg.dev/YOUR-PROJECT/my-repo/blog-server:latest`

3. **检查 Cloud Build 运行日志**（即使 CLI 挂起也可查看）：
   - 访问 <https://console.cloud.google.com/cloud-build/builds>
   - 找到由你的部署触发的最新 build → 查看详细步骤或错误。

4. **添加 `--async`** 让 CLI 立即返回：

   ```bash
   gcloud run deploy ... --async
   ```

   然后在 Console 中监控，或使用 `gcloud run services describe blog-server --region asia-northeast1`。

先尝试使用 `--verbosity=debug` 运行 — 它会精确显示时间花在了哪里（例如：正在上传 X MB，等待 build 步骤 Y）。如果仍然无限期挂起（超过 20–30 分钟），请取消 (Ctrl+C)，通过 `.gcloudignore` 清理不必要的文件，或切手动推送镜像。

References:

- [gcloud CLI overview – verbosity flag](https://docs.cloud.google.com/sdk/gcloud)
- [Deploy services from source code | Cloud Run](https://docs.cloud.google.com/run/docs/deploying-source-code)
- [gcloud run deploy reference](https://docs.cloud.google.com/sdk/gcloud/reference/run/deploy)
- [Troubleshoot Cloud Run issues](https://docs.cloud.google.com/run/docs/troubleshooting)
