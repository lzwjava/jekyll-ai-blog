---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Docker与DockerCompose的区别
translated: true
type: note
---

### Docker 与 Docker Compose：核心差异

Docker 和 Docker Compose 虽然相关，但在容器化工作流中承担着不同的职责。Docker 是基础技术，而 Docker Compose 在其之上构建，用于处理更复杂的场景。

#### 什么是 Docker？
Docker 是一个用于在轻量级、可移植的 **容器 ** 内开发、交付和运行应用程序的平台。这些容器将应用程序及其所有依赖项（代码、运行时环境、库等）打包在一起，确保其在开发、测试和生产等不同环境中能够稳定运行。您主要通过命令行界面（CLI）与 Docker 交互，使用诸如 `docker run`、`docker build` 和 `docker ps` 等命令来管理单个容器。

#### 什么是 Docker Compose？
Docker Compose 是一个编排工具，它扩展了 Docker 的功能以处理 **多容器应用程序**。它使用一个简单的 YAML 文件（通常是 `docker-compose.yml`）来定义您的整个应用栈——包括多个服务、网络、数据卷和环境变量。您无需再费力地处理几十个 `docker run` 命令，只需一个 `docker-compose up` 命令即可启动所有服务。

#### 主要区别
以下是一个快速对比：

| 对比维度           | Docker                                | Docker Compose                            |
|--------------------|---------------------------------------|-------------------------------------------|
| **主要关注点**     | 构建、运行和管理 **单个容器**         | 定义和编排 **多容器应用**                 |
| **配置方式**       | 内联的 CLI 参数（如 `docker run -p 80:80 image`） | 使用 YAML 文件进行声明式设置（服务、端口、数据卷等） |
| **常用命令**       | `docker run`, `docker build` 等       | `docker-compose up`, `down`, `scale` 等   |
| **适用范围**       | 底层的容器生命周期管理                | 高层的应用栈（例如：应用 + 数据库 + 缓存） |
| **网络/依赖管理**  | 需要为每个容器手动设置                | 自动管理（例如，服务可以通过名称相互引用） |
| **典型用例**       | 简单、隔离的服务                      | 复杂的应用，如带有数据库的 Web 服务器     |

简而言之：Docker 像是执行单一任务的单引擎车辆，而 Docker Compose 则是协调多辆车辆完成一段旅程的车队经理。

### 为什么我们需要 Docker Compose？

虽然 Docker 本身对于单容器应用已经足够强大，但现实世界的应用程序通常涉及多个相互关联的组件（例如，前端、后端 API、数据库和 Redis 缓存）。以下是 Docker Compose 至关重要的原因：

- **简化多容器管理**：没有它，您需要手动启动/停止容器、配置网络并通过重复的 CLI 命令处理依赖关系——这很容易变得混乱且容易出错。Compose 通过一个文件和一个命令自动化了这些过程。

- **可重现性与协作**：YAML 文件充当了蓝图。团队成员可以通过 `docker-compose up` 启动完全相同的环境，这使得开发过程保持一致且可移植（非常适合 CI/CD 流水线）。

- **提高开发效率**：诸如服务链接（例如，您的应用通过主机名自动连接到数据库）和为实时代码重载而挂载数据卷等功能，可以加速开发迭代。您还可以在不重新构建镜像的情况下扩展服务（例如，`docker-compose scale web=3`）。

- **环境隔离**：它为每个项目创建独立的网络和数据卷，从而避免在本地运行多个应用时产生冲突。

本质上，Docker Compose 将 Docker 从一个单打独斗的工具转变为一个适用于现代基于微服务架构的团队协作者。如果您是初学者，可以尝试为一个 WordPress + MySQL 的简单技术栈编写一个 `docker-compose.yml` 文件来体验其魔力。

#### 参考资料
- [Docker vs. Docker Compose: Simple and Fun Explanation](https://medium.com/@ShantKhayalian/docker-vs-docker-compose-simple-and-fun-explanation-4811582127f7)
- [What is the difference between docker and docker-compose](https://stackoverflow.com/questions/37966552/what-is-the-difference-between-docker-and-docker-compose)
- [How To Choose Between Docker Compose vs Docker?](https://cyberpanel.net/blog/docker-compose-vs-docker)
- [Docker Compose - What is It, Example & Tutorial](https://spacelift.io/blog/docker-compose)
