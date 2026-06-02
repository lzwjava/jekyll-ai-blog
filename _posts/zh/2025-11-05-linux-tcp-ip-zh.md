---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Linux C语言TCP/IP编程
translated: true
type: note
---

### Linux 中的 TCP/IP 协议：概述及在 C 语言中的使用

在 Linux 系统中，TCP（传输控制协议）和 IP（网际协议）是作为 Linux TCP/IP 协议栈的核心网络协议**在内核中实现**的。该协议栈处理诸如数据包路由、拥塞控制和连接管理等底层细节。用户空间应用程序（例如你的 C 程序）通过 **Berkeley 套接字 API**（也称为 POSIX 套接字）与此协议栈交互，该 API 提供了一种标准化的创建网络连接的方式。

你无需自己实现 TCP/IP——内核已经完成了这项工作。相反，你使用套接字 API 来与内核"对话"。该 API **内置于 Linux 的标准 C 库（glibc）** 中，因此无需安装或链接单独的"TCP/IP 库"。所有功能都由 `libc`（GNU C 库）提供。

#### 关键库和头文件

- **主库**：`libc`（glibc）。所有套接字函数都包含在此库中。隐式链接此库（使用 `gcc` 时通常是自动的）。
  - 位置：通常为 `/lib/x86_64-linux-gnu/libc.so.6`（或类似路径，具体取决于你的体系结构和发行版）。你可以使用 `ldd /bin/ls` 或 `locate libc.so` 查找它。
- **头文件**（用于声明）：这些是 Linux 开发头文件的一部分。
  - `<sys/socket.h>`：核心套接字函数（例如 `socket()`、`bind()`、`connect()`）。
  - `<netinet/in.h>`：网络地址结构（例如用于 IPv4 的 `struct sockaddr_in`）。
  - `<arpa/inet.h>`：地址转换函数（例如 `inet_addr()`）。
  - `<sys/types.h>`：基本类型（通常被间接包含）。
  - 位置：通常是 `/usr/include/`（例如 `/usr/include/sys/socket.h`）。如果缺少开发头文件，请安装它们（例如，在基于 Debian 的系统上使用 `sudo apt install libc6-dev`）。

在 Linux 上不需要像 `-lsocket` 这样的额外标志（这与一些旧的 Unix 系统不同）。只需使用 `gcc your_program.c -o your_program` 编译即可。

#### 基础示例：C 语言中的简单 TCP 客户端

这是一个连接到服务器（例如 example.com 的 80 端口）的最小 TCP 客户端。它演示了套接字 API 的使用。

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>  // 用于 close()

int main() {
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);  // 创建 TCP 套接字 (AF_INET 用于 IPv4, SOCK_STREAM 用于 TCP)
    if (sockfd < 0) {
        perror("socket");
        return 1;
    }

    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(80);  // 主机字节序到网络字节序
    inet_pton(AF_INET, "93.184.216.34", &server_addr.sin_addr);  // example.com 的 IP 地址

    if (connect(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("connect");
        close(sockfd);
        return 1;
    }

    const char* msg = "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n";
    send(sockfd, msg, strlen(msg), 0);

    char buffer[1024];
    int bytes = recv(sockfd, buffer, sizeof(buffer) - 1, 0);
    buffer[bytes] = '\0';
    printf("Response: %s\n", buffer);

    close(sockfd);
    return 0;
}
```

- 编译：`gcc -o tcp_client tcp_client.c`
- 运行：`./tcp_client`

对于服务器，你将使用 `bind()`、`listen()` 和 `accept()` 而不是 `connect()`。

#### 延伸学习

- **手册页**：在你的 Linux 系统上运行 `man socket` 或 `man 7 ip` 以获取详细文档。
- **内核侧**：如果你指的是内核级实现，请查看 `/usr/src/linux/net/ipv4/`（TCP）或 `/usr/src/linux/net/ipv6/`（IPv6）中的源代码。使用 `sudo apt install linux-headers-$(uname -r)` 安装内核头文件。
- 资源：
  - [C 语言套接字编程 (GeeksforGeeks)](https://www.geeksforgeeks.org/c/socket-programming-cc/)
  - [使用 TCP/IP 进行 Linux 套接字编程 (IBM Developer)](https://developer.ibm.com/tutorials/l-sock/)

如果这不是你想要的（例如，内核模块或其他内容），请提供更多细节！
