---
audio: false
generated: true
image: false
lang: en
layout: post
title: GitHub Copilot API Bridge
translated: false
type: note
---

You’ve landed on **ericc-ch/copilot-api**, a GitHub project that transforms **GitHub Copilot** into a local API server compatible with **OpenAI** and **Anthropic** (e.g., Claude) APIs.

Here’s a clearer breakdown—no tables, just straight talk:

---

### What’s This?

* It’s a **reverse-engineered proxy** that lets you interact with GitHub Copilot using familiar OpenAI-style endpoints like `/v1/chat/completions`, `/v1/models`, and `/v1/embeddings`. You can also use Anthropic-compatible endpoints such as `/v1/messages` ([GitHub][1]).

* Essentially, this lets tools that support OpenAI or Anthropic APIs—like Claude Code—use GitHub Copilot as their backend ([GitHub][1]).

---

### Key Features

* **OpenAI & Anthropic Compatibility**: Works like the real OpenAI or Anthropic API ([GitHub][1]).
* **Claude Code Integration**: Ready to plug into Claude Code with a `--claude-code` flag ([GitHub][1]).
* **Usage Dashboard**: Monitor your Copilot API usage and quotas via a built-in web interface ([GitHub][1]).
* **Rate Limiting & Approval Controls**: Includes options for rate-limiting (`--rate-limit`), auto-waiting (`--wait`), manual approval (`--manual`), and debugging (showing tokens)—great for avoiding GitHub’s abuse systems ([GitHub][1]).
* **Supports Various Copilot Plans**: Individual, business, or enterprise accounts all work ([GitHub][1]).

---

### Setup & Usage

* **Prerequisites**: You'll need Bun (≥ 1.2.x) and a GitHub Copilot subscription ([GitHub][1]).
* **Installation Options**:

  * **Docker**:

    ```bash
    docker build -t copilot-api .
    docker run -p 4141:4141 -v $(pwd)/copilot-data:/root/.local/share/copilot-api copilot-api
    ```

    Or pass your GitHub token directly via `GH_TOKEN` ([GitHub][1]).
  * **npx**:

    ```bash
    npx copilot-api@latest start --port 8080
    ```

    Or `npx copilot-api@latest auth` just to authenticate ([GitHub][1]).
* **Command Structure**:

  * `start`: Launches the API server (handles auth if needed).
  * `auth`: Triggers GitHub login without running the server.
  * `check-usage`: Outputs current Copilot usage in your terminal.
  * `debug`: Shows diagnostic info (versions, auth status, etc.), with optional `--json` output ([GitHub][1]).

---

### Real-World Feedback

Reddit users have chimed in:

> “This project lets you turn copilot into an openai compatible endpoint.” ([Reddit][2])
> “It is an awesome project to make your …” ([Reddit][3])

---

### Important Caveats

* **Unofficial & Unsupported**: This is **not** an official GitHub product and could break anytime ([GitHub][1]).
* **Risk of Abuse Detection**: Heavy or automated usage might trigger GitHub’s abuse protection and could suspend your Copilot access ([GitHub][1]).
* **Potential Rate-Limit Issues**: Some users have reported errors like `421 Misdirected Request`, and the maintainer paused development while investigating ([GitHub][4]).

---

### Summary (No Tables Needed)

* **What It Does**: Exposes GitHub Copilot as if it were an OpenAI/Anthropic API.
* **Why That Matters**: Makes Copilot usable in tools expecting those APIs—like Claude Code.
* **How to Use It**: Install via Docker or npx; run commands to start, authenticate, or monitor usage.
* **Proceed With Caution**: It’s handy, but unofficial, and GitHub’s rate-limits or security safeguards may trip up heavy use.

---

Let me know if you’d like help setting it up, or are curious about integrating it into a specific project or tool!

[1]: https://github.com/ericc-ch/copilot-api?utm_source=chatgpt.com "ericc-ch/copilot-api"
[2]: https://www.reddit.com/r/ChatGPTCoding/comments/1m6cqac/how_to_use_your_github_copilot_subscription_with/?utm_source=chatgpt.com "How to use your GitHub Copilot subscription with Claude ..."
[3]: https://www.reddit.com/r/ClaudeAI/comments/1lc21gk/using_github_copilot_as_a_provider_for_claude_code/?utm_source=chatgpt.com "Using GitHub Copilot as a provider for Claude Code"
[4]: https://github.com/ericc-ch/copilot-api/issues/7?utm_source=chatgpt.com "Issue #7 · ericc-ch/copilot-api - 421 Misdirected Request"
