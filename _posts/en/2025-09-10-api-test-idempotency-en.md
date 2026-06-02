---
audio: false
date: 2025-09-10
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: API Test Uniqueness and Idempotency Strategy
translated: false
type: note
---

Great question. Let’s zoom out, then get practical about “uniqueness” in API/integration tests.

# What’s what (quick refresher)

* **URL (path + query)**

  * Path is usually the **resource identity**: `/orders/123`.
  * Query params are **filters/modifiers**: `/orders?status=PAID&page=2`.

* **Method**

  * `GET/HEAD` are safe.
  * `PUT` is **idempotent** (same call, same result).
  * `POST` is **not** idempotent unless you add an **Idempotency-Key** scheme.
  * `PATCH` is not guaranteed idempotent.

* **Headers**

  * `Content-Type`: how the **body** is encoded.

    * `application/json` → JSON body.
    * `application/x-www-form-urlencoded` → `a=1&b=2` body.
    * `multipart/form-data; boundary=----abcd` → file/uploads & mixed parts.
  * `Content-Disposition` appears **inside multipart parts**, not the top-level request. A typical part:

    ```
    --Boundary123
    Content-Disposition: form-data; name="file"; filename="x.png"
    Content-Type: image/png

    <binary bytes>
    --Boundary123--
    ```
  * Useful custom headers:

    * **Idempotency-Key**: de-duplicate side-effectful POSTs.
    * **X-Request-ID / Correlation-ID**: trace/log a single request across services.

* **Body**

  * JSON: a serialized document.
  * `form-urlencoded`: key-value pairs like a query string but in the body.
  * `multipart/form-data`: multiple “parts” separated by the `boundary` delimiter (`----WebKitFormBoundary...` is a common browser string).

# Where should identity live?

* **Resource identity** → in the **URL path** (`/users/{id}`), because it’s stable and bookmarkable.
* **Operation modifiers** → query or headers.
* **Representation/state to write** → body.

Trying to encode request uniqueness only in the URL often fails for write ops (e.g., POST with large JSON). Instead, think in **two layers**:

1. **Request identity (fingerprint)**:
   A deterministic hash of:

   * HTTP **method**
   * **Canonicalized path** (template + concrete values)
   * **Normalized query** (sorted)
   * **Selected headers** (only those that affect semantics, e.g., `Accept`, `Content-Language`, *not* `Date`)
   * **Body** (normalized JSON or a digest per part for multipart)

2. **Operation identity (business idempotency)**:
   For side-effectful ops (create/charge/transfer), use **Idempotency-Key** (a UUID per *business intention*). The server stores the first result under that key and returns it for retries.

These solve different problems: fingerprints help your **tests** and **observability**; idempotency keys protect **production** from duplicate effects.

# Testing strategy for “uniqueness”

1. **Define a request fingerprint function** (client/test side). Example logic:

   * Lowercase header names; include only a safe allowlist.
   * Sort query params; stable JSON stringify the body (remove whitespace, sort keys).
   * SHA-256 over `METHOD\nPATH\nQUERY\nHEADERS\nBODY`.

2. **Give every test a Correlation ID**

   * Generate a UUID per test case: `X-Request-ID: test-<suite>-<uuid>`.
   * Log it server-side so you can tie logs to one test.

3. **Use Idempotency-Key where needed**

   * For POSTs that create resources or charge money:

     * `Idempotency-Key: <uuid>`
     * Server should return the same 200/201 and body for retries with the same key within a retention window.

4. **Keep test data unique but minimal**

   * Use seeded, deterministic IDs (e.g., email `user+T001@example.com`) or suffix with the test UUID.
   * Clean up, or better, design tests to be **idempotent** by using PUT/DELETE against your seeded IDs where possible.

5. **Assert at the right level**

   * For **idempotent** operations: assert **status**, **representation**, and **side effects** (e.g., record count unchanged on repeat).
   * For **non-idempotent** POSTs with Idempotency-Key: assert first call 201, subsequent retry 200 with same body (or 201 repeated with the same resource).

# Practical snippets

**cURL examples**

* JSON POST:

  ```bash
  curl -X POST https://api.example.com/orders \
    -H 'Content-Type: application/json' \
    -H 'Idempotency-Key: 4b6f2d1a-...' \
    -H 'X-Request-ID: test-orders-create-...' \
    -d '{"customerId":"C123","items":[{"sku":"ABC","qty":1}]}'
  ```
* Multipart upload:

  ```bash
  curl -X POST https://api.example.com/uploads \
    -H 'X-Request-ID: test-upload-...' \
    -F 'file=@/path/pic.png' \
    -F 'meta={"purpose":"avatar"};type=application/json'
  ```

  (curl sets `Content-Type: multipart/form-data; boundary=----...` and each part has its own `Content-Disposition`.)

**Python test-side request fingerprint (illustrative):**

```python
import hashlib, json, urllib.parse

def canonical_json(obj):
    return json.dumps(obj, separators=(',', ':'), sort_keys=True)

def normalize_query(url):
    parsed = urllib.parse.urlsplit(url)
    q = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    q.sort()
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urllib.parse.urlencode(q), '')), q

def request_fingerprint(method, url, headers=None, body_bytes=b''):
    headers = headers or {}
    # allowlist headers that affect semantics
    allow = {'accept', 'content-type', 'content-language'}
    norm_headers = {k.lower(): v.strip() for k, v in headers.items() if k.lower() in allow}
    header_line = '\n'.join(f'{k}:{norm_headers[k]}' for k in sorted(norm_headers))
    url_no_query, q_pairs = normalize_query(url)
    query_line = '&'.join(f'{k}={v}' for k, v in q_pairs)
    h = hashlib.sha256()
    h.update((method.upper() + '\n').encode())
    h.update((url_no_query + '\n').encode())
    h.update((query_line + '\n').encode())
    h.update((header_line + '\n').encode())
    h.update(body_bytes or b'')
    return h.hexdigest()
```

* For JSON bodies, pass `body_bytes=canonical_json(payload).encode()`.
* For multipart, hash each part then hash the concatenation to avoid boundary noise.

# Answering your core idea

> “If URL is unique then requests are unique; params/body still contribute a lot—how to think about uniqueness for API/integration tests?”

* Treat **URL alone** as **insufficient** for uniqueness in tests, because headers and body materially change semantics.
* Build a **request fingerprint** as above for dedup/trace in tests.
* For business-level de-duplication of **POSTs**, rely on **Idempotency-Key**, not URL.
* Keep **resource identity** in the path for clarity and better test determinism.

# Small checklist you can adopt today

* [ ] Add `X-Request-ID` (UUID) to every test request.
* [ ] Add `Idempotency-Key` to POSTs that create/charge.
* [ ] Implement a test helper that computes a request fingerprint and logs it with each assertion.
* [ ] Canonicalize JSON before hashing; sort query params; allowlist semantic headers.
* [ ] Prefer PUT for upserts to make tests idempotent; reserve POST for true creates.
* [ ] For multipart, assert on **server-parsed parts** (names, filenames, content types) rather than raw boundary bytes.

If you share your current test stack (pytest/unittest + requests/httpx, or Java/Kotlin), I can drop in a ready-to-use helper tailored to it.
