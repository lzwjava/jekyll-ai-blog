---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: NanoChat Compact Full Stack LLM
translated: false
type: note
---

### What is NanoChat?

NanoChat is a compact, full-stack implementation of a large language model (LLM) system similar to ChatGPT, built in a single, minimal codebase that's easy to hack on and requires few dependencies. Created by Andrej Karpathy (famous for his work in AI, like nanoGPT), it's designed to run the complete LLM pipeline—from tokenization and pretraining to finetuning, evaluation, inference, and even a simple web UI for chatting with your model—on affordable hardware like a single 8xH100 GPU node.

It's positioned as the "best ChatGPT that $100 can buy," serving as a baseline for budget-friendly LLM development (under $1,000 total). This makes it a capstone project for Karpathy's upcoming LLM101n course by Eureka Labs, emphasizing simplicity over complex configs.

### Key Features

- **End-to-End Pipeline**: Handles everything in ~2,000 lines of code (with a tiny `uv.lock` file for deps). Trains a capable model with 4e19 FLOPs in about 4 hours on an 8xH100 setup costing ~$24/hour.
- **ChatGPT-Like UI**: After training, spin up a web server to interact with your model just like the real ChatGPT.
- **Evaluation Report**: Auto-generates a `report.md` with benchmark scores on tasks like ARC-Challenge, GSM8K, HumanEval, MMLU, and more. For example, a sample $100 run shows progressive improvements across stages (BASE, MID, SFT, RL):

| Metric        | BASE   | MID    | SFT    | RL     |
|---------------|--------|--------|--------|--------|
| CORE          | 0.2219 | -      | -      | -      |
| ARC-Challenge | -      | 0.2875 | 0.2807 | -      |
| ARC-Easy      | -      | 0.3561 | 0.3876 | -      |
| GSM8K         | -      | 0.0250 | 0.0455 | 0.0758 |
| HumanEval     | -      | 0.0671 | 0.0854 | -      |
| MMLU          | -      | 0.3111 | 0.3151 | -      |
| ChatCORE      | -      | 0.0730 | 0.0884 | -      |

(Total time: ~3h51m for the full run.)

- **Hardware Flexibility**: Works on Ampere 8xA100 (slower), single GPUs (with auto gradient accumulation), or lower-VRAM setups by tweaking batch sizes. Uses vanilla PyTorch; adaptable to other devices with tweaks.
- **Data Sources**: Pulls from Hugging Face datasets like FineWeb and SmolTalk.
- **Extras**: Includes tests (e.g., for the Rust-based tokenizer), and it's easy to package the whole repo (~330KB) for querying with other LLMs.

It's inspired by Karpathy's earlier nanoGPT project and modded-nanoGPT, but scaled up for a full chat experience.

### How to Get Started

The quickest way is the `speedrun.sh` script, which handles the $100-tier model end-to-end on an 8xH100 (e.g., via Lambda Labs):

1. Boot an 8xH100 instance and clone the repo.
2. Run:

   ```
   bash speedrun.sh
   ```

   (Or in a screen session for logging: `screen -L -Logfile speedrun.log -S speedrun bash speedrun.sh`. Detach with Ctrl+A+D and tail the log.)

3. Once done (~4 hours), activate the env (`source .venv/bin/activate`) and serve the UI:

   ```
   python -m scripts.chat_web
   ```

   Open the local URL (e.g., <http://your-ip:8000>) to chat with your model. Check `report.md` for results.

For bigger models (e.g., $300 tier in ~12 hours, beating GPT-2 on some scores), edit `speedrun.sh` to download more data shards and adjust depth/batch sizes. Run tests like `python -m pytest tests/test_rustbpe.py -v -s`.

It's MIT-licensed and open for contributions to push micro-models further. For a detailed walkthrough, check the repo's Discussions.

[nanoChat GitHub Repo](https://github.com/karpathy/nanochat)
