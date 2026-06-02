---
audio: false
generated: true
image: false
lang: en
layout: post
title: Warp's Core Technology Stack
translated: false
type: note
---

Here's the major libraries Warp uses:

== Major External Dependencies ==

GPU & Rendering
----------------

wgpu 29.0.1        - GPU abstraction layer (Metal on macOS, Vulkan on Linux)
metal               - Apple Metal API bindings (macOS GPU rendering)
cocoa 0.26.0        - macOS Cocoa framework bindings
core-foundation     - macOS Core Foundation (windows, events, fonts)
objc2-app-kit       - macOS App Kit bindings
font-kit            - Font loading and rasterization (forked by Warp)

Async & Networking
------------------

tokio 1.47.1        - Async runtime (the backbone)
hyper 1.6.0         - HTTP client/server
reqwest 0.13        - HTTP client (API calls, AI endpoints)
axum 0.8.4          - HTTP server framework
tower 0.5.2         - Service middleware
rustls              - TLS (instead of OpenSSL for most paths)
actix-web           - Additional HTTP server
prost               - Protobuf serialization (gRPC APIs)

Data & Storage
--------------

serde               - Serialization framework
serde_json          - JSON
diesel 2.3.8        - SQLite ORM (persistence layer)
libsqlite3-sys      - SQLite bindings
tantivy 0.26.0      - Full-text search engine (command palette, search)
git2                - Git repository operations

Terminal & Text
---------------

syntect             - Syntax highlighting
arborium-*          - Tree-sitter based parsers (30+ languages)
regex               - Regular expressions

AI & Auth
---------

oauth2 5.0.0        - OAuth2 authentication
firebase            - Firebase auth integration
sentry              - Error tracking and crash reporting

Utilities
---------

clap 4.5            - CLI argument parsing
chrono              - Date/time handling
uuid                - UUID generation
image 0.25.9        - Image processing
nix 0.26.4          - Unix system calls (signals, process management)
anyhow              - Error handling
log                 - Logging facade

== Architecture Pattern ==

- GPU-accelerated UI via wgpu (not native toolkit widgets)
- Custom rendering pipeline (similar to game engines)
- Async-first with Tokio
- SQLite for local persistence
- Tantivy for fast search
- Tree-sitter for code understanding
- Protobuf/gRPC for backend communication
