---
audio: false
generated: true
image: false
lang: en
layout: post
title: SEC Edgar Prompt File Setup
translated: false
type: note
---

Done. 5 prompt files created in /mnt/data/zz/:

  prompt1_business.txt   — Company overview (healthcare SaaS)
  prompt2_mda.txt        — MD&A with revenue/gross profit analysis
  prompt3_risk.txt       — Risk factors (net losses, quarterly fluctuation)
  prompt4_notes.txt      — Notes with revenue recognition + table
  prompt5_proxy.txt      — Proxy statement with exec comp table

Attach to the tmux session and run any of these:

  tmux attach -t sec-sample

Then paste these commands one at a time:

  python3 sample.py --out_dir=out-sec-edgar-124m --start='FILE:/mnt/data/zz/prompt1_business.txt' --num_samples=1 --max_new_tokens=1200 --temperature=0.7

  python3 sample.py --out_dir=out-sec-edgar-124m --start='FILE:/mnt/data/zz/prompt2_mda.txt' --num_samples=1 --max_new_tokens=1200 --temperature=0.7

  python3 sample.py --out_dir=out-sec-edgar-124m --start='FILE:/mnt/data/zz/prompt3_risk.txt' --num_samples=1 --max_new_tokens=1200 --temperature=0.7

  python3 sample.py --out_dir=out-sec-edgar-124m --start='FILE:/mnt/data/zz/prompt4_notes.txt' --num_samples=1 --max_new_tokens=1200 --temperature=0.7

  python3 sample.py --out_dir=out-sec-edgar-124m --start='FILE:/mnt/data/zz/prompt5_proxy.txt' --num_samples=1 --max_new_tokens=1200 --temperature=0.7

You can also edit the .txt files to change prompts, or create new ones — just use FILE:/path/to/yourfile.txt as the --start argument.
