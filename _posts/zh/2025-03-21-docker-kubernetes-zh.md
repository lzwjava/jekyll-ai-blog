---
audio: false
generated: true
lang: zh
layout: post
title: Docker与Kubernetes对比
translated: true
type: note
---

Docker 和 Kubernetes 是容器生态系统中互补的技术，但它们的功能定位不同。让我们来解析它们的区别与关联。

---

### Docker：容器化平台
**功能**：Docker 是用于创建、运行和管理独立容器的工具——这种轻量级隔离环境将应用程序与其依赖项打包在一起。

#### 核心特性
1. **容器运行时**：
   - Docker 使用运行时（如 `containerd` 或 `runc`）基于 Linux 内核的命名空间和控制组功能来执行容器
   - 负责单个容器的生命周期管理：构建、启动、停止等

2. **镜像管理**：
   - 通过 `Dockerfile` 构建镜像，定义应用程序、库和配置
   - 镜像存储在注册中心（如 Docker Hub），并作为容器运行

3. **单机部署**：
   - Docker 擅长在单台机器上管理容器。虽然可以运行多个容器，但不具备跨多主机的原生编排能力

4. **命令行驱动**：
   - 通过 `docker build`、`docker run`、`docker ps` 等命令直接操作容器

#### 应用场景
- 在本地或服务器上运行单个 Spring Boot 应用：
  ```bash
  docker run -p 8080:8080 myapp:latest
  ```

#### 局限性
- 缺乏原生多主机支持
- 没有自动扩缩容、自愈或负载均衡功能
- 手动管理大量容器时会变得混乱

---

### Kubernetes：容器编排系统
**功能**：Kubernetes（常简称为 K8s）是在机器集群中管理和编排多容器的平台，可自动化容器化应用的部署、扩缩容和运维。

#### 核心特性
1. **集群管理**：
   - 在节点集群（物理机或虚拟机）上运行，包含“控制平面”（管理集群）和“工作节点”（运行容器）

2. **编排功能**：
   - **调度**：根据资源和约束条件决定容器运行位置
   - **扩缩容**：自动调整容器实例数量（如基于 CPU 使用率）
   - **自愈能力**：重启故障容器，在节点失效时重新调度，确保维持期望状态
   - **负载均衡**：在多个容器实例间分配流量

3. **抽象层**：
   - 以“Pod”为最小单位——每个 Pod 可包含一个或多个共享存储和网络资源的容器（通常为一个）
   - 通过声明式 YAML 文件进行管理（如定义部署、服务）

4. **多主机架构**：
   - 专为分布式系统设计，可跨多台机器协调容器

5. **生态系统**：
   - 包含服务发现、持久化存储、密钥管理和滚动更新等功能

#### 应用场景
- 部署包含 10 个服务的微服务应用，每个服务运行在独立容器中，跨 5 台服务器，具备自动扩缩容和故障转移能力：
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: myapp
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: myapp
    template:
      metadata:
        labels:
          app: myapp
      spec:
        containers:
        - name: myapp
          image: myapp:latest
          ports:
          - containerPort: 8080
  ```

#### 局限性
- 学习曲线较陡峭
- 对于单机简单应用属于过度设计

---

### 核心差异对比

| 维度                | Docker                              | Kubernetes                          |
|---------------------|-------------------------------------|-------------------------------------|
| **定位**            | 容器创建与运行时                    | 容器编排                            |
| **范围**            | 单机环境                            | 多主机集群                          |
| **单元**            | 容器                                | Pod（容器组）                       |
| **扩缩容**          | 手动（如多次执行 `docker run`）     | 自动（通过副本数配置）              |
| **网络**            | 基础网络（桥接/主机/覆盖）          | 高级网络（服务/入口）               |
| **自愈能力**        | 无（需手动重启）                    | 内置（自动重启/重新调度）           |
| **管理方式**        | CLI 或 Docker Compose（小型场景）   | YAML 配置与 `kubectl` CLI          |
| **依赖关系**        | 独立运行（需 Docker 引擎）          | 需容器运行时（如 Docker）           |

---

### 协作方式
- **Docker 作为运行时**：Kubernetes 不直接运行容器，需依赖 Docker（或 `containerd` 等替代方案）在 Pod 内启动和管理单个容器
- **工作流程**：
  1. 构建 Docker 镜像（`docker build -t myapp:latest .`）
  2. 推送至注册中心（`docker push myapp:latest`）
  3. Kubernetes 根据 YAML 配置拉取镜像并部署到集群（`kubectl apply -f deployment.yaml`）

- **示例**：Kubernetes 可能使用 Docker 在不同节点上运行三个 `myapp:latest` 实例，并通过负载均衡服务暴露这些实例

---

### 形象类比
- **Docker**：在厨房烹饪单道菜肴的厨师。您告知厨师烹饪内容（`Dockerfile`）和上菜方式（`docker run`）
- **Kubernetes**：管理多个厨房（节点）中众多厨师（Docker 实例）的餐厅经理。经理确保准时出餐，高峰时段增派人手，并在厨师生病时及时替换

---

### 适用场景
- **单独使用 Docker**：适用于开发测试环境或单机简单应用（如单个 Spring Boot 应用）
- **Kubernetes**：适用于需要高可用、弹性扩缩容和故障恢复的生产级分布式应用（如微服务架构）

---

这样的解释是否更清晰？如果您想深入了解特定方面——例如搭建 Kubernetes 或与 Docker Compose 的对比，请随时告诉我！
