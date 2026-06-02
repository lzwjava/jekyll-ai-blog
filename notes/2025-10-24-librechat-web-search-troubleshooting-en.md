---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Troubleshooting LibreChat Web Search
translated: false
type: note
---

Let’s troubleshoot this carefully — when **web search doesn’t work in LibreChat** even after adding **Firecrawl**, **SerpApi**, and **Jina API** keys, the issue is almost always one of these: configuration mistakes, missing backend enable flags, or UI misinterpretation.

Here’s a clear breakdown you can follow (no tables, just explanations):

---

### 1. **Check if “Web Search” is enabled in the backend config**

Open your LibreChat server config file (usually `.env` or `api/config.yaml` depending on your setup) and confirm you have something like:

```
# For .env
SEARCH_ENABLED=true
```

Or, if using YAML:

```yaml
features:
  search: true
```

If `SEARCH_ENABLED` or `search` is not explicitly set to `true`, the UI button may appear but won’t actually perform searches.

---

### 2. **Confirm API keys are properly named**

Each provider expects specific environment variable names. For example:

* For **SerpApi**:

  ```
  SERPAPI_API_KEY=your_key_here
  ```
* For **Firecrawl**:

  ```
  FIRECRAWL_API_KEY=your_key_here
  ```
* For **Jina**:

  ```
  JINA_API_KEY=your_key_here
  ```

Also make sure these are exported or loaded in the same environment as the running `backend` process.

To check:

```bash
echo $SERPAPI_API_KEY
```

If it returns blank, your backend doesn’t see it.

---

### 3. **Restart LibreChat after editing keys**

LibreChat doesn’t hot-reload environment variables. Run:

```bash
docker compose down
docker compose up -d
```

(or `npm run start` again if you’re not using Docker).

---

### 4. **Verify which search provider LibreChat is actually using**

LibreChat picks one default web search backend depending on config order.

If you want it to use SerpApi, for example, you must specify:

```
SEARCH_PROVIDER=serpapi
```

Alternatively, if you want Jina:

```
SEARCH_PROVIDER=jina
```

If you only set keys but didn’t define which provider to use, LibreChat may default to none.

---

### 5. **Look at backend logs**

Run:

```bash
docker logs librechat-backend
```

or

```bash
npm run start:debug
```

Look for messages like:

```
[Search] SerpApi key missing or invalid
```

or

```
Search provider not configured
```

These are the best clues.

---

### 6. **Test the APIs directly**

To make sure your keys actually work:

**SerpApi test:**

```bash
curl "https://serpapi.com/search.json?q=chatgpt&api_key=YOUR_KEY"
```

**Firecrawl test:**

```bash
curl "https://api.firecrawl.dev/v1/search?q=chatgpt" -H "Authorization: Bearer YOUR_KEY"
```

**Jina test:**

```bash
curl "https://r.jina.ai/chatgpt" -H "Authorization: Bearer YOUR_KEY"
```

If these fail, the keys themselves are invalid or rate-limited.

---

### 7. **Frontend version mismatch**

If you recently updated LibreChat (especially from pre-v0.7 to v0.8+), the frontend `Web Search` toggle might exist even though your backend version doesn’t support the integrated Firecrawl/Jina search module yet.
Run:

```bash
git pull
```

and rebuild:

```bash
docker compose build --no-cache
docker compose up -d
```

---

### 8. **Final check — confirm from Web UI**

Open the UI, go to **Settings → Features**, and confirm:

* “Web Search” toggle is ON
* Your selected provider is listed (SerpApi, Firecrawl, or Jina)

If it says *“No provider available”*, the backend isn’t reading your keys.

---

If you want, you can paste your relevant `.env` (with the keys masked) and I’ll pinpoint exactly which line is missing or misnamed.

Would you like to show me that snippet?
