---
audio: false
generated: true
lang: zh
layout: post
title: C语言实现UDP数据包解码
translated: true
type: note
---

以下是一个在 C 语言中解码 UDP 数据包的示例。这段代码演示了如何接收 UDP 数据包并提取其关键组成部分：

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>

// UDP 头部结构
struct udp_header {
    uint16_t source_port;      // 源端口
    uint16_t dest_port;       // 目标端口
    uint16_t length;          // UDP 数据包长度（头部 + 数据）
    uint16_t checksum;        // 校验和
};

void decode_udp_packet(unsigned char* buffer, int size) {
    // 假设 IP 头部为 20 字节（无选项）
    struct udp_header* udp = (struct udp_header*)(buffer + 20);

    printf("\nUDP 头部\n");
    printf("源端口: %u\n", ntohs(udp->source_port));
    printf("目标端口: %u\n", ntohs(udp->dest_port));
    printf("长度: %u\n", ntohs(udp->length));
    printf("校验和: 0x%04x\n", ntohs(udp->checksum));

    // 计算数据长度和指针
    int udp_header_size = 8;  // UDP 头部固定为 8 字节
    int data_length = ntohs(udp->length) - udp_header_size;
    unsigned char* data = buffer + 20 + udp_header_size;

    printf("数据: ");
    for(int i = 0; i < data_length && i < 20; i++) {  // 最多显示前 20 字节
        printf("%02x ", data[i]);
    }
    printf("\n");
}

int main() {
    int sockfd;
    struct sockaddr_in server_addr, client_addr;
    unsigned char buffer[65535];  // UDP 数据包最大尺寸

    // 创建 UDP 套接字
    sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sockfd < 0) {
        perror("套接字创建失败");
        return 1;
    }

    // 初始化服务器地址
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(12345);  // 示例端口

    // 绑定套接字
    if (bind(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("绑定失败");
        close(sockfd);
        return 1;
    }

    printf("正在监听 12345 端口的 UDP 数据包...\n");

    while (1) {
        socklen_t client_len = sizeof(client_addr);
        int received_bytes = recvfrom(sockfd, buffer, sizeof(buffer), 0,
                                    (struct sockaddr*)&client_addr, &client_len);

        if (received_bytes < 0) {
            perror("接收失败");
            continue;
        }

        decode_udp_packet(buffer, received_bytes);
    }

    close(sockfd);
    return 0;
}
```

这段代码实现了以下功能：

1. 定义了与 UDP 数据包头部格式匹配的 `udp_header` 结构：
   - 源端口（16 位）
   - 目标端口（16 位）
   - 长度（16 位）
   - 校验和（16 位）

2. 创建 UDP 套接字并绑定到 12345 端口（可修改此端口号）。

3. `decode_udp_packet` 函数：
   - 接收原始数据包缓冲区作为输入
   - 假设 UDP 头部前有 20 字节的 IP 头部（注意：如果存在 IP 选项，此长度可能变化）
   - 使用 `ntohs` 将头部字段从网络字节序（大端序）转换为主机字节序
   - 打印头部信息
   - 提取并显示载荷数据

编译和运行方法：
```bash
gcc udp_decoder.c -o udp_decoder
sudo ./udp_decoder  # 因使用原始套接字需要 sudo 权限
```

重要说明：
1. 这是一个基础示例 - 实际应用可能需要：
   - 数据包大小的错误检查
   - IP 头部选项的处理（可变长度）
   - 校验和验证
   - 更复杂的数据处理

2. 测试方法：
   - 使用 netcat 发送 UDP 数据包：`echo "test" | nc -u 127.0.0.1 12345`
   - 使用数据包生成工具

3. 代码假设数据包包含 IP 头部。如果处理原始 UDP 数据，请移除 +20 的偏移量。

4. 生产环境中，建议添加更多错误处理，并考虑使用 `<netinet/udp.h>` 中的 `struct udphdr` 替代自定义结构体。

是否需要我详细解释任何特定部分，或展示此代码的变体？
