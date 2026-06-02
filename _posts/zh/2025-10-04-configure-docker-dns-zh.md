---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 配置Docker守护进程DNS服务器
translated: true
type: note
---

要为 Docker 守护进程配置 DNS 服务器（容器将默认使用该配置，除非在容器级别被覆盖），您可以编辑 `/etc/docker/daemon.json` 文件。该文件允许您自定义 Docker 的运行时行为。

### 配置 DNS 的步骤

1. **编辑 daemon.json 文件**：
   - 如果文件不存在，请使用 root 权限创建（例如使用 `sudo nano /etc/docker/daemon.json` 或您偏好的编辑器）。
   - 添加或更新 `dns` 键，将其设置为 DNS 服务器的 IP 地址数组。例如，要使用 Google 的公共 DNS（8.8.8.8 和 8.8.4.4）：

     ```json
     {
       "dns": ["8.8.8.8", "8.8.4.4"]
     }
     ```

     - 如果需要，您可以添加更多服务器（例如 Cloudflare 的 1.1.1.1）。
     - 此设置适用于使用默认网络创建的所有容器，除非另有指定。

2. **验证 JSON**：
   - 确保文件是有效的 JSON。您可以使用 `jq` 等工具检查：`jq . /etc/docker/daemon.json`。如果报错，请修复语法。

3. **重启 Docker 服务**：
   - 通过重启 Docker 来应用更改：
     ```
     sudo systemctl restart docker
     ```
     - 在非 systemd 系统上（例如较旧的 Linux 发行版），使用 `sudo service docker restart`。
   - 验证状态：`sudo systemctl status docker`。

4. **测试配置**：
   - 运行一个测试容器并检查其 DNS 解析：
     ```
     docker run --rm busybox nslookup google.com
     ```
     - 它应该使用您配置的 DNS 服务器进行解析。

### 注意事项
- **作用范围**：此配置针对主机上的 Docker 守护进程，影响容器的出站名称解析。它不会更改主机的系统 DNS。
- **覆盖**：如果容器需要不同的 DNS（例如通过 `docker run` 中的 `--dns` 标志），它将覆盖此守护进程级别的设置。
- **安全性**：对于大多数情况，使用公共 DNS（如 8.8.8.8）是可以的，但在企业环境中请考虑使用内部 DNS。
- **文档**：有关更多选项（例如 DNS 搜索域），请参阅 [官方 Docker 文档中的 daemon.json 部分](https://docs.docker.com/engine/reference/commandline/dockerd/#daemon-configuration-file)。

如果您遇到错误（例如权限问题或 JSON 解析错误），请分享详细信息以便进一步排查。
