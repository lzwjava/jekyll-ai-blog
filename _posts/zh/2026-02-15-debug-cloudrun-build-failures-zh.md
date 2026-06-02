---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 排除 Cloud Run 构建故障
translated: true
type: note
---

问题：`gcloud run deploy` 命令失败并显示 "Build failed; check build logs for details" 且伴有 traceback —— 如何查找并修复该问题？

回答：

您的部署在 **Cloud Build** 阶段失败了（由 `--source .` 自动触发），该阶段负责根据您的源代码和 `Dockerfile` 构建 container image。

关键信息是：**"Build failed; check build logs for details"** —— 这意味着实际的错误（例如 Maven 编译失败、缺少 dependency、错误的 Dockerfile 指令、权限问题或 timeout）隐藏在 **Cloud Build logs** 中，而不是在简短的 gcloud 输出里。

### 第一步：查找 Build Logs（最快的方法）

1. **在 Google Cloud Console 中（最简单 - 推荐首选）**：
    * 访问：<https://console.cloud.google.com/cloud-build/builds?project=YOUR-PROJECT-ID>
    * 查看 **Build history** 列表（按最新排序）。
    * 找到针对您的服务（`blog-server`）的最新构建；它通常显示为 "FAILED" 或带有红色状态。
    * 点击进入 → 您将看到详细的分步日志。
    * 浏览各步骤（特别是 Maven/build 步骤或 Dockerfile 执行过程）以查找红色的错误行（例如 "Compilation failure", "Could not resolve dependencies", "COPY failed" 等）。
    * 控制台通常会显示一个直接链接，如：
        "Logs are available at <https://console.cloud.google.com/cloud-build/builds/abc123-xyz?project=>..."
        （gcloud 有时会在失败前打印此链接 —— 请检查您的终端回滚记录）。

2. **使用 gcloud CLI**：
    * 列出最近的构建以获取 BUILD_ID（最近失败的那一个）：

        ```bash
        gcloud builds list --limit=5 --filter="status=FAILURE"
        ```

    * 查找与您的部署匹配的 ID（长十六进制字符串，如 `abcdef12-3456-...`）以及触发器/源信息。

    * 查看该构建的完整日志：

        ```bash
        gcloud builds log BUILD_ID_HERE
        ```

    * 如果您想实时查看，可以添加 `--stream`（但既然已经失败了，普通模式即可）。
    * 或者通过管道传输给 less/grep：

        ```bash
        gcloud builds log BUILD_ID_HERE | less
        gcloud builds log BUILD_ID_HERE | grep -i error
        ```

### 第二步：Java/Spring Boot + Dockerfile 项目的常见原因及修复

看到日志后，请对照以下频繁出现的问题：

* **Maven 构建错误**（最常见）：
  * Dependency 解析失败 → 检查构建环境中的 internet/proxy，或根据需要添加 Maven `settings.xml`。
  * 测试失败 → 在 Dockerfile 中跳过测试：添加 `mvn clean package -DskipTests`。
  * 内存不足（Out of memory） → 增加构建资源或添加 `--set-build-env-vars MAVEN_OPTS="-Xmx2g"`。

* **Dockerfile 问题**：
  * 基础镜像错误（现代 Java 请使用 `openjdk:17-jdk-slim` 或 `eclipse-temurin:17`）。
  * App 未暴露/监听 `$PORT`（Cloud Run 设置 PORT=8080；您的 App 必须绑定到 `0.0.0.0:$PORT`）。
  * CMD/ENTRYPOINT 错误 → 确保它正确运行 JAR，例如：

        ```dockerfile
        CMD ["java", "-jar", "/app.jar", "--server.port=${PORT:-8080}"]
        ```

  * 多阶段构建在 copy 步骤中失败。

* **权限/配额问题**：
  * Cloud Build service account 缺少角色 → 确保 `PROJECT_NUMBER@cloudbuild.gserviceaccount.com` 拥有 `roles/run.builder` 和 `roles/artifactregistry.writer`（如果使用 Artifact Registry）。
  * 运行：`gcloud projects add-iam-policy-binding YOUR-PROJECT-ID --member=serviceAccount:YOUR_PROJECT_NUMBER@cloudbuild.gserviceaccount.com --role=roles/run.builder`

* **上传文件过大 / Timeout**：
  * 添加 `.gcloudignore` 文件来排除 `target/`、`.git/` 等目录（如前所述）。

* **Buildpack 回退**（如果没有 Dockerfile 或检测错误）：
  * 有时它会转而使用 buildpacks → 强制进行 Dockerfile 检测或指定 builder。

### 第三步：建议的后续行动（更快速且更可靠）

既然从源码部署失败了，可以切换到 **手动构建 + 部署**（您可以在本地控制构建过程）：

1. 在本地构建并测试：

    ```bash
    docker build -t blog-server:test .
    docker run -p 8080:8080 -e PORT=8080 blog-server:test
    ```

    → 先在本地修复所有错误。

2. 打标签（Tag）并推送到仓库：

    ```bash
    IMAGE="asia-southeast1-docker.pkg.dev/YOUR-PROJECT-ID/my-repo/blog-server:latest"
    docker build -t $IMAGE .
    gcloud auth configure-docker asia-southeast1-docker.pkg.dev
    docker push $IMAGE
    ```

3. 直接部署镜像：

    ```bash
    gcloud run deploy blog-server \
      --image $IMAGE \
      --region asia-southeast1 \
      --allow-unauthenticated \
      --port 8080 \
      --memory 1Gi
    ```

这会完全跳过远程源码上传和构建环节。

检查日志后，请在此处回复构建日志中的 **具体错误信息**（例如红色的部分）—— 我可以帮助定位准确的修复方案。

参考链接：

* [Troubleshoot Cloud Run issues](https://cloud.google.com/run/docs/troubleshooting)
* [Troubleshooting build errors - Cloud Build](https://cloud.google.com/build/docs/troubleshooting)
* [Store and view build logs - Cloud Build](https://cloud.google.com/build/docs/securing-builds/store-manage-build-logs)
* [gcloud builds log reference](https://cloud.google.com/sdk/gcloud/reference/builds/log)
* [Deploy from source code - Cloud Run](https://cloud.google.com/run/docs/deploying-source-code)
