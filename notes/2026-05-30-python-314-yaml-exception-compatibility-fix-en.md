---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python 3.14 YAML Exception Compatibility Fix
translated: false
type: note
---

Test run complete. Here's the summary:

```
Results: 339 passed, 1 failed (out of 340 tests)
Time:    4.25 seconds
```

The single failure:

```
FAILED tests/cloud/test_ec2.py::TestGetEc2Instances::test_unexpected_error
```

**Root cause:** In `ww/cloud/ec2.py:25`, the `except yaml.YAMLError` clause triggers a `TypeError` on Python 3.14 — `yaml.YAMLError` doesn't inherit from `BaseException` on this version. The test mocks `subprocess.run` to raise `RuntimeError("unexpected")`, which isn't caught by the existing `except subprocess.CalledProcessError` or `except yaml.YAMLError` clauses, and the latter itself blows up.

This is a Python 3.14 compatibility issue with the YAML library's exception hierarchy. A quick fix would be to either:

1. Add a bare `except Exception` clause after the existing ones, or
2. Bump `pyyaml` to a version compatible with 3.14

Everything else (339 tests) passes cleanly.
