---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dynamic Copilot Model Fetching Guide
translated: false
type: note
---

Question: What is the `GET https://api.githubcopilot.com/models` endpoint, how does it work, and how can I use it to dynamically fetch the model list for a `/model` command instead of hardcoding models?

Answer:

## Overview of `GET https://api.githubcopilot.com/models`

This is an **unofficial but widely-used** GitHub Copilot internal API endpoint that returns the list of AI models available to your specific Copilot subscription. It is **not part of the official `docs.github.com` REST API documentation**, but is reverse-engineered from how VS Code and JetBrains Copilot clients communicate with GitHub's backend.

---

## Endpoint Details

| Property | Value |
|---|---|
| **Method** | `GET` |
| **URL** | `https://api.githubcopilot.com/models` |
| **Auth** | Bearer token (Copilot OAuth token, not a GitHub PAT) |
| **Returns** | A list of models your subscription supports |

---

## Required Headers

For all Copilot API requests, you need two essential headers: `Authorization: Bearer YOUR_COPILOT_TOKEN` for authentication, and `Copilot-Integration-Id: vscode-chat` to identify the integration type.

Additionally, GitHub Copilot may also expect headers like `Editor-Version`, `Editor-Plugin-Version`, and `User-Agent` to identify your application.

### Full Header Example

```bash
curl -X GET 'https://api.githubcopilot.com/models' \
  -H 'Authorization: Bearer YOUR_COPILOT_TOKEN' \
  -H 'Copilot-Integration-Id: vscode-chat' \
  -H 'Content-Type: application/json' \
  -H 'Editor-Version: vscode/1.104.1' \
  -H 'Editor-Plugin-Version: copilot-chat/0.26.7' \
  -H 'User-Agent: GitHubCopilotChat/0.26.7'
```

---

## Response Format

The response returns a JSON object with a `data` array, where each item includes fields like `id`, `object`, `created`, and `owned_by`. A simplified example:

```json
{
  "data": [
    {
      "id": "gpt-4o",
      "object": "model",
      "created": 1234567890,
      "owned_by": "github-copilot"
    },
    {
      "id": "claude-3.5-sonnet",
      "object": "model",
      "created": 1234567890,
      "owned_by": "github-copilot"
    }
  ]
}
```

Each `id` in the list is a model identifier you can pass to `/chat/completions`.

---

## Why It's Subscription-Aware

Copilot hosts many models from OpenAI, Anthropic, Google, and others. You can list the models your subscription allows by calling this endpoint, and each returned ID can then be used directly in your API calls. This means:

- **Copilot Individual** may return fewer models
- **Copilot Business / Enterprise** may return additional or premium models
- The list changes as GitHub adds or removes model support

---

## How to Get the Copilot OAuth Token

The token needed here is **not** your normal GitHub PAT. It's a short-lived Copilot session token. The easiest path is to sign in to Copilot from any JetBrains IDE (PyCharm, GoLand, etc.) — after you authenticate, a file appears containing the `oauth_token` value, which is your token for API calls.

You can also obtain it programmatically via the token endpoint used by Copilot clients (e.g., `https://api.github.com/copilot_internal/v2/token`).

---

## Updating `/model` Command to Use This Endpoint

Here's how you would implement a dynamic `/model` command in JavaScript/TypeScript:

```typescript
async function fetchAvailableModels(copilotToken: string): Promise<string[]> {
  const response = await fetch("https://api.githubcopilot.com/models", {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${copilotToken}`,
      "Copilot-Integration-Id": "vscode-chat",
      "Content-Type": "application/json",
      "Editor-Version": "vscode/1.104.1",
      "Editor-Plugin-Version": "copilot-chat/0.26.7",
      "User-Agent": "GitHubCopilotChat/0.26.7"
    }
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch models: ${response.statusText}`);
  }

  const data = await response.json();
  // Extract just the model IDs
  return data.data.map((model: { id: string }) => model.id);
}

// Example usage in your /model command handler:
async function handleModelCommand(copilotToken: string) {
  const models = await fetchAvailableModels(copilotToken);
  console.log("Available models for your subscription:");
  models.forEach(id => console.log(` - ${id}`));
}
```

---

## Key Benefits of Dynamic Fetching vs. Hardcoding

| Hardcoded | Dynamic (`/models` endpoint) |
|---|---|
| Breaks when GitHub adds/removes models | Always up-to-date |
| May show models the user can't access | Only shows subscription-supported models |
| Requires code change to update | Zero maintenance |
| Fast (no network call needed) | Small latency cost (one extra request at startup) |

---

## Important Caveats

- This is a **reverse-engineered, unofficial endpoint** — GitHub could change it without notice.
- Excessive automated or scripted use of the Copilot API may trigger GitHub's abuse-detection systems, and further anomalous activity could result in temporary suspension of your Copilot access.
- Cache the model list (e.g., for 10–30 minutes) rather than re-fetching on every `/model` command invocation.

References:

- [aider - GitHub Copilot Integration](https://aider.chat/docs/llms/github.html)
- [Alorse/copilot-to-api on GitHub](https://github.com/Alorse/copilot-to-api)
- [ericc-ch/copilot-api on GitHub](https://github.com/ericc-ch/copilot-api)
- [@opeoginni/github-copilot-openai-compatible on npm](https://www.npmjs.com/package/@opeoginni/github-copilot-openai-compatible)
- [GitHub Models API Changelog](https://github.blog/changelog/2025-05-15-github-models-api-now-available/)