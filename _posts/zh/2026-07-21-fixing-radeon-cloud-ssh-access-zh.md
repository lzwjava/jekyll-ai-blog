---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Radeon Cloud SSH访问
translated: true
type: note
---

**问题：为什么切换到 Jupyter 镜像并安装 SSH 服务器解决了 Radeon Cloud 上的访问问题？**

答案：

是的，你的理解基本正确。在 [Radeon Cloud](https://radeon-global.anruicloud.com/?tab=notebook&utm_source=chatgpt.com) 上，不同的容器镜像不仅仅是不同的软件包——它们定义了整个运行时环境。

流程大致如下：

```
Radeon Cloud
      |
      v
GPU VM / container
      |
      +-- 所选镜像
              |
              +-- JupyterLab？
              +-- SSH 服务器？
              +-- vLLM？
              +-- 模型文件？
              +-- 工具？
```

vLLM 镜像针对**服务模型**进行了优化，不一定是交互式开发。它可能启动：

```
vllm serve ...
```

但不包含：

```
jupyter lab
sshd
terminal UI
```

Jupyter 镜像更像一个开发工作站：

```
JupyterLab
 ├── Notebook
 ├── Terminal
 ├── Python 环境
 ├── ROCm 工具
 └── SSH（如果安装）
```

Radeon Cloud 的示例也使用 Jupyter 作为 vLLM 实验的入口：例如，他们的 Hermes + vLLM 工作坊指导用户打开 Jupyter 终端并在其中启动 vLLM 服务器。（[Radeon Cloud][1]）

所以你的解决方法：

```
切换镜像 -> Jupyter notebook
        |
        v
apt install openssh-server
        |
        v
ssh 进入 GPU 机器
```

是一个正常的云工作流程。

典型的设置：

```bash
sudo apt update
sudo apt install -y openssh-server

sudo mkdir -p /run/sshd

sudo service ssh start

ss -tlnp | grep :22
```

然后从你的笔记本电脑：

```bash
ssh user@<gpu-instance-ip>
```

SSH 成功后，你可以运行：

```bash
tmux new -s vllm

vllm serve \
  Qwen/Qwen3-8B \
  --host 0.0.0.0 \
  --port 8000
```

架构变为：

```
笔记本电脑
  |
  | ssh
  v
Radeon Cloud GPU 实例
  |
  +-- tmux
        |
        +-- vLLM 服务器 :8000
        |
        +-- ROCm
        |
        +-- AMD GPU
```

对于黑客马拉松工作，我通常会选择：

* **Jupyter/基础镜像** → 探索、编码、调试、SSH、代理
* **vLLM 镜像** → 最终推理部署/演示

因为在开发过程中，你访问 shell 的频率远高于预配置的推理服务器。Radeon Cloud 提供了笔记本风格的环境和面向 vLLM 的模板。（[Radeon Cloud][2]）

需要注意的一点是：安装 SSH 后，确保容器保持进程存活。某些云容器在主进程退出时会重启。将 `sshd` 放在平台预期的启动机制下运行比手动启动更安全。

[1]: https://radeon.anruicloud.com/templates/320/preview?utm_source=chatgpt.com "Notebook Preview - Radeon Cloud"
[2]: https://radeon.anruicloud.com/?utm_source=chatgpt.com "Radeon Cloud"