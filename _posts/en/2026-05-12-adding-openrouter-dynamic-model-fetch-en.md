---
audio: false
generated: true
image: false
lang: en
layout: post
title: Adding OpenRouter Dynamic Model Fetch
translated: false
type: note
---

Good — I have everything I need. Here's the analysis (no code changes).

## Where the input lives

`lib/clacky/web/settings.js:99-109` renders the combobox: a free-form `<input class="model-name-input">` plus a button that opens `<div class="model-name-dropdown">`. The dropdown is populated by `_updateModelDropdown()` at `settings.js:277-315`, which reads `provider.models` (a static array).

The `_providers` array is loaded once at startup from `GET /api/providers` (`settings.js:27,32`), which is served by `api_list_providers` at `lib/clacky/server/http_server.rb:2815-2832`, which just copies `Providers::PRESETS[id]["models"]` from `lib/clacky/providers.rb`.

## What's already half-done

`providers.rb:78-98` defines the OpenRouter preset with:

```ruby
"base_url" => "https://openrouter.ai/api/v1",
"models" => [],  # Dynamic - fetched from API
```

So the codebase already intends OpenRouter's models to come from its API — but the fetch was never wired up. That's exactly the gap you noticed.

## How to fill it in

OpenRouter exposes `GET https://openrouter.ai/api/v1/models` (no auth required) returning `{ data: [ { id, name, context_length, pricing, ... }, ... ] }`. You want each `id` (e.g. `moonshotai/kimi-k2.6`) as a dropdown option.

Two viable shapes:

**A. Backend fetch + cache (recommended)**
Inside `api_list_providers` (`http_server.rb:2817`), when iterating presets, for the `openrouter` id call `https://openrouter.ai/api/v1/models` via the existing HTTP client, map `data[].id` into `models`, and cache the result (e.g. 1h TTL in an instance var or on disk) so you don't re-fetch on every settings open. On network failure, fall back to `[]` so the UI degrades to a plain text input — same as today.

- Pros: no extra CORS surface in browser, one place to cache, no key leakage risk, reuses existing HTTP infra.
- Cons: backend has to do an outbound call on first request.

**B. Frontend fetch on dropdown open**
In `_updateModelDropdown()` (`settings.js:277`), when the matched provider is OpenRouter and `provider.models` is empty, `fetch("https://openrouter.ai/api/v1/models")` directly from the browser, map `data[].id`, and render. Cache the result on `_providers[i].models` so subsequent opens are instant.

- Pros: smallest diff, no Ruby changes.
- Cons: depends on OpenRouter's CORS headers being permissive (they are today, but it's outside your control); also means every user's browser hits OpenRouter even without a key.

I'd pick **A** because the file comment already implies it ("Dynamic - fetched from API") and it keeps frontend logic uniform (`provider.models` is just a list regardless of source).

## Two extra things worth deciding before implementing

1. **Volume**: OpenRouter lists ~300+ models. The current dropdown CSS (`app.css`, `.model-name-dropdown`) has no scroll/filter — you'll likely want to add a text filter at the top of the dropdown, or sort/group by vendor prefix (`anthropic/*`, `moonshotai/*`, etc.). Otherwise the list is unusable.
2. **Scope of "dynamic"**: only OpenRouter has this property in `providers.rb`. Other providers (Kimi, MiniMax, GLM) keep curated static lists for a reason — the preset acts as a known-good shortlist. Don't generalize the fetch to "any provider with empty models" without thinking through that.

Sources:

- [OpenRouter models endpoint](https://openrouter.ai/docs/api-reference/list-available-models)
