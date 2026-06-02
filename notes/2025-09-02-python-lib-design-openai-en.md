---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python Library Design Lessons from OpenAI
translated: false
type: note
---

Here’s a quick teardown of `openai/openai-python` and the lessons you can lift for building a great Python library.

# What the repo shows (at a glance)

* **Clear “src layout”**: `src/openai` for code; top-level `tests/`, `examples/`, `scripts/`, `.github/`, `pyproject.toml`, `mypy.ini`, `noxfile.py`, etc. That separation keeps import paths clean and test discovery predictable. ([GitHub][1])
* **Typed public surface**: requests use `TypedDict`, responses are **Pydantic** models; great DX and safer refactors. ([GitHub][1])
* **Sync + Async parity**: `OpenAI` and `AsyncOpenAI` share the same API; default transport is `httpx`, with optional `aiohttp`. ([GitHub][1])
* **First-class streaming**: Server-Sent Events with simple iteration in both sync and async. ([GitHub][1])
* **Auto-pagination**: iterable list endpoints so users don’t hand-roll page loops. ([GitHub][1])
* **Realtime/WebSocket client**: an opt-in sub-client with examples and error-handling guidance. ([GitHub][1])
* **Codegen pipeline**: the SDK is generated from an OpenAPI spec (via Stainless), which enforces consistency and type coverage. ([GitHub][1])

# Design takeaways you can reuse

* **Keep the “one obvious way”**: expose a single `Client` (plus `AsyncClient`) with mirror method names. Users shouldn’t wonder “which class should I use?” The OpenAI SDK shows this with `OpenAI` and `AsyncOpenAI`. ([GitHub][1])
* **Portable transports**: default to `httpx`, but allow a swappable HTTP backend (e.g., `aiohttp`), so high-concurrency users aren’t boxed in. ([GitHub][1])
* **Typed requests + models**: ship typed request payloads and rich response models. That buys you editor autocomplete, lintable examples, and safer breaking changes. ([GitHub][1])
* **Zero-friction streaming**: design streaming as a plain iterator / async iterator. No custom event pumps needed. ([GitHub][1])
* **Iterator-based pagination**: expose `for item in client.resource.list(limit=...)` and fetch pages lazily. It keeps user code tiny while remaining efficient. ([GitHub][1])
* **Subsystems are sub-clients**: put specialized features (e.g., realtime) behind a clearly-named namespace (`client.beta.realtime`) to keep the main surface clean. ([GitHub][1])
* **Generate where it helps**: if your API is spec-driven, let codegen create the boring, strongly-typed layers and hand-craft the ergonomic bits. ([GitHub][1])

# A skeleton you can copy

```bash
yourlib/
  pyproject.toml
  noxfile.py
  mypy.ini
  README.md
  CHANGELOG.md
  SECURITY.md
  src/yourlib/
    __init__.py
    _version.py
    _types.py            # TypedDicts, enums
    _errors.py           # Exception hierarchy
    _http.py             # httpx client wrapper, retries, timeouts
    _pagination.py       # generic Pager[T]
    client.py            # Client + AsyncClient, auth, base URL
    resources/
      __init__.py
      widgets.py         # resource groups w/ sync+async methods
    streaming.py         # SSE helpers (sync/async)
  tests/
    test_client.py
    test_widgets.py
  examples/
    quickstart.py
    async_quickstart.py
```

## Public API (`src/yourlib/__init__.py`)

* Re-export just what users need:

```python
from .client import Client, AsyncClient
from ._errors import YourLibError, APIError, RateLimitError
__all__ = ["Client", "AsyncClient", "YourLibError", "APIError", "RateLimitError"]
```

## Client shape (sync & async)

* Mirror the same method names; differ only in `await`/`async`:

```python
# src/yourlib/client.py
import httpx
from .resources.widgets import Widgets
from ._http import HttpTransport

class Client:
    def __init__(self, api_key=None, base_url="https://api.example.com", http_client=None):
        self._transport = HttpTransport(api_key, base_url, http_client or httpx.Client(timeout=30))
        self.widgets = Widgets(self._transport)

class AsyncClient:
    def __init__(self, api_key=None, base_url="https://api.example.com", http_client=None):
        self._transport = HttpTransport(api_key, base_url, http_client or httpx.AsyncClient(timeout=30))
        self.widgets = Widgets(self._transport)
```

## Pagination pattern

```python
# src/yourlib/_pagination.py
from typing import AsyncIterator, Iterator, Generic, TypeVar, Callable, Optional
T = TypeVar("T")
class Pager(Generic[T]):
    def __init__(self, fetch: Callable[..., dict], limit: int = 100):
        self._fetch = fetch
        self._limit = limit
        self._cursor = None
    def __iter__(self) -> Iterator[T]:
        while True:
            page = self._fetch(limit=self._limit, cursor=self._cursor)
            for item in page["data"]:
                yield item
            self._cursor = page.get("next_cursor")
            if not self._cursor:
                break
```

Expose it so users can `for item in client.widgets.list(limit=50): ...`. (OpenAI’s SDK takes the same approach. ([GitHub][1]))

## Streaming pattern (SSE)

* Wrap `httpx`’s streaming with a small iterator that yields events; mirror an async variant. That yields the ergonomic `for event in client.responses.create(..., stream=True)` UX seen in the OpenAI SDK. ([GitHub][1])

# Tooling & release flow that scales

* **`pyproject.toml` (PEP 621)** for metadata; lock dev deps separately.
* **Type checking**: ship types, run `mypy` in CI (their repo has `mypy.ini`). ([GitHub][1])
* **Task runner**: `nox` sessions for test, lint, typecheck, build (they use `noxfile.py`). ([GitHub][1])
* **CI**: GitHub Actions in `.github/` to run tests across Python versions/platforms. ([GitHub][2])
* **CHANGELOG** and **versioning**: keep a human-readable log; automate releases (they use release-please). ([GitHub][1])
* **Security & Contributing docs**: set expectations for reporters and contributors. ([GitHub][1])

# Docs & examples

* **README examples** should be runnable and copy-paste friendly—sync, async, streaming, pagination, and any “special transports” (like `aiohttp`). The OpenAI README demonstrates each succinctly. ([GitHub][1])
* **API reference**: if code-generated, publish an `api.md`/reference site and keep it in lockstep with releases. ([GitHub][1])
* **Examples folder**: include minimal, focused scripts, plus one “full” sample.

# Errors, retries, and timeouts (what to implement)

* **Error hierarchy**: `YourLibError` → `APIError`, `AuthError`, `RateLimitError`, `TimeoutError`. Map HTTP status codes to exceptions; include request IDs.
* **Retries**: idempotent operations should auto-retry with exponential backoff + jitter on 429/5xx.
* **Timeouts**: set sensible defaults and make them configurable at client and per-call levels.
* **Logging hooks**: structured debug logging without leaking secrets.

# Packaging & compatibility

* **Support 3–4 active Python minors** (e.g., 3.9–3.13), and test them in CI.
* **No side effects on import**; defer network/client creation until first use.
* **Environment config**: accept `API_KEY` env var but let users pass credentials explicitly too (OpenAI shows `OPENAI_API_KEY` and a `.env` tip). ([GitHub][1])
* **Stable public API**: keep internals private (`_module.py`), re-export a tidy surface in `__init__.py`.

# Pitfalls to avoid

* Cramming everything into a single module; split by resource and keep public imports stable.
* Leaking transport types; your resources should depend on a tiny “transport” protocol, not `httpx` directly.
* Making async feel second-class; ensure tests and examples cover both equally (OpenAI’s parity is a good model). ([GitHub][1])
* For streaming, don’t force users to juggle threads or callbacks—iterators are simpler. ([GitHub][1])

If you want, I can scaffold this structure for a concrete domain (e.g., a typed client for your internal REST services, with sync/async, pagination, and streaming) and drop in ready-to-run `nox`, CI, and example scripts.

[1]: https://github.com/openai/openai-python "GitHub - openai/openai-python: The official Python library for the OpenAI API"
[2]: https://github.com/openai/openai-python/tree/main/.github "openai-python/.github at main · openai/openai-python · GitHub"
