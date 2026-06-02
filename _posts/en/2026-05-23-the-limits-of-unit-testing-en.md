---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Limits of Unit Testing
translated: false
type: note
---

Honest take: this is a common belief but it's actually a half-truth.

Unit tests are great FOR:
- Pure logic, algorithms, data transformations
- Edge cases in business rules
- Fast feedback loops during development
- Testing error paths that are hard to trigger in real systems

But unit tests have a fundamental problem: **mocks lie**.

When you mock a database, HTTP client, or file system, you're testing your assumptions about those dependencies — not the actual behavior. You can have 100% unit test coverage and the system is completely broken in production because:

```
# This unit test passes with flying colors
def test_parse_user():
    mock_db = Mock()
    mock_db.query.return_value = {"name": "Alice"}
    result = get_user(mock_db, 1)
    assert result.name == "Alice"  # ✓

# But in production, the actual query returns
# {"name": "Alice", "role": null} and it blows up
```

The real hierarchy is:

```
Unit tests:     fast, cheap, test logic branches
                blind spots: integration, real I/O, serialization

Integration:    test real components together
                catches: actual DB queries, HTTP behavior, serialization
                worth the cost for critical paths

E2E/API tests:  test the full user journey
                catches: things no amount of mocking can reveal
```

The pragmatic approach:

- Pure logic → unit test (no mocks needed, just inputs/outputs)
- I/O-heavy code → integration test (real DB, real HTTP, just isolated environment)
- Critical paths → both

The "mock everything" school leads to tests that pass confidently while the system burns. The real skill is knowing when a mock is adding confidence vs hiding risk.

What unit tests ARE better at: speed, simplicity, isolation. What they're worse at: proving the system actually works.
