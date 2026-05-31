---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ncat SOCKS5 ProxyCommand Flow Analysis
translated: false
type: note
---

Now I have the full picture from the nmap source tree. Here's how ncat works in your SSH ProxyCommand setup:

```
ncat --proxy localhost:7891 --proxy-type socks5 %h %p
```

THE FULL FLOW (from source code):

1. OPTION PARSING (ncat_main.c:441-448)
   --proxy      -> o.proxyaddr = "localhost:7891"
   --proxy-type -> o.proxytype = "socks5"
   %h %p        -> o.target = hostname, o.portno = port (SSH 22)

2. PROXY ADDRESS RESOLUTION (ncat_main.c:753)
   parseproxy("localhost:7891", ...) resolves the proxy itself
   targetaddrs now points to localhost:7891 (the SOCKS proxy, NOT the final SSH target)
   The real target (o.target) is kept aside for the SOCKS5 CONNECT request

3. DISPATCH (ncat_connect.c:1064)
   if (strcmp(o.proxytype, "socks5") == 0)
       connect_socket = do_proxy_socks5();

4. TCP CONNECT TO PROXY (ncat_connect.c:639, util.c:489-517)
   sd = do_connect(SOCK_STREAM)
   Creates raw TCP socket, connects to targetaddrs (= localhost:7891)
   This is the ONLY direct network connection ncat makes

5. SOCKS5 HANDSHAKE — Phase 1: Auth Negotiation (ncat_connect.c:650-671)
   Sends:  [0x05, 0x01, 0x00]  = SOCKS5, 1 method, NO AUTH
   Receives: [0x05, 0x00]       = SOCKS5, NO AUTH accepted
   (If --proxy-auth was given, it also offers method 0x02 USERPASS)

6. SOCKS5 HANDSHAKE — Phase 2: CONNECT Request (ncat_connect.c:773-828)
   Sends socks5_request struct:
     ver  = 0x05 (SOCKS5)
     cmd  = 0x01 (CONNECT)
     rsv  = 0x00
     atyp = 0x03 (DOMAINNAME) or 0x01 (IPv4) or 0x04 (IPv6)
     dst  = hostname bytes + port (2 bytes, network order)
   
   Example for "github.com:22":
     [0x05, 0x01, 0x00, 0x03, 0x0A]
     + "github.com"
     + [0x00, 0x16]  (port 22)

7. SOCKS5 RESPONSE (ncat_connect.c:830-920)
   Receives 4-byte header, checks reply code 0x00 = success
   Reads bound address (variable length based on atyp)
   Returns the socket fd

8. DATA RELAY (ncat_connect.c:1074-1097)
   Once proxy negotiation succeeds:
     cs.sock_nsi = nsock_iod_new2(mypool, connect_socket, NULL);
   Nsock (nmap's async I/O library) takes over the raw socket
   nsock_loop(mypool, -1) runs the event loop
   Data flows: SSH <-> ncat stdin/stdout <-> SOCKS proxy <-> internet

WHY IT'S SLOW FOR BULK TRANSFERS:

The bottleneck is step 8. Nsock's event loop copies data through
userspace buffers with DEFAULT_BUF_LEN (8KB for TCP). Each chunk:

  read(socket) -> buffer -> write(stdout)   (proxy -> SSH)
  read(stdin)  -> buffer -> write(socket)   (SSH -> proxy)

This is two extra copy() syscalls per direction per buffer-full.
For a git packfile that's say 50MB:

  50MB / 8KB = ~6,400 round trips through the event loop
  Each with 2 syscalls = ~12,800 extra syscalls

Plus nsock does its own select()/poll() overhead on each iteration.

ALTERNATIVES AND WHY THEY'RE FASTER:

  connect (brew install connect):
    Uses splice()/sendfile() where possible
    Direct fd-to-fd relay, no event loop abstraction
    ProxyCommand: connect -H localhost:7891 %h %p

  nc -X 5 -x localhost:7891:
    Uses raw read()/write() with larger buffers
    No nsock event loop overhead
    ProxyCommand: nc -X 5 -x localhost:7891 %h %p

Both skip the nsock indirection layer and do simpler I/O loops
with potentially larger buffers (64KB+ instead of 8KB).

For your model repos — you're right to prefer HTTPS remotes over
SSH for large packfile transfers through the proxy. The SOCKS5
handshake itself (steps 4-7) is fast (~2ms), it's the sustained
throughput that suffers.