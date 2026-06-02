---
audio: false
generated: true
lang: en
layout: post
title: C Program to Decode a UDP Packet
translated: false
type: note
---

Here's an example of how to decode a UDP packet in C. This code demonstrates receiving a UDP packet and extracting its key components:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>

// UDP header structure
struct udp_header {
    uint16_t source_port;      // Source port
    uint16_t dest_port;       // Destination port
    uint16_t length;          // Length of UDP packet (header + data)
    uint16_t checksum;        // Checksum
};

void decode_udp_packet(unsigned char* buffer, int size) {
    // Assuming IP header is 20 bytes (without options)
    struct udp_header* udp = (struct udp_header*)(buffer + 20);

    printf("\nUDP Header\n");
    printf("Source Port: %u\n", ntohs(udp->source_port));
    printf("Destination Port: %u\n", ntohs(udp->dest_port));
    printf("Length: %u\n", ntohs(udp->length));
    printf("Checksum: 0x%04x\n", ntohs(udp->checksum));

    // Calculate data length and pointer
    int udp_header_size = 8;  // UDP header is 8 bytes
    int data_length = ntohs(udp->length) - udp_header_size;
    unsigned char* data = buffer + 20 + udp_header_size;

    printf("Data: ");
    for(int i = 0; i < data_length && i < 20; i++) {  // Print first 20 bytes max
        printf("%02x ", data[i]);
    }
    printf("\n");
}

int main() {
    int sockfd;
    struct sockaddr_in server_addr, client_addr;
    unsigned char buffer[65535];  // Max UDP packet size

    // Create UDP socket
    sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sockfd < 0) {
        perror("Socket creation failed");
        return 1;
    }

    // Initialize server address
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(12345);  // Example port

    // Bind socket
    if (bind(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("Bind failed");
        close(sockfd);
        return 1;
    }

    printf("Listening for UDP packets on port 12345...\n");

    while (1) {
        socklen_t client_len = sizeof(client_addr);
        int received_bytes = recvfrom(sockfd, buffer, sizeof(buffer), 0,
                                    (struct sockaddr*)&client_addr, &client_len);

        if (received_bytes < 0) {
            perror("Receive failed");
            continue;
        }

        decode_udp_packet(buffer, received_bytes);
    }

    close(sockfd);
    return 0;
}
```

This code does the following:

1. Defines a `udp_header` structure that matches the UDP packet header format:
   - Source port (16 bits)
   - Destination port (16 bits)
   - Length (16 bits)
   - Checksum (16 bits)

2. Creates a UDP socket and binds it to port 12345 (you can change this port number).

3. The `decode_udp_packet` function:
   - Takes a raw packet buffer as input
   - Assumes a 20-byte IP header precedes the UDP header (Note: this might vary if IP options are present)
   - Extracts and converts the header fields from network byte order (big-endian) to host byte order using `ntohs`
   - Prints the header information
   - Extracts and displays the payload data

To compile and run:
```bash
gcc udp_decoder.c -o udp_decoder
sudo ./udp_decoder  # Needs sudo because of raw socket usage
```

Important notes:
1. This is a basic example - real-world applications might need:
   - Error checking for packet size
   - Handling of IP header options (variable length)
   - Checksum verification
   - More sophisticated data processing

2. To test it, you can:
   - Send UDP packets using netcat: `echo "test" | nc -u 127.0.0.1 12345`
   - Use a packet generator tool

3. The code assumes the packet includes an IP header. If you're working with raw UDP data, remove the +20 offset.

4. For production use, add more error handling and possibly use `struct udphdr` from `<netinet/udp.h>` instead of custom struct.

Would you like me to explain any specific part in more detail or show a variation of this code?
