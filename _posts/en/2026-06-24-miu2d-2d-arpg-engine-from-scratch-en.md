---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Miu2D: 2D ARPG Engine from Scratch"
translated: false
type: note
---

Miu2D is a from-scratch 2D ARPG engine written in TypeScript + Rust, rendering through raw WebGL with zero game-framework dependencies.

Key facts:

- 176,000 lines of code
- TypeScript + Rust (pathfinding compiled to WASM)
- Raw WebGL — no PixiJS, Phaser, Unity, Godot
- Custom sprite batching, A* pathfinding, binary format decoders, scripting VM, weather particles, screen effects — all from first principles
- Custom DSL with 218 commands + Lua 5.4 runtime (via wasmoon)
- Rust A* pathfinding runs in ~0.2ms via WASM with zero-copy shared memory
- SpriteBatcher coalesces ~4,800 tile draws into 1-5 WebGL draw calls

As a proof of concept, it rebuilds three classic Kingsoft (西山居) wuxia RPGs, fully playable in-browser:

1. Legend of Yue Ying (剑侠情缘外传：月影传说) — 2001, 7+ endings
2. Swords of Legends 2 (剑侠情缘贰) — 1998, Diablo-style real-time combat
3. New Swords of Legends (新剑侠情缘) — 2001, 110+ maps

It's a monorepo (pnpm workspace) with a web package, scripts for data conversion/analysis, and a Vercel deployment. The project is built with AI-assisted coding from day one ("vibe coding").

Live demo at <https://miu2d.com>
