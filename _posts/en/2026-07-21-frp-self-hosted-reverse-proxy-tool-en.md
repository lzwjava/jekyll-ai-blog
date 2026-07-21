---
audio: false
generated: true
image: false
lang: en
layout: post
title: "frp: Self-Hosted Reverse Proxy Tool"
translated: false
type: note
---

Question: What is `fatedier/frp`?

Answer:

frp (Fast Reverse Proxy) is a **reverse proxy / tunneling tool** written in Go. It helps expose services behind NAT or firewalls to the public internet.

Repository: [https://github.com/fatedier/frp](https://github.com/fatedier/frp)

The core idea:

```
Client machine (inside LAN)
        |
        | outbound connection
        |
        v
frpc  <----------------->  frps
                          |
                          |
                    Public server
                    with public IP
```

* `frps` = server side, runs on a VPS with a public IP.
* `frpc` = client side, runs on your machine behind NAT.

Example:

You have a local service:

```
localhost:3000
```

Maybe:

* local web app
* SSH server
* Jupyter notebook
* LLM API server (vLLM)
* home lab service

Your home network has no public IP. Start:

```
your laptop
    |
    | frpc tunnel
    |
    v
VPS (public IP)
    |
    v
https://your-domain.com
```

Now the world can access your local service.

---

### Typical use cases

#### 1. Expose local development server

Local:

```
npm run dev

localhost:5173
```

frpc config:

```toml
[[proxies]]
name = "frontend"
type = "http"
localIP = "127.0.0.1"
localPort = 5173
customDomains = ["demo.example.com"]
```

Then:

```
https://demo.example.com
```

opens your local app.

---

#### 2. SSH into a machine behind NAT

Client:

```
home PC
  sshd :22
```

frpc:

```toml
[[proxies]]
name = "ssh"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = 6000
```

Then:

```bash
ssh user@your-vps-ip -p 6000
```

---

#### 3. AI / LLM serving

Relevant to your setup:

```
RTX 4070 machine
      |
      | frpc
      |
      v
cloud VPS
      |
      v
OpenAI-compatible API
```

Example:

```
localhost:8000/v1
```

(vLLM server)

Expose:

```
https://api.example.com/v1
```

Useful for:

* testing agents remotely
* sharing demos
* hackathons
* webhook callbacks

---

### Compared with alternatives

| Tool               | Purpose                         |
| ------------------ | ------------------------------- |
| frp                | General TCP/HTTP reverse proxy  |
| ngrok              | Easy temporary tunnels          |
| Cloudflare Tunnel  | HTTP services behind Cloudflare |
| Tailscale Funnel   | Tailnet-based sharing           |
| SSH reverse tunnel | Minimal manual solution         |

frp is popular because it is:

* self-hosted
* fast
* Go single binary
* supports TCP/UDP/HTTP/HTTPS
* supports authentication
* supports multiple clients

---

### Minimal deployment

VPS:

```bash
wget https://github.com/fatedier/frp/releases/latest/download/frp_linux_amd64.tar.gz

tar xzf frp_linux_amd64.tar.gz
cd frp_*
```

`frps.toml`

```toml
bindPort = 7000
```

Run:

```bash
./frps -c frps.toml
```

Client:

`frpc.toml`

```toml
serverAddr = "your-vps-ip"
serverPort = 7000

[[proxies]]
name = "ssh"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = 6000
```

Run:

```bash
./frpc -c frpc.toml
```

---

For your AI workflow, the interesting use case is: **run vLLM/Jupyter/agent servers on GPU machines (AMD Cloud, RunPod, home GPU) and use frp to expose them through a cheap VPS without needing a public IP.**
