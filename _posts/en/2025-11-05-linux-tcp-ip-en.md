---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Linux TCP/IP Programming in C
translated: false
type: note
---

### TCP/IP Protocols in Linux: Overview and Using Them in C

In Linux, the TCP (Transmission Control Protocol) and IP (Internet Protocol) are core networking protocols implemented **in the kernel** as part of the Linux TCP/IP stack. This stack handles low-level details like packet routing, congestion control, and connection management. User-space applications (e.g., your C programs) interact with this stack via the **Berkeley sockets API** (also known as POSIX sockets), which provides a standardized way to create network connections.

You don't need to implement TCP/IP yourself— the kernel does that. Instead, you use the sockets API to "talk" to the kernel. This API is **built into the standard C library (glibc)** on Linux, so there's no separate "TCP/IP library" to install or link against. Everything is provided by `libc` (GNU C Library).

#### Key Libraries and Headers
- **Main Library**: `libc` (glibc). All socket functions are included here. Link your program with it implicitly (it's usually automatic with `gcc`).
  - Location: Typically `/lib/x86_64-linux-gnu/libc.so.6` (or similar, depending on your architecture and distro). You can find it with `ldd /bin/ls` or `locate libc.so`.
- **Headers** (for declarations): These are part of the Linux development headers.
  - `<sys/socket.h>`: Core socket functions (e.g., `socket()`, `bind()`, `connect()`).
  - `<netinet/in.h>`: Internet address structures (e.g., `struct sockaddr_in` for IPv4).
  - `<arpa/inet.h>`: Address conversion functions (e.g., `inet_addr()`).
  - `<sys/types.h>`: Basic types (often included indirectly).
  - Location: Usually `/usr/include/` (e.g., `/usr/include/sys/socket.h`). Install development headers if missing (e.g., `sudo apt install libc6-dev` on Debian-based systems).

No extra flags like `-lsocket` are needed on Linux (unlike some older Unix systems). Just compile with `gcc your_program.c -o your_program`.

#### Basic Example: Simple TCP Client in C
Here's a minimal TCP client that connects to a server (e.g., port 80 on example.com). This demonstrates using the sockets API.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>  // For close()

int main() {
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);  // Create TCP socket (AF_INET for IPv4, SOCK_STREAM for TCP)
    if (sockfd < 0) {
        perror("socket");
        return 1;
    }

    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(80);  // Host-to-network byte order
    inet_pton(AF_INET, "93.184.216.34", &server_addr.sin_addr);  // IP for example.com

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

- Compile: `gcc -o tcp_client tcp_client.c`
- Run: `./tcp_client`

For a server, you'd use `bind()`, `listen()`, and `accept()` instead of `connect()`.

#### Where to Learn More
- **Man Pages**: Run `man socket` or `man 7 ip` on your Linux system for detailed docs.
- **Kernel Side**: If you meant kernel-level implementation, check the source in `/usr/src/linux/net/ipv4/` (TCP) or `/usr/src/linux/net/ipv6/` (for IPv6). Install kernel headers with `sudo apt install linux-headers-$(uname -r)`.
- Resources:
  - [Socket Programming in C (GeeksforGeeks)](https://www.geeksforgeeks.org/c/socket-programming-cc/)
  - [Programming Linux Sockets with TCP/IP (IBM Developer)](https://developer.ibm.com/tutorials/l-sock/)

If this isn't what you meant (e.g., kernel modules or something else), provide more details!
