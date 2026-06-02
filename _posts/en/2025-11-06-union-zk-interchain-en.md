---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Union ZK Interchain Infrastructure Protocol
translated: false
type: note
---

### Overview
The GitHub repository at [https://github.com/unionlabs/union](https://github.com/unionlabs/union) is the official open-source codebase for **Union**, a zero-knowledge (ZK) infrastructure protocol developed by Union Labs. Union aims to enable seamless, secure interoperability between different blockchains, allowing assets and data to move across chains without traditional bridges, custodians, or trusted intermediaries. It leverages ZK proofs to verify transactions and state transitions, focusing on scalability, privacy, and composability in the multi-chain ecosystem.

### Key Features
- **ZK-Light Client**: Uses zero-knowledge proofs for lightweight, trust-minimized verification of blockchain states and consensus, reducing reliance on heavy relayers.
- **Interoperability Primitives**: Supports cross-chain messaging, asset transfers (e.g., tokens, NFTs), and arbitrary data passing between EVM-compatible chains and beyond.
- **Modular Architecture**: Built with Cosmos SDK and Tendermint for consensus, but extensible to other frameworks. It includes components like the Union relayer, proof generators, and verifier contracts.
- **Security Focus**: Emphasizes cryptographic primitives like Groth16 proofs and BLS signatures to prevent common bridge exploits.

### Development Status (as of November 2025)
- The repo is actively maintained, with recent commits focusing on testnet integrations (e.g., Union Testnet v2 launched in mid-2025).
- It has over 500 stars, contributions from 50+ developers, and is licensed under Apache-2.0.
- Documentation includes setup guides for running nodes, deploying contracts, and integrating with wallets like MetaMask.

### Use Cases
- DeFi protocols bridging liquidity across Ethereum, Solana, and Cosmos ecosystems.
- Gaming and NFT projects needing cross-chain portability.
- Enterprise apps requiring private, verifiable data sharing between ledgers.

If you're a developer, you can clone the repo and start with `make install` for dependencies, then `make build` to compile. For more, check the [docs folder](https://github.com/unionlabs/union/tree/main/docs) or Union Labs' site.

[Union Labs Website](https://union.build/)
[Union Whitepaper](https://union.build/whitepaper)
[GitHub Repo](https://github.com/unionlabs/union)
