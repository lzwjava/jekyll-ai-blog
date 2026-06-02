---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Disabling LibreChat Web Search Citations
translated: false
type: note
---

## Disabling Citations in LibreChat Web Search Mode

LibreChat's web search feature (powered by providers like Serper.dev or SearxNG, combined with scrapers like Firecrawl) automatically includes citations in responses to credit sources and improve transparency. Based on official documentation and community discussions, there is no built-in user-facing toggle specifically for disabling web search citations at the individual user level. However, you can achieve this or approximate it through configuration changes, primarily for admins or self-hosters. Here's how:

### 1. **Admin-Level Configuration (Recommended Approach)**
   If you're running your own instance of LibreChat (self-hosted), modify the configuration files to limit or remove citation rendering. Citations are handled via the interface and search components.

   - **Edit `librechat.yaml` for Interface Settings**:
     LibreChat uses a YAML file for global settings. Look for the `interface` section, which controls citation visibility (inspired by file citation controls, which may extend to web search).
     - Set `fileCitations` to `false` to globally disable citation permissions. While this is explicitly for file searches, it can influence web search UI rendering in some setups.
       ```yaml
       interface:
         fileCitations: false  # Disables citation display for searches overall
       ```
     - For web search specifically, under the `webSearch` section, you can disable or customize providers to avoid detailed source linking:
       ```yaml
       webSearch:
         enabled: true  # Keep enabled, but adjust providers
         serper:  # Or your provider
           enabled: true
           # No direct 'citations' flag, but omitting API keys for scrapers like Firecrawl reduces detailed extracts/cites
         firecrawl:
           enabled: false  # Disables content scraping, which often generates citations
       ```
     - Restart your LibreChat instance after changes. Source for interface config: [LibreChat Interface Object Structure](https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/interface)[1].

   - **Environment Variables (.env File)**:
     In your `.env` file, disable debug or logging modes that might enforce citations, or set web search to a minimal provider.
     - Example:
       ```
       DEBUG_PLUGINS=false  # Reduces verbose output, including citations
       SERPER_API_KEY=your_key  # Use a basic search provider without scraping for fewer cites
       FIRECRAWL_API_KEY=  # Leave blank to disable scraper (no page extracts/citations)
       ```
     - This shifts responses to summary-only search results without inline citations. Full setup: [LibreChat .env Configuration](https://www.librechat.ai/docs/configuration/dotenv)[2].

   - **Web Search Provider Customization**:
     Switch to a provider like SearxNG, which can be configured server-side to omit source links.
     - Set `SEARXNG_INSTANCE_URL=your_minimal_searxng_url` in `.env`.
     - In your SearxNG instance, edit its settings to suppress result metadata (e.g., via `settings.yml` in SearxNG: disable `reveal_version: false` and customize templates to remove links).
     - Documentation: [Web Search Configuration](https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/web_search)[3].

### 2. **User-Level Workarounds (No Admin Access)**
   If you're using a hosted LibreChat (e.g., public instance), options are limited since citations are often enforced for accuracy:
   - **Prompt Engineering**: Instruct the AI explicitly in your messages, e.g., "Search the web but do not include citations or sources in your response." This works inconsistently as the search tool may still append them, but many models will comply partially.
   - **Disable Web Search Entirely**: If citations are the main issue, turn off web search per conversation:
     - In the chat interface, avoid clicking the "Web Search" button.
     - For agents: When creating/editing an agent, remove the `web_search` capability in the agent's config (via the Agents UI). Source: [Agents Documentation](https://www.librechat.ai/docs/features/agents)[4].
     - Request admins to add a toggle; community discussions suggest this as a feature request (e.g., [GitHub Discussion on Web Search Toggle](https://github.com/danny-avila/LibreChat/discussions/7738)[5]).

### 3. **Limitations and Notes**
   - Citations are a core part of web search to ensure ethical AI use and traceability, so fully disabling them might require custom code modifications (e.g., editing frontend components like `WebSearchResults.jsx` in the GitHub repo to hide citation elements).
   - No direct "turn off citations" flag exists in current versions (as of October 2025). Check for updates in the [Web Search Feature Docs](https://www.librechat.ai/docs/features/web_search)[6], as features evolve.
   - If self-hosting, test changes in a dev environment—disabling scrapers might reduce response quality.
   - Community feedback (e.g., Reddit) notes occasional bugs with search features, but nothing specific to citations: [Reddit Thread on LibreChat Issues](https://www.reddit.com/r/LocalLLaMA/comments/1k2hraj/is_it_just_me_or_is_librechat_a_complete_buggy/)[7].

For official support, join the LibreChat Discord or open a GitHub issue with your setup details. If this doesn't resolve it, provide more context about your LibreChat version or hosting method!

Citations:
[1] https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/interface
[2] https://www.librechat.ai/docs/configuration/dotenv
[3] https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/web_search
[4] https://www.librechat.ai/docs/features/agents
[5] https://github.com/danny-avila/LibreChat/discussions/7738
[6] https://www.librechat.ai/docs/features/web_search
[7] https://www.reddit.com/r/LocalLLaMA/comments/1k2hraj/is_it_just_me_or_is_librechat_a_complete_buggy/
