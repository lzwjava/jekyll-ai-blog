---
audio: false
generated: true
lang: en
layout: post
title: Rust's Rise in Big Tech
translated: false
type: note
---

Rust is gaining significant traction in big tech due to its strong focus on memory safety, performance, and concurrency. Many major tech companies are adopting Rust for various critical projects. Here's a breakdown of some prominent examples:

**1. Amazon (AWS)**

* **Firecracker:** A microVM designed to safely run container workloads at scale, powering AWS Lambda and Fargate.
* **AWS Nitro System:** Used for developing new components, including secure and isolated EC2 environments.
* **Other Services:** Rust is used in components of Amazon S3, Amazon EC2, Amazon CloudFront, and Amazon Route 53.
* **Bottlerocket:** A Linux-based container operating system written in Rust.

**2. Microsoft**

* **Windows Components:** Microsoft is actively rewriting parts of Windows, including kernel components, in Rust to improve safety and maintainability.
* **Azure Services:** Rust is integrated into Azure IoT Edge and Kusto (the core query and storage engine for Azure Data Explorer).
* **`windows-rs`:** A project that allows calling Windows APIs using Rust.

**3. Meta (Facebook)**

* **Internal Source Control Tools:** Meta rebuilt parts of their internal source control system (Mononoke) in Rust to handle their large monorepo with better concurrency and speed.
* **Diem (formerly Libra) Blockchain:** The blockchain for this cryptocurrency project was primarily written in Rust.

**4. Google**

* **Android Open Source Project (AOSP):** Rust is increasingly used to write safe system components in Android, reducing memory bugs in critical functions like media processing and file system access.
* **Fuchsia OS:** A significant proportion of Fuchsia OS's internal code is written in Rust.
* **Chromium:** Experimental support for Rust exists in Chromium.

**5. Dropbox**

* **Sync Engine:** Rust replaced older Python and C++ code in Dropbox's file synchronization engine, leading to reduced CPU usage, better concurrency, and smoother syncing.
* **Core File-Storage System:** Several components of their core file-storage system are written in Rust.

**6. Discord**

* **Backend Services:** Discord uses Rust for critical backend services like message routing and presence tracking, improving performance and reliability. They switched from Go to Rust for their "Read States" service to avoid latency spikes.
* **Client and Server Sides:** Both the client and server sides of Discord's codebase have Rust components.

**7. Cloudflare**

* **Pingora:** A high-performance web proxy written in Rust to replace NGINX, resulting in reduced CPU usage and improved connection management.
* **Core Edge Logic:** Rust is used in Cloudflare's core edge logic as a replacement for memory-unsafe languages like C.
* **Cloudflare Workers:** Supports serverless code deployment with Rust.

**8. Mozilla**

* **Firefox (Stylo):** Mozilla, the original creator of Rust, used the language to build Stylo, the CSS engine in Firefox, significantly improving performance and safety.
* **Servo:** A prototype web browser engine built entirely in Rust.

**9. npm (Node Package Manager)**

* **Authentication Services:** npm used Rust to rewrite parts of its authentication services to improve security, handle load, and reduce delays.

**Other Notable Adopters and Projects:**

* **Linux Kernel:** Rust is now the second official language for Linux kernel development, allowing for safer device drivers and other modules.
* **Figma:** Their multiplayer synchronization engine was rewritten from TypeScript to Rust for improved performance.
* **1Password:** Powers their latest desktop and mobile apps with a single shared Rust codebase.
* **Hugging Face:** Many components in their AI ecosystem, including `safetensors`, `tokenizer`, and `candle`, are implemented using Rust.
* **Polkadot:** This blockchain platform is built entirely in Rust for security and speed.
* **Solana:** Another high-performance blockchain platform that leverages Rust.
* **Brave Browser:** Uses Rust in some of its components.
* **Atlassian:** Uses Rust in a service for analyzing petabytes of source code.
* **Huawei:** Migrated parts of its codebase to Rust for telecommunications equipment and infrastructure tools.

The adoption of Rust by these major tech companies underscores its growing importance for building reliable, efficient, and secure software, particularly for system-level programming, infrastructure, and high-performance applications.
