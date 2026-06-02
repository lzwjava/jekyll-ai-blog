---
audio: false
generated: true
lang: zh
layout: post
title: C程序解码TCP数据包
translated: true
type: note
---

在 C 语言中解码 TCP 数据包涉及捕获原始网络数据（通常使用原始套接字或数据包捕获机制），然后逐步解析头部：以太网头部（如果存在）、IP 头部，最后是 TCP 头部。由于 TCP 运行在 IP 之上，您需要先提取 IP 头部以定位数据包中的 TCP 段。为简化起见，我假设我们正在处理 IPv4 和捕获 IP 数据包的原始套接字（无以太网层）。

以下是一个 C 程序，使用原始套接字捕获 TCP 数据包，解码 IP 头部，然后解码 TCP 头部以显示关键字段，如源/目标端口、序列号、确认号、标志和窗口大小。

---

### 用于解码 TCP 数据包的 C 程序

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/ip.h>   // 用于 struct iphdr
#include <netinet/tcp.h>  // 用于 struct tcphdr

// 以人类可读形式打印 TCP 标志
void print_tcp_flags(struct tcphdr *tcp) {
    printf("Flags: ");
    if (tcp->syn) printf("SYN ");
    if (tcp->ack) printf("ACK ");
    if (tcp->fin) printf("FIN ");
    if (tcp->rst) printf("RST ");
    if (tcp->psh) printf("PSH ");
    if (tcp->urg) printf("URG ");
    printf("\n");
}

int main() {
    int sock_fd;
    char buffer[65535]; // 最大 IP 数据包大小
    struct sockaddr_in source_addr, dest_addr;

    // 创建原始套接字以捕获 TCP 数据包
    sock_fd = socket(AF_INET, SOCK_RAW, IPPROTO_TCP);
    if (sock_fd < 0) {
        perror("Socket creation failed (run as root?)");
        exit(EXIT_FAILURE);
    }

    printf("Listening for TCP packets...\n");

    while (1) {
        // 接收原始数据包
        ssize_t bytes_received = recvfrom(sock_fd, buffer, sizeof(buffer), 0, NULL, NULL);
        if (bytes_received < 0) {
            perror("Receive failed");
            continue;
        }

        // IP 头部 (struct iphdr) 位于数据包起始位置
        struct iphdr *ip = (struct iphdr *)buffer;
        int ip_header_len = ip->ihl * 4; // ihl 以 32 位字为单位，转换为字节

        // 检查是否为 IPv4 数据包且协议为 TCP
        if (ip->version == 4 && ip->protocol == IPPROTO_TCP) {
            // TCP 头部紧随 IP 头部之后
            struct tcphdr *tcp = (struct tcphdr *)(buffer + ip_header_len);

            // 提取源和目标 IP 地址
            inet_ntop(AF_INET, &ip->saddr, (char *)&source_addr.sin_addr, sizeof(source_addr));
            inet_ntop(AF_INET, &ip->daddr, (char *)&dest_addr.sin_addr, sizeof(dest_addr));

            // 解码并打印 TCP 数据包详情
            printf("\n--- TCP Packet ---\n");
            printf("Source IP: %s\n", inet_ntoa(*(struct in_addr *)&ip->saddr));
            printf("Dest IP: %s\n", inet_ntoa(*(struct in_addr *)&ip->daddr));
            printf("Source Port: %u\n", ntohs(tcp->source));
            printf("Dest Port: %u\n", ntohs(tcp->dest));
            printf("Sequence Number: %u\n", ntohl(tcp->seq));
            printf("Acknowledgment Number: %u\n", ntohl(tcp->ack_seq));
            printf("Data Offset: %d bytes\n", tcp->doff * 4); // TCP 头部长度
            print_tcp_flags(tcp);
            printf("Window Size: %u\n", ntohs(tcp->window));
            printf("Checksum: 0x%04x\n", ntohs(tcp->check));
            printf("Urgent Pointer: %u\n", ntohs(tcp->urg_ptr));

            // 载荷（TCP 头部之后的数据）
            int tcp_header_len = tcp->doff * 4;
            int payload_len = bytes_received - ip_header_len - tcp_header_len;
            if (payload_len > 0) {
                printf("Payload Length: %d bytes\n", payload_len);
                printf("Payload (first 16 bytes): ");
                unsigned char *payload = (unsigned char *)(buffer + ip_header_len + tcp_header_len);
                for (int i = 0; i < payload_len && i < 16; i++) {
                    printf("%02x ", payload[i]);
                }
                printf("\n");
            } else {
                printf("No payload\n");
            }
        }
    }

    close(sock_fd); // 在此循环中无法到达，但出于良好实践
    return 0;
}
```

---

### 工作原理

1. **套接字设置**：
   - `socket(AF_INET, SOCK_RAW, IPPROTO_TCP)` 创建一个原始套接字，捕获所有发送到主机的 TCP 数据包。这需要 root 权限（`sudo`）。

2. **数据包捕获**：
   - `recvfrom()` 获取原始 IP 数据包，包括 IP 头部、TCP 头部和载荷。

3. **IP 头部解析**：
   - `struct iphdr` 定义 IPv4 头部（来自 `<netinet/ip.h>`）。
   - `ihl`（IP 头部长度）乘以 4 得到字节偏移量，因为它以 32 位字为单位。
   - 检查 `version == 4` 和 `protocol == IPPROTO_TCP` 以确保是 IPv4 TCP 数据包。

4. **TCP 头部解析**：
   - `struct tcphdr`（来自 `<netinet/tcp.h>`）定义 TCP 头部，紧接在 IP 头部之后。
   - 关键字段：
     - `source` 和 `dest`：源端口和目标端口（使用 `ntohs` 从网络字节序转换为主机字节序）。
     - `seq` 和 `ack_seq`：序列号和确认号（使用 `ntohl` 进行 32 位转换）。
     - `doff`：数据偏移量（TCP 头部长度，以字节为单位，同样乘以 4）。
     - `syn`、`ack`、`fin` 等：指示数据包类型的标志。
     - `window`：接收方窗口大小。
     - `check`：校验和（为简化起见，此处未验证）。
     - `urg_ptr`：紧急指针（与 URG 标志一起使用）。

5. **载荷提取**：
   - 载荷从 TCP 头部之后开始。其长度计算为：`总字节数 - IP 头部长度 - TCP 头部长度`。
   - 载荷的前 16 字节以十六进制形式打印。

---

### 编译与使用
- 编译：`gcc tcp_decode.c -o tcp_decode`
- 运行（需 root 权限）：`sudo ./tcp_decode`
- 示例输出（当存在 TCP 流量时，例如浏览网页）：
  ```
  Listening for TCP packets...

  --- TCP Packet ---
  Source IP: 192.168.1.100
  Dest IP: 93.184.216.34
  Source Port: 54321
  Dest Port: 80
  Sequence Number: 123456789
  Acknowledgment Number: 987654321
  Data Offset: 20 bytes
  Flags: SYN
  Window Size: 64240
  Checksum: 0x1a2b
  Urgent Pointer: 0
  No payload
  ```

---

### 关键结构
- **IP 头部 (`struct iphdr`)**：
  ```c
  struct iphdr {
      unsigned int ihl:4;    // 头部长度（以 32 位字为单位）
      unsigned int version:4;// IP 版本（4 表示 IPv4）
      uint8_t tos;           // 服务类型
      uint16_t tot_len;      // 总长度
      uint16_t id;           // 标识符
      uint16_t frag_off;     // 分片偏移
      uint8_t ttl;           // 生存时间
      uint8_t protocol;      // 协议（6 表示 TCP）
      uint16_t check;        // 校验和
      uint32_t saddr;        // 源地址
      uint32_t daddr;        // 目标地址
  };
  ```

- **TCP 头部 (`struct tcphdr`)**：
  ```c
  struct tcphdr {
      uint16_t source;       // 源端口
      uint16_t dest;         // 目标端口
      uint32_t seq;          // 序列号
      uint32_t ack_seq;      // 确认号
      uint16_t doff:4;       // 数据偏移（头部长度，以 32 位字为单位）
      uint16_t res1:4;       // 保留
      uint16_t res2:2;       // 保留
      uint16_t urg:1;        // 紧急标志
      uint16_t ack:1;        // 确认标志
      uint16_t psh:1;        // 推送标志
      uint16_t rst:1;        // 重置标志
      uint16_t syn:1;        // 同步标志
      uint16_t fin:1;        // 结束标志
      uint16_t window;       // 窗口大小
      uint16_t check;        // 校验和
      uint16_t urg_ptr;      // 紧急指针
  };
  ```

---

### 注意事项
- **Root 权限**：原始套接字需要 `sudo`，因为它们直接访问网络栈。
- **混杂模式**：此程序仅捕获发送到主机的数据包。要捕获所有流量（如 Wireshark），您需要 `libpcap` 或不同的方法（例如，带有混杂模式的 `PF_PACKET` 套接字）。
- **字节序**：使用 `ntohs`（16 位）和 `ntohl`（32 位）将网络字节序（大端序）转换为主机字节序。
- **局限性**：此程序不验证校验和，也不处理分片数据包。

如果您希望进一步改进（例如，添加校验和验证或过滤特定端口），请告诉我！
