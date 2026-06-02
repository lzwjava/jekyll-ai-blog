---
audio: false
generated: true
lang: en
layout: post
title: C Program to Decode a TCP Packet
translated: false
type: note
---

Decoding a TCP packet in C involves capturing raw network data (typically using raw sockets or a packet capture mechanism) and then parsing the headers step-by-step: the Ethernet header (if present), the IP header, and finally the TCP header. Since TCP runs over IP, you’ll need to extract the IP header first to locate the TCP segment within the packet. For simplicity, I’ll assume we’re working with IPv4 and a raw socket capturing IP packets (no Ethernet layer).

Here’s a C program that captures a TCP packet using a raw socket, decodes the IP header, and then decodes the TCP header to display key fields like source/destination ports, sequence number, acknowledgment number, flags, and window size.

---

### C Program to Decode a TCP Packet

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/ip.h>   // For struct iphdr
#include <netinet/tcp.h>  // For struct tcphdr

// Print TCP flags in human-readable form
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
    char buffer[65535]; // Max IP packet size
    struct sockaddr_in source_addr, dest_addr;

    // Create raw socket to capture TCP packets
    sock_fd = socket(AF_INET, SOCK_RAW, IPPROTO_TCP);
    if (sock_fd < 0) {
        perror("Socket creation failed (run as root?)");
        exit(EXIT_FAILURE);
    }

    printf("Listening for TCP packets...\n");

    while (1) {
        // Receive raw packet
        ssize_t bytes_received = recvfrom(sock_fd, buffer, sizeof(buffer), 0, NULL, NULL);
        if (bytes_received < 0) {
            perror("Receive failed");
            continue;
        }

        // IP header (struct iphdr) is at the start of the packet
        struct iphdr *ip = (struct iphdr *)buffer;
        int ip_header_len = ip->ihl * 4; // ihl is in 32-bit words, convert to bytes

        // Check if it's an IPv4 packet with TCP protocol
        if (ip->version == 4 && ip->protocol == IPPROTO_TCP) {
            // TCP header follows IP header
            struct tcphdr *tcp = (struct tcphdr *)(buffer + ip_header_len);

            // Extract source and destination IP addresses
            inet_ntop(AF_INET, &ip->saddr, (char *)&source_addr.sin_addr, sizeof(source_addr));
            inet_ntop(AF_INET, &ip->daddr, (char *)&dest_addr.sin_addr, sizeof(dest_addr));

            // Decode and print TCP packet details
            printf("\n--- TCP Packet ---\n");
            printf("Source IP: %s\n", inet_ntoa(*(struct in_addr *)&ip->saddr));
            printf("Dest IP: %s\n", inet_ntoa(*(struct in_addr *)&ip->daddr));
            printf("Source Port: %u\n", ntohs(tcp->source));
            printf("Dest Port: %u\n", ntohs(tcp->dest));
            printf("Sequence Number: %u\n", ntohl(tcp->seq));
            printf("Acknowledgment Number: %u\n", ntohl(tcp->ack_seq));
            printf("Data Offset: %d bytes\n", tcp->doff * 4); // TCP header length
            print_tcp_flags(tcp);
            printf("Window Size: %u\n", ntohs(tcp->window));
            printf("Checksum: 0x%04x\n", ntohs(tcp->check));
            printf("Urgent Pointer: %u\n", ntohs(tcp->urg_ptr));

            // Payload (data after TCP header)
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

    close(sock_fd); // Unreachable in this loop, but good practice
    return 0;
}
```

---

### How It Works

1. **Socket Setup**:
   - `socket(AF_INET, SOCK_RAW, IPPROTO_TCP)` creates a raw socket that captures all TCP packets destined for the host. This requires root privileges (`sudo`).

2. **Packet Capture**:
   - `recvfrom()` grabs the raw IP packet, which includes the IP header, TCP header, and payload.

3. **IP Header Parsing**:
   - `struct iphdr` defines the IPv4 header (from `<netinet/ip.h>`).
   - `ihl` (IP header length) is multiplied by 4 to get the byte offset, since it’s measured in 32-bit words.
   - Check `version == 4` and `protocol == IPPROTO_TCP` to ensure it’s an IPv4 TCP packet.

4. **TCP Header Parsing**:
   - `struct tcphdr` (from `<netinet/tcp.h>`) defines the TCP header, starting right after the IP header.
   - Key fields:
     - `source` and `dest`: Source and destination ports (converted from network to host byte order with `ntohs`).
     - `seq` and `ack_seq`: Sequence and acknowledgment numbers (`ntohl` for 32-bit conversion).
     - `doff`: Data offset (TCP header length in bytes, also multiplied by 4).
     - `syn`, `ack`, `fin`, etc.: Flags indicating packet type.
     - `window`: Receiver’s window size.
     - `check`: Checksum (not validated here for simplicity).
     - `urg_ptr`: Urgent pointer (used with URG flag).

5. **Payload Extraction**:
   - The payload starts after the TCP header. Its length is calculated as: `total bytes - IP header length - TCP header length`.
   - A snippet of the payload is printed in hex.

---

### Compilation and Usage

- Compile: `gcc tcp_decode.c -o tcp_decode`
- Run (as root): `sudo ./tcp_decode`
- Example output (when TCP traffic is present, e.g., browsing the web):

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

### Key Structures

- **IP Header (`struct iphdr`)**:

  ```c
  struct iphdr {
      unsigned int ihl:4;    // Header length (in 32-bit words)
      unsigned int version:4;// IP version (4 for IPv4)
      uint8_t tos;           // Type of service
      uint16_t tot_len;      // Total length
      uint16_t id;           // Identification
      uint16_t frag_off;     // Fragment offset
      uint8_t ttl;           // Time to live
      uint8_t protocol;      // Protocol (6 for TCP)
      uint16_t check;        // Checksum
      uint32_t saddr;        // Source address
      uint32_t daddr;        // Destination address
  };
  ```

- **TCP Header (`struct tcphdr`)**:

  ```c
  struct tcphdr {
      uint16_t source;       // Source port
      uint16_t dest;         // Destination port
      uint32_t seq;          // Sequence number
      uint32_t ack_seq;      // Acknowledgment number
      uint16_t doff:4;       // Data offset (header length in 32-bit words)
      uint16_t res1:4;       // Reserved
      uint16_t res2:2;       // Reserved
      uint16_t urg:1;        // Urgent flag
      uint16_t ack:1;        // Acknowledgment flag
      uint16_t psh:1;        // Push flag
      uint16_t rst:1;        // Reset flag
      uint16_t syn:1;        // Synchronize flag
      uint16_t fin:1;        // Finish flag
      uint16_t window;       // Window size
      uint16_t check;        // Checksum
      uint16_t urg_ptr;      // Urgent pointer
  };
  ```

---

### Notes

- **Root Privileges**: Raw sockets require `sudo` because they access the network stack directly.
- **Promiscuous Mode**: This captures only packets destined for the host. For all traffic (like Wireshark), you’d need `libpcap` or a different approach (e.g., `PF_PACKET` sockets with promiscuous mode).
- **Byte Order**: Network byte order (big-endian) is converted to host byte order using `ntohs` (16-bit) and `ntohl` (32-bit).
- **Limitations**: This doesn’t validate the checksum or handle fragmented packets.

Let me know if you want to refine this further (e.g., add checksum validation or filter specific ports)!
