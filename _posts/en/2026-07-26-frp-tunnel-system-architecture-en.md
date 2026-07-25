---
audio: false
generated: true
image: false
lang: en
layout: post
title: FRP Tunnel System Architecture
translated: false
type: note
---

Great question! Here's how the whole thing works under the hood:

---

## 🧠 The Architecture: FRP Tunnel System

The rc-tunnel tool is a **client-server tunnel** built on top of [**frp** (Fast Reverse Proxy)](https://github.com/fatedier/frpc). Here's the full picture:

### 1. The Key Components

```
┌──────────────────────────────────┐       ┌──────────────────────────────┐
│     Your Notebook (Pod)          │       │   Platform / Ops Side       │
│                                  │       │                              │
│  ┌──────────┐   ┌───────────┐    │       │  ┌──────────────────────┐   │
│  │ Your App │──▶│ frpc      │────┼──────▶│  │ frps (Broker Server) │   │
│  │:8081     │   │ (client)  │    │       │  │ :8443                 │   │
│  └──────────┘   └───────────┘    │       │  └──────┬───────────────┘   │
│                                  │       │         │                    │
│   Identities & Secrets:          │       │  ┌──────▼───────────────┐   │
│   /var/run/secrets/frp-self-     │       │  │ Public Nginx/Proxy   │   │
│     service/                     │       │  │ *.radeon.firstdg.ai  │   │
│     ├── ca.crt  (TLS CA)         │       │  └──────────────────────┘   │
│     ├── token   (JWT auth)       │       └──────────────────────────────┘
│     ├── namespace                │
│     └── install (script)         │               🌐 Internet
│                                  │                   │
└──────────────────────────────────┘         ┌─────────▼──────────┐
                                             │  End User's Browser │
                                             │ curl https://rc-... │
                                             └────────────────────┘
```

### 2. Bootstrapping Flow

Here's the step-by-step logic we followed:

```
Step 1: Identity Injection
─────────────────────────
Kuberbernetes injects these into the Pod:
  ├── /var/run/secrets/frp-self-service/ca.crt  ← TLS trust anchor
  ├── /var/run/secrets/frp-self-service/token   ← JWT for authentication
  ├── /var/run/secrets/frp-self-service/namespace ← K8s namespace
  └── Environment variables (via PID 1):
      ├── FRP_BROKER_URL = https://10.110.220.177:8443
      └── FRP_BROKER_TLS_SERVER_NAME = frp-broker.frp-self-service-poc.svc.cluster.local

Step 2: Install Script
──────────────────────
/var/run/secrets/frp-self-service/install does:
  1. Validates env vars exist (FRP_BROKER_URL, FRP_BROKER_TLS_SERVER_NAME)
  2. Downloads rc-tunnel binary from the broker:
     curl --cacert ca.crt \
          --connect-to <tls_host>:<port>:<broker_ip>:<port> \
          https://<tls_host>:<port>/downloads/rc-tunnel-linux-amd64
     → The --connect-to bypasses DNS (it's a cluster-internal service)
  3. Installs to ~/.local/bin/rc-tunnel
  4. Adds ~/.local/bin to PATH in .bashrc/.profile

Step 3: Authentication
──────────────────────
When you run "rc-tunnel expose --port 8081":
  1. rc-tunnel reads the JWT token from /var/run/secrets/frp-self-service/token
  2. It authenticates to the FRP broker using this token
  3. The broker's frps validates the JWT (signed by Kubernetes API server)
  4. On success, the broker assigns a unique domain: rc-<random>.radeon.firstdg.ai

Step 4: Tunnel Establishment
─────────────────────────────
  1. rc-tunnel generates an frpc config file at ~/.local/state/rc-tunnel/frpc.toml
  2. It downloads the frpc binary (the actual FRP client)
  3. Starts frpc as a child process (PID 1140 in our case)
  4. frpc opens a persistent TCP connection to frps at 10.110.220.177:8443
  5. Both sides do mutual TLS verification using the CA certificate
  6. frps registers the proxy route: rc-a899e6bb9beab78e → this Pod's :8081

Step 5: Request Flow
─────────────────────
  User → https://rc-a899e6bb9beab78e.radeon.firstdg.ai
         ↓
  DNS resolves → Platform's public load balancer
         ↓
  Nginx/Proxy (platform side) → frps (broker)
         ↓
  frps looks up the route → finds our frpc connection
         ↓
  frps forwards the HTTP request through the persistent TCP tunnel
         ↓
  frpc in our Pod receives it → forwards to 127.0.0.1:8081
         ↓
  Our Python HTTP server responds → response goes back through the tunnel
```

### 3. Why the Env Vars Weren't in the Shell

This was the tricky part we hit. The Notebook **is** a new-enough Pod (it has the identity directory), but:

```bash
# These were set at container startup but NOT exported to login shells:
/proc/1/environ contains:
  FRP_BROKER_URL=https://10.110.220.177:8443
  FRP_BROKER_TLS_SERVER_NAME=frp-broker.frp-self-service-poc.svc.cluster.local

# But when you SSH in, your shell doesn't inherit them
echo $FRP_BROKER_URL  # (empty)
```

That's why we had to manually source them from `/proc/1/environ` — the Pod's initialization injected them into PID 1 but didn't write them to `/etc/environment` or a profile script.

### 4. Security Model

| Layer | Mechanism |
|-------|-----------|
| **TLS transport** | Mutual TLS between frpc ↔ frps, verified via `ca.crt` |
| **Authentication** | JWT token signed by Kubernetes API server (service account) |
| **Identity binding** | Token embeds the Pod name, namespace, and node info — frps verifies the Pod is allowed to expose ports |
| **No key sharing** | Never copy `~/.local/state/rc-tunnel` or the token to another Pod |
| **User responsibility** | The tunnel URL is public — your app must enforce its own authentication |

### 5. Lifecycle

```
                    ┌────────────┐
                    │ Pod starts │
                    └─────┬──────┘
                          │
                    ┌─────▼──────┐
                    │ Install    │  ← Run install script once
                    │ rc-tunnel  │
                    └─────┬──────┘
                          │
                    ┌─────▼──────┐
                    │ rc-tunnel  │  ← "expose --port 8081"
                    │ expose     │     Requests domain, starts frpc
                    └─────┬──────┘
                          │
               ┌──────────▼──────────┐
               │ Tunnel active       │  ← Public URL live
               │ PID: 1140           │     Heartbeat every N seconds
               └──────────┬──────────┘
                          │
               ┌──────────▼──────────┐
               │ rc-tunnel stop      │  ← Domain enters 24h freeze
               │ (or Pod terminates) │     Port released immediately
               └─────────────────────┘
```

### 6. The "Old Pod" Check

The install script does this upfront:

```bash
broker_url=${FRP_BROKER_URL:?FRP_BROKER_URL is not injected into this Notebook}
tls_host=${FRP_BROKER_TLS_SERVER_NAME:?FRP_BROKER_TLS_SERVER_NAME is not injected into this Notebook}
```

The `:?` in bash means **"if unset or empty, print this error and exit"**. So if the env vars aren't there at all (old Pods), the script immediately fails with that message — you can't proceed without recreating the Notebook.

---

**In short:** The Notebook acts as an frpc client that opens a persistent TCP connection to a central frps broker. The broker assigns a public subdomain and reverse-proxies HTTP traffic through that tunnel back to your local port. It's like a managed, authenticated ngrok tailored for this platform.
