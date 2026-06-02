---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-haiku
title: Docker CLI 常用命令快速指南
translated: true
type: note
---

Docker 通过 command-line interface 进行控制，其基本结构如下：

```
docker [GLOBAL OPTIONS] COMMAND [COMMAND OPTIONS] [ARGUMENTS]
```

## Global Options

这些选项适用于所有 Docker 命令：

- `--config string` - client 配置文件位置（默认：~/.docker）
- `--context string` - 要使用的 context 名称
- `--debug` - 启用 debug 模式
- `--host, -H string` - 连接到的 daemon socket
- `--log-level string` - 设置日志级别（debug, info, warn, error, fatal）
- `--version, -v` - 打印版本信息

如需获取任何命令的帮助，请使用 `docker COMMAND --help`。

## Container Commands

**docker run** 创建并启动一个 container。关键选项包括 `-d`（detach/后台运行）、`--name`（指定名称）、`-p`（发布端口）、`-v`（挂载 volumes）、`-e`（环境变量）、`-w`（working directory）、`--rm`（退出时自动删除）、`-it`（interactive terminal），以及资源限制如 `--memory` 和 `--cpus`。示例：`docker run -d --name web -p 8080:80 nginx`。

**docker ps** 列出 containers。使用 `-a` 显示所有（正在运行和已停止的），`-q` 仅显示 ID，`-s` 显示大小，`--filter` 根据状态或其他条件进行过滤。

**docker exec** 在运行中的 containers 中执行命令。使用 `-it` 进入交互模式：`docker exec -it container_name bash`。

**docker stop** 优雅地停止 containers，`-t` 可指定在强制杀死前的超时秒数。

**docker start** 重启已停止的 containers。

**docker rm** 删除 containers（使用 `-f` 强制删除正在运行的，`-v` 同时删除 volumes）。

**docker logs** 显示 container 输出。使用 `-f` 实时追踪日志，`--tail` 限制行数，`-t` 显示时间戳。

## Image Commands

**docker build** 从 Dockerfiles 创建 images。核心选项：`-t`（给 image 打标签）、`-f`（指定 Dockerfile 路径）、`--build-arg`（传递构建变量）、`--no-cache`（跳过缓存）、`--target`（构建特定阶段）。示例：`docker build -t myapp:1.0 .`。

**docker images** 列出本地 images。使用 `-a` 显示所有镜像（包括中间层），`-q` 仅显示 ID，`--filter` 过滤结果。

**docker pull** 从 registries 下载 images：`docker pull ubuntu:20.04`。

**docker push** 将 images 上传到 registries：`docker push myregistry.com/myapp:latest`。

**docker tag** 创建 image 别名或标签：`docker tag myapp:latest myregistry.com/myapp:v1.0`。

**docker rmi** 删除 images（使用 `-f` 强制删除）。

## Volume Commands

**docker volume create** 创建具名 volumes：`docker volume create mydata`。

**docker volume ls** 列出所有 volumes。

**docker volume inspect** 显示详细的 volume 信息。

**docker volume rm** 删除 volumes。

## Network Commands

**docker network create** 创建 networks，使用 `-d` 指定 driver 类型（bridge, host, overlay, macvlan）：`docker network create mynet`。

**docker network ls** 列出 networks。

**docker network inspect** 显示 network 详情。

**docker network rm** 删除 networks。

## System Commands

**docker info** 显示 Docker 系统级信息。

**docker version** 显示 Docker 版本详情。

**docker stats** 显示实时 container 资源占用情况（CPU、memory、network I/O）。

**docker system prune** 删除未使用的 images、containers 和 networks（使用 `-a` 包含悬空镜像，`-f` 跳过确认）。

**docker top** 显示 container 中运行的进程。

**docker inspect** 显示 containers 或 images 的详细 JSON 配置。

## Key Patterns and Tips

许多命令使用一致的语法：列表命令（`docker ps`, `docker images`）支持 `-q` 用于简洁输出和 `--filter` 用于过滤。删除命令（`docker rm`, `docker rmi`）使用 `-f` 强制执行。交互式命令接受 `-it` 进入 interactive terminal 模式。你可以向大多数命令传递多个参数：`docker stop container1 container2 container3`。

常见过滤示例：containers 使用 `--filter "status=exited"`，images 使用 `--filter "dangling=true"`，networks 使用 `--filter "driver=bridge"`。

端口发布 `-p` 使用 `HOST:CONTAINER` 格式（例如，`-p 8080:80` 将 host 端口 8080 映射到 container 端口 80）。Volume 挂载 `-v` 使用 `HOST:CONTAINER` 或 `VOLUME:CONTAINER` 语法。

请经常使用 `docker COMMAND --help` —— 这是查看任何命令所有可用选项的最快方式。
