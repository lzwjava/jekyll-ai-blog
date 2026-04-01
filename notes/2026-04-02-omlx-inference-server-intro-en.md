---
audio: false
generated: true
image: false
lang: en
layout: post
title: Introduction to oMLX.ai Inference Server
translated: false
type: note
---

I'll search for information about omlx.ai to provide you with a comprehensive introduction.Let me search for more detailed technical information about oMLX.**Question:** What is a comprehensive introduction to omlx.ai?

**Answer:**

## Overview

oMLX is a native macOS inference server built on MLX, specifically optimized for Apple Silicon (M1, M2, M3, M4) processors. It provides paged SSD KV caching, continuous batching, and drop-in API compatibility for Claude Code, OpenClaw, and Cursor.

## Key Innovation: Tiered KV Caching

The standout feature that distinguishes oMLX from alternatives like Ollama and LM Studio is its intelligent caching system. While Ollama and LM Studio cache the KV state in memory, when the context shifts mid-session — which happens constantly with coding agents — the entire cache gets invalidated and recomputed from scratch. oMLX persists every KV cache block to SSD, so previously cached portions are always recoverable, reducing TTFT (Time To First Token) from 30-90 seconds to under 5 seconds on long contexts.

The cache operates in two tiers:
- **Hot tier (RAM)**: Frequently accessed blocks remain in memory for fast access
- **Cold tier (SSD)**: When the hot cache fills, blocks are offloaded to SSD in safetensors format and can be restored from disk instead of being recomputed

## Core Features

### Multi-Model Support
oMLX supports text LLMs, vision-language models (VLM), OCR models, embeddings, and rerankers on Apple Silicon. Models are managed through automatic LRU eviction, manual load/unload controls, model pinning, and per-model TTL settings.

### Performance Optimization
Continuous batching handles concurrent requests through mlx-lm's BatchGenerator, achieving up to 4.14× generation speedup at 8× concurrency. The system includes context scaling support specifically optimized for Claude Code.

### Native macOS Integration
The application is a native PyObjC menubar app (not Electron) that allows users to start, stop, and monitor the server without opening a terminal. It includes persistent serving stats, auto-restart on crash, and in-app auto-update.

### Admin Dashboard
A web UI at /admin provides real-time monitoring, model management, chat, benchmark, and per-model settings, supporting English, Korean, Japanese, and Chinese. The dashboard includes a built-in model downloader for searching and downloading MLX models from HuggingFace.

### API Compatibility
oMLX serves as a drop-in replacement for OpenAI and Anthropic APIs, providing both OpenAI-compatible (/v1/chat/completions) and Anthropic-compatible (/v1/messages) API endpoints. It supports streaming, tool calling, structured output, and MCP (Model Context Protocol) integration.

## System Requirements

Apple Silicon (M1 or later) with macOS 15+ is required, with 16GB RAM as the minimum, though 64GB+ is recommended for comfortable use with larger models. The sweet spot for daily coding work is described as an M-series Pro/Max with 64GB or more.

## Installation Methods

1. **macOS App**: Download the DMG from GitHub releases with in-app auto-update
2. **Homebrew**: Install via `brew tap jundot/omlx` and `brew install omlx`
3. **From Source**: Clone the repository and install with pip

## Performance Benchmarks

On M3 Ultra with 512GB, Qwen3.5-122B-A10B-4bit achieves 768 tok/s prompt processing and 56.6 tok/s token generation at 1k context, demonstrating impressive performance for local AI workloads.

## Use Cases

Primary use cases include local AI programming assistants working with tools like Claude Code and Cursor, model research and experimentation, privacy-sensitive applications requiring data to never leave the user's device, and multi-model deployment for complex AI applications.

oMLX represents a significant advancement in making local LLM inference practical for real-world development work on Apple Silicon, particularly for coding agents that traditionally struggled with frequent context invalidation.

**References:**

- [https://omlx.ai/](https://omlx.ai/)
- [https://github.com/jundot/omlx](https://github.com/jundot/omlx)
- [https://jimmysong.io/ai/omlx/](https://jimmysong.io/ai/omlx/)