---
audio: false
generated: true
lang: en
layout: post
title: Networking System Calls
translated: false
type: note
---

In operating systems like Linux/Unix, the lowest-level system calls for networking, particularly for establishing a TCP connection, come from the Berkeley Sockets API (often just called "sockets"). These system calls interact directly with the kernel's networking stack. The most fundamental ones for TCP connections are:

1. **`socket()`** - Creates a new socket.
2. **`bind()`** - Assigns an address to the socket (optional for clients).
3. **`connect()`** - Initiates a connection to a remote server (for clients).
4. **`listen()`** - Marks the socket as accepting connections (for servers).
5. **`accept()`** - Accepts an incoming connection (for servers).
6. **`send()` / `recv()`** - Sends or receives data over the connection.
7. **`close()`** - Closes the socket.

These are the raw system calls you'd use at the lowest level, below any higher-level libraries like `libcurl` or frameworks. Here's a simple example in C showing both a TCP client and server establishing a connection.

---

### TCP Server Example

This code sets up a server that listens for a connection on port 8080, accepts it, and sends a message.

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

    // Create socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == -1) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Set up server address structure
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY; // Bind to any address
    server_addr.sin_port = htons(8080);       // Port 8080

    // Bind socket
    if (bind(server_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    // Listen for connections
    if (listen(server_fd, 3) < 0) { // Allow up to 3 queued connections
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }
    printf("Server listening on port 8080...\n");

    // Accept incoming connection
    client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
    if (client_fd < 0) {
        perror("Accept failed");
        exit(EXIT_FAILURE);
    }
    printf("Connection accepted\n");

    // Send message to client
    send(client_fd, message, strlen(message), 0);

    // Clean up
    close(client_fd);
    close(server_fd);
    return 0;
}
```

---

### TCP Client Example

This code connects to the server at `127.0.0.1:8080` and reads the message.

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

    // Create socket
    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd == -1) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Set up server address structure
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(8080);              // Port 8080
    inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr); // Localhost

    // Connect to server
    if (connect(sock_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Connection failed");
        exit(EXIT_FAILURE);
    }
    printf("Connected to server\n");

    // Receive message from server
    recv(sock_fd, buffer, sizeof(buffer), 0);
    printf("Server message: %s", buffer);

    // Clean up
    close(sock_fd);
    return 0;
}
```

---

### Explanation of Key System Calls

- **`socket(AF_INET, SOCK_STREAM, 0)`**: Creates a TCP socket (`AF_INET` for IPv4, `SOCK_STREAM` for TCP).
- **`bind()`**: Associates the socket with a local address and port (server-side).
- **`listen()`**: Prepares the socket to accept connections (server-side).
- **`accept()`**: Blocks until a client connects, then returns a new socket for communication.
- **`connect()`**: Initiates a TCP handshake with the server (client-side).
- **`send()` / `recv()`**: Handle data transfer over the established connection.
- **`close()`**: Terminates the socket.

These are as low-level as it gets for TCP networking in user space. Below this, you’d be dealing with kernel internals (e.g., the TCP/IP stack itself), which isn’t directly accessible via system calls without writing kernel code.

To compile and run:

1. Save the server code as `server.c` and client code as `client.c`.
2. Compile: `gcc server.c -o server` and `gcc client.c -o client`.
3. Run the server first: `./server`.
4. In another terminal, run the client: `./client`.

Let me know if you want more details or a deeper dive!
