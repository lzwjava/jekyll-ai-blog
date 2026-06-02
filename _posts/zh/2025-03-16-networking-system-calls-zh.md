---
audio: false
generated: true
lang: zh
layout: post
title: 网络系统调用
translated: true
type: note
---

在 Linux/Unix 这类操作系统中，网络编程最底层的系统调用源自伯克利套接字 API（通常简称为“套接字”）。这些系统调用直接与内核的网络协议栈交互。建立 TCP 连接最基础的系统调用包括：

1. **`socket()`** - 创建新套接字
2. **`bind()`** - 为套接字分配地址（客户端可选）
3. **`connect()`** - 初始化与远程服务器的连接（客户端）
4. **`listen()`** - 将套接字标记为可接受连接（服务端）
5. **`accept()`** - 接受传入连接（服务端）
6. **`send()` / `recv()`** - 通过连接发送/接收数据
7. **`close()`** - 关闭套接字

这些是在任何高级库（如 `libcurl`）或框架之下最底层的原始系统调用。以下是通过 C 语言展示 TCP 客户端与服务端建立连接的简单示例：

---

### TCP 服务端示例

此代码创建在 8080 端口监听连接的服务端，接受连接后发送消息。

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

int main() {
    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    char *message = "Hello from server!\n";

    // 创建套接字
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == -1) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // 配置服务端地址结构
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY; // 绑定任意地址
    server_addr.sin_port = htons(8080);       // 8080 端口

    // 绑定套接字
    if (bind(server_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    // 监听连接
    if (listen(server_fd, 3) < 0) { // 允许最多 3 个排队连接
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }
    printf("Server listening on port 8080...\n");

    // 接受传入连接
    client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
    if (client_fd < 0) {
        perror("Accept failed");
        exit(EXIT_FAILURE);
    }
    printf("Connection accepted\n");

    // 向客户端发送消息
    send(client_fd, message, strlen(message), 0);

    // 清理资源
    close(client_fd);
    close(server_fd);
    return 0;
}
```

---

### TCP 客户端示例

此代码连接至 `127.0.0.1:8080` 的服务端并读取消息。

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

int main() {
    int sock_fd;
    struct sockaddr_in server_addr;
    char buffer[1024] = {0};

    // 创建套接字
    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd == -1) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // 配置服务端地址结构
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(8080);              // 8080 端口
    inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr); // 本地主机

    // 连接服务端
    if (connect(sock_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Connection failed");
        exit(EXIT_FAILURE);
    }
    printf("Connected to server\n");

    // 接收服务端消息
    recv(sock_fd, buffer, sizeof(buffer), 0);
    printf("Server message: %s", buffer);

    // 清理资源
    close(sock_fd);
    return 0;
}
```

---

### 关键系统调用解析

- **`socket(AF_INET, SOCK_STREAM, 0)`**：创建 TCP 套接字（`AF_INET` 表示 IPv4，`SOCK_STREAM` 表示 TCP）
- **`bind()`**：将套接字与本地地址和端口关联（服务端）
- **`listen()`**：将套接字设置为接受连接状态（服务端）
- **`accept()`**：阻塞直到客户端连接，返回用于通信的新套接字
- **`connect()`**：与服务端发起 TCP 三次握手（客户端）
- **`send()` / `recv()`**：通过已建立连接进行数据传输
- **`close()`**：终止套接字

这些是用户空间能接触到的底层 TCP 网络编程接口。在此之下需要涉及内核内部机制（如 TCP/IP 协议栈本身），若不编写内核代码则无法直接通过系统调用访问。

编译运行步骤：

1. 将服务端代码保存为 `server.c`，客户端代码保存为 `client.c`
2. 编译：`gcc server.c -o server` 与 `gcc client.c -o client`
3. 先运行服务端：`./server`
4. 在另一个终端运行客户端：`./client`

如需更多细节或深入探讨，欢迎随时提问！
