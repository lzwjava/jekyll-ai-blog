---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Configuring GitHub Copilot LLM Router
translated: false
type: note
---

To configure your LLM router to exclusively use GitHub Copilot's LLM API in an enterprise setting, add a dedicated provider for it and adjust the router settings to route all traffic through that provider.

- **Add a GitHub Copilot Provider**: Include a new entry in the "Providers" array with the appropriate API base URL, your GitHub personal access token (PAT) as the API key, and supported models.
- **Update Router Defaults**: Change all router fields (e.g., "default", "think") to point solely to the new provider name, ensuring no other providers are called.
- **Handle Enterprise Restrictions**: Use your enterprise GitHub account's PAT with the necessary scopes, and leverage the existing "PROXY_URL" if your environment requires proxy routing for compliance.
- **Test and Verify**: After updates, validate that all API calls are directed only to the Copilot endpoint to align with policies allowing solely Copilot API interactions.

### Step-by-Step Configuration

1. **Generate a GitHub PAT**: Log into your GitHub enterprise account and create a personal access token with scopes like `copilot` for chat access or `models:read` for broader model inference. This ensures secure authentication without exposing broader permissions.
2. **Modify the Providers Array**: Append a new object to the "Providers" list in your config JSON. Set "name" to something descriptive like "github_copilot", "api_base_url" to "<https://api.githubcopilot.com/chat/completions>" (for Copilot agents) or "<https://models.github.ai/inference/chat/completions>" (for general GitHub Models inference), "api_key" to your PAT, and list compatible models.
3. **Adjust the Router Section**: Replace all values in the "Router" object with your new provider name (e.g., "github_copilot") to enforce exclusive usage. This prevents fallback to other providers like OpenRouter.
4. **Enterprise Considerations**: In restricted environments, confirm your network policies allow outbound calls to GitHub's domains. If needed, update "PROXY_URL" to route through an approved enterprise proxy. Enable logging ("LOG": true) to audit calls and ensure compliance.

### Example Updated Config

Here's how your config might look after modifications (replace placeholders with your actual PAT and preferred endpoint):

```json
{
  "PROXY_URL": "http://127.0.0.1:7890",
  "LOG": true,
  "Providers": [
    {
      "name": "openrouter",
      "api_base_url": "https://openrouter.ai/api/v1/chat/completions",
      "api_key": "",
      "models": [
        "moonshotai/kimi-k2",
        "anthropic/claude-sonnet-4",
        "anthropic/claude-3.5-sonnet",
        "anthropic/claude-3.7-sonnet:thinking",
        "anthropic/claude-opus-4",
        "google/gemini-2.5-flash",
        "google/gemini-2.5-pro",
        "deepseek/deepseek-chat-v3.1",
        "deepseek/deepseek-r1",
        "mistralai/mistral-medium-3.1",
        "qwen/qwen3-coder",
        "openai/gpt-oss-120b",
        "openai/gpt-5",
        "z-ai/glm-4.6",
        "x-ai/grok-code-fast-1",
        "x-ai/grok-4-fast",
        "minimax/minimax-m2",
        "moonshotai/kimi-k2-thinking"
      ],
      "transformer": {
        "use": [
          "openrouter"
        ]
      }
    },
    {
      "name": "github_copilot",
      "api_base_url": "https://api.githubcopilot.com/chat/completions",
      "api_key": "ghp_YourPersonalAccessTokenHere",
      "models": [
        "gpt-4o",
        "gpt-4o-mini",
        "claude-3-5-sonnet-20240620"
      ],
      "transformer": {
        "use": [
          "github_copilot"
        ]
      }
    }
  ],
  "Router": {
    "default": "github_copilot",
    "background": "github_copilot",
    "think": "github_copilot",
    "longContext": "github_copilot",
    "longContextThreshold": 30000,
    "webSearch": "github_copilot"
  }
}
```

This setup ensures the router only interacts with the Copilot API, complying with enterprise policies that restrict calls to approved endpoints.

---

In enterprise environments, integrating LLM APIs like GitHub Copilot requires careful configuration to adhere to security policies, often limiting outbound calls to specific approved services. The provided router config appears to be a custom setup for routing LLM requests across providers, similar to tools like OpenRouter or LiteLLM, where "Providers" define API endpoints and models, and "Router" dictates fallback or category-specific routing. To adapt this for exclusive use of GitHub Copilot's LLM API—ensuring no other external services are invoked—you'll need to incorporate Copilot as a provider and enforce it across all router paths. This approach supports scenarios where enterprise firewalls or compliance rules permit only GitHub-hosted APIs, leveraging Copilot's OpenAI-compatible interface for chat completions.

GitHub Copilot provides LLM access primarily through two avenues: the dedicated Copilot LLM endpoint for building agents and extensions, and the broader GitHub Models API for general inference. The Copilot-specific endpoint at `https://api.githubcopilot.com/chat/completions` is tailored for enterprise-grade agent development, supporting POST requests in the OpenAI chat completions format. Authentication uses a Bearer token derived from a GitHub personal access token (PAT), typically passed via an `Authorization` header. For instance, a sample request might include headers like `Authorization: Bearer <your-pat>` and `Content-Type: application/json`, with a body containing `messages` (an array of user/system prompts) and optional parameters like `stream: true` for real-time responses. Models aren't explicitly listed in the docs but align with Copilot's underlying providers, such as GPT-4 variants and Claude models, with strict rate limits applied to third-party agents to prevent abuse.

Alternatively, the GitHub Models API at `https://models.github.ai/inference/chat/completions` offers a more versatile inference service, allowing access to a catalog of models using just GitHub credentials. This is ideal for prototyping and integration into workflows like GitHub Actions. Authentication requires a PAT with the `models:read` scope, created via your GitHub settings (<https://github.com/settings/tokens>). In enterprise setups, this can be extended to organization-level tokens or used in CI/CD pipelines by adding `permissions: models: read` to workflow YAML files. Available models include industry standards like `openai/gpt-4o`, `openai/gpt-4o-mini`, `anthropic/claude-3-5-sonnet-20240620`, Meta's Llama 3.1 series, and Mistral variants, all invocable through the same OpenAI-compatible API format. This compatibility makes it straightforward to slot into your router config without major changes to downstream code.

For enterprise-specific configurations, GitHub Copilot Enterprise enhances standard Copilot with organization-wide controls, such as fine-tuned models based on your codebase, but API access follows the same patterns. Network management is crucial: You can configure subscription-based routing to ensure Copilot traffic uses approved paths, requiring users to update their IDE extensions (e.g., VS Code) to minimum versions supporting this. If your environment mandates proxies, update the config's "PROXY_URL" to point to your enterprise proxy server, and consider custom certificates for SSL inspection. Tools like LiteLLM can act as an intermediary proxy for further control—install via `pip install litellm[proxy]`, define models in a YAML config, start the server on a local port, and redirect Copilot requests through it for logging, rate limiting, and fallback handling. However, in your case, since the goal is exclusivity, avoid fallbacks in the router to comply with "only OK to call Copilot" policies.

To implement this in your config, start by appending a new provider object. Choose the endpoint based on your use case: Use the Copilot agent endpoint if building extensions, or GitHub Models for general LLM routing. List models that overlap with your existing ones (e.g., Claude and GPT variants) to maintain compatibility. Then, overwrite all "Router" fields to reference only this new provider, eliminating commas or fallbacks like ",minimax/minimax-m2". Enable logging to monitor compliance, and test by simulating requests to verify no unauthorized endpoints are hit. If integrating with VS Code or other IDEs, adjust settings like `github.copilot.advanced.debug.overrideProxyUrl` to route through your configured proxy if needed.

Here's a comparison table of the two main GitHub LLM API options to help decide which endpoint to use in your provider config:

| Aspect                  | GitHub Copilot LLM API (for Agents)                  | GitHub Models API                                   |
|-------------------------|-----------------------------------------------------|-----------------------------------------------------|
| Endpoint                | <https://api.githubcopilot.com/chat/completions>      | <https://models.github.ai/inference/chat/completions> |
| Primary Use             | Building Copilot extensions and agents              | General prototyping, inference, and workflows       |
| Authentication          | Bearer PAT (via Authorization header)               | PAT with models:read scope                          |
| Models Supported        | Implicit (e.g., GPT-4, Claude variants)             | Explicit catalog: gpt-4o, claude-3-5-sonnet, Llama 3.1, etc. |
| Enterprise Features     | Rate limits for third-parties; integrates with Copilot Enterprise | Usable in GitHub Actions; bring-your-own-key support |
| Rate Limits/Quotas      | Strict for non-GitHub agents                        | Free tier for prototyping; scalable for enterprise  |
| Compatibility           | OpenAI chat format                                  | OpenAI-compatible; easy router integration          |

This table highlights why GitHub Models might be preferable for broad router usage, as it offers more explicit model selection and enterprise workflow integration.

Potential challenges include token expiration (PATs typically last 30-90 days), so automate renewal in enterprise scripts. If your environment uses GitHub Enterprise Cloud, enable Copilot at the organization level for seamless access. For advanced setups, explore bringing your own API keys (BYOK) in GitHub Models to route through preferred providers while staying within GitHub's ecosystem. Always prioritize primary GitHub documentation for the latest scopes and endpoints, as features evolve rapidly. If direct API calls fail due to network restrictions, consider using GitHub's proxy configuration options or integrating with Azure for hybrid enterprise deployments.

In summary, this configuration transforms your router into a Copilot-exclusive system, aligning with enterprise policies while maintaining functionality for code-related or general LLM tasks.

**Key Citations:**

- [Using GitHub Copilot's LLM for your agent](https://docs.github.com/en/enterprise-cloud@latest/copilot/how-tos/use-copilot-extensions/build-a-copilot-agent/use-copilots-llm)
- [Quickstart for GitHub Models](https://docs.github.com/en/github-models/quickstart)
- [GitHub Copilot | liteLLM](https://docs.litellm.ai/docs/tutorials/github_copilot_integration)
- [Managing GitHub Copilot access to your enterprise's network](https://docs.github.com/enterprise-cloud%40latest/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-access/manage-network-access)
- [Configuring network settings for GitHub Copilot](https://docs.github.com/copilot/configuring-github-copilot/configuring-network-settings-for-github-copilot)
- [Prototyping with AI models](https://docs.github.com/github-models/prototyping-with-ai-models)
- [Using your own API keys in GitHub Models](https://docs.github.com/en/github-models/github-models-at-scale/using-your-own-api-keys-in-github-models)
