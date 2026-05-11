---
audio: false
generated: true
image: false
lang: en
layout: post
title: Progress Tracker for Resumable Dataset Downloads
translated: false
type: note
---

- progress.json lives in the output dir alongside the parquet files. It stores the selected shard plan with
  status: pending|done per shard.
  - First run: lists shards from HF, selects the 100B-token slice, writes progress.json, then starts
  downloading.
  - Cancelled mid-shard (Ctrl-C): the in-flight shard leaves a .part file. JSON still marks it pending.
  - Restart: loads progress.json (no HF API call), skips done shards instantly, resumes the .part via HTTP Range
   — only that one shard continues.
  - --refresh-plan forces re-listing from the Hub if you want a new plan.

  Status is fsynced after each shard completes (atomic via .tmp + os.replace), so a crash never leaves the JSON
  inconsistent.