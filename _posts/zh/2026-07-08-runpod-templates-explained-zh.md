---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RunPod 模板详解
translated: true
type: note
---

问题：在RunPod中，“Your templates”指的是什么？当它说“预先配置你的Docker镜像一次，然后在Pods和Serverless中重复使用它们”时，是什么意思？

答案：

RunPod **模板** 只是一个容器的保存规范——它是位于Docker镜像之上的元数据层，而非镜像本身。你只需定义一次，之后在启动计算资源时直接引用它，无需每次都重新输入相同的配置。

**模板实际存储的内容：**

```
Template = {
  container_image: "docker.io/you/your-image:tag",  # 来自Docker Hub / GHCR / 私有仓库
  container_disk_size_gb: 20,
  volume_disk_size_gb: 50,          # 持久化卷（如有）
  volume_mount_path: "/workspace",
  docker_start_command: "python3 rp_handler.py",  # 或入口点覆盖
  env_vars: {"HF_TOKEN": "<SECRET>", "MODEL_NAME": "..."},
  ports: "8888/http,22/tcp",        # Pod的暴露端口（Jupyter、SSH）
  is_serverless: false,             # 影响哪些表面可以使用它
}
```

**Pods vs Serverless——同一模板，不同运行时语义：**

| | Pods | Serverless |
| --- | --- | --- |
| 生命周期 | 长期运行，手动启停 | 临时工作器，按需启动，缩至零 |
| 入口点 | 通常通过SSH/Jupyter进入运行中的容器 | 必须调用 `runpod.serverless.start({"handler": handler})` |
| 计费 | 运行时按小时计费 | 按处理请求的实际秒数计费 |
| 网络 | 暴露端口（8888、22等） | 无暴露端口——请求/响应通过RunPod的队列进行 |

同一Docker镜像通常不能直接同时用于两者：Pod镜像预期无限期运行并提供交互式访问（SSH、Jupyter），而Serverless镜像必须实现RunPod Python SDK的处理程序模式，并在每个作业后优雅退出——一个GPU Cloud模板如果没有Serverless处理程序，则无法在Serverless中工作，因此不建议将设计用于Pods的镜像用于Serverless。

因此，“预先配置一次，在Pods和Serverless中重复使用”实际意味着：你可以将*多个*端点/Pod配置指向*同一底层镜像*（如果你构建得足够通用——例如，一个同时包含交互式入口点和由环境变量控制的`rp_handler.py`的镜像），而且每次部署时无需重新定义磁盘大小、环境变量、暴露端口等。这是一种部署配置的DRY机制，而非两个运行时之间的神奇兼容层。

**如果你确实希望一个镜像同时服务于两者，实用的构建模式：**

```dockerfile
FROM nvidia/cuda:12.4.0-runtime-ubuntu22.04
COPY . /workspace
WORKDIR /workspace
RUN pip install runpod torch transformers

# entrypoint.sh在容器启动时决定模式
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

```bash
#!/bin/bash
# entrypoint.sh
if [ "$RUNPOD_SERVERLESS" = "1" ]; then
    exec python3 rp_handler.py   # runpod.serverless.start(...)
else
    exec /start.sh               # 用于交互式Pod使用的jupyter lab / sshd
fi
```

然后一个模板，两个部署目标：在创建Serverless端点时将 `RUNPOD_SERVERLESS=1` 作为环境变量覆盖，对于Pod则不设置该变量。

**管理位置：** `console.runpod.io/serverless/user/templates` 用于Serverless作用域的模板，以及对应的Pods模板页面用于GPU Cloud——模板也可以通过RunPod Python SDK编程方式创建，例如 `runpod.create_pod("test", "runpod/stack", "NVIDIA GeForce RTX 3070")`，如果你希望在CI/CD中脚本化模板创建，而不是通过UI点击。

参考：

- [Runpod Serverless概览](https://docs.runpod.io/serverless/overview)
- [Runpod Serverless入门](https://trapdoor.cloud/getting-started-with-runpod-serverless/)
- [runpod-python GitHub](https://github.com/runpod/runpod-python)
- [Runpod快速部署](https://docs.runpod.io/serverless/quick-deploys)
