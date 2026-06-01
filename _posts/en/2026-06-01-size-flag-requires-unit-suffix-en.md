---
audio: false
generated: true
image: false
lang: en
layout: post
title: Size Flag Requires Unit Suffix
translated: false
type: note
---

Here's the exact bug. The issue is in `commands/volumes.go`:

**Line 152:** `size, err := humanize.ParseBytes(sizeStr)`
**Line 194:** `createVolume.SizeGigaBytes = int64(size / (1 << 30))`

When you pass `--size 200` (bare number, no unit suffix), here's what happens:

1. `humanize.ParseBytes("200")` splits into num="200" and extra="" (empty suffix)
2. In `bytesSizeTable` (line 49): `""` maps to `Byte` (value 1)
3. Result: `200 * 1 = 200 bytes`
4. Division: `200 / (1 << 30)` = `200 / 1073741824` = **0 GiB** (integer truncation)

So `--size 200` creates a **0 GiB volume** — that's why the API rejects it.

**The fix:** The `--size` flag requires a unit suffix. Use:

```
doctl compute volume create my-vol --size 200GiB --region sgp1
```

Valid suffixes from the `bytesSizeTable`:
- `GiB`, `gib`, `gi`, `g` → GiB (binary)
- `GB`, `gb` → GB (decimal, 1000-based)
- `TiB`, `tib`, `ti`, `t` → TiB
- `TB`, `tb` → TB

The default value on line 53 is `"4TiB"` — confirming the CLI always expects a suffix. This is different from the AMD Dev Cloud web UI which defaults the unit to GiB.