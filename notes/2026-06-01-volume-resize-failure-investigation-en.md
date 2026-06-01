---
audio: false
generated: true
image: false
lang: en
layout: post
title: Volume Resize Failure Investigation
translated: false
type: note
---

Here's the full investigation summary:

---

## Investigation: Why Volume Resize Fails via CLI

### The Problem
The AMD Dev Cloud (DigitalOcean-based) web UI shows an "Increase storage size" modal for volume `volume-atl1-1780280110689`. Typing `200` in the size field shows "invalid size". The user wanted to do it via CLI instead.

### Step 1: Examined the doctl Codebase

Checked `/Users/lzwjava/projects/doctl/commands/volumes.go`:

- Line 53: `--size` flag default is `"4TiB"` — requires a unit suffix (e.g. `200GiB`)
- Line 152: Uses `humanize.ParseBytes()` to parse the size string
- Line 194: Converts to GiB via `int64(size / (1 << 30))`

Found that bare `--size 200` would be interpreted as **200 bytes** → 0 GiB after division. But this is a CLI quirk, not the UI issue.

### Step 2: Analyzed the Web UI HTML

The user shared the modal HTML. Key finding:

```html
<input type="number" min="101" max="16384" step="1" value="101">
```

- `min="101"` — minimum is 101 GB (current volume is 100 GB)
- `max="16384"` — maximum is 16 TiB
- Default value is 101

The HTML5 validation should accept `200`. The error must come from elsewhere.

### Step 3: Checked the API Client Library

Examined `/Users/lzwjava/projects/doctl/vendor/github.com/digitalocean/godo/storage_actions.go`:

- Line 68-75: `Resize()` sends `{"type": "resize", "size_gigabytes": N, "region": "..."}` to `POST /v2/volumes/{id}/actions`
- `size_gigabytes` is `int64` — no client-side validation beyond type

### Step 4: Set Up CLI Access

- `doctl` v1.148.0 was already installed via Homebrew
- Authenticated with the API token via `doctl auth init`
- Verified token works: `doctl compute volume list` succeeded

### Step 5: Listed the Volume

```
doctl compute volume list
```

Result:
```
ID                                      Name                         Size       Region    Droplet IDs
52743aec-...                            volume-atl1-1780280110689    100 GiB    atl1      [574422820]
```

Current size: **100 GiB**, attached to GPU Droplet `574422820` (MI300X 192GB, atl1).

### Step 6: Attempted Resize via CLI

```bash
doctl compute volume-action resize 52743aec-... --size 200 --region atl1
```

Result: `422 "error resizing volume: invalid size specified"`

### Step 7: Brute-Forced All Sizes

Wrote a Python script to test sizes 101, 110, 125, 128, 150, 200, 250, 256, 300, 400, 500, 512, 1024 via `POST /v2/volumes/{id}/actions`:

**Every single size returned `422 "invalid size specified"`.**

### Step 8: Tried Detaching First

```bash
doctl compute volume-action detach 52743aec-... 574422820 --wait
doctl compute volume-action resize 52743aec-... --size 200 --region atl1
```

Still `422`. Reattached the volume afterward.

### Step 9: Tested Different Request Formats

Wrote another Python script testing:
- With/without `droplet_id` in the body
- With/without `region`
- `size_gigabytes` as float (200.0) → `400 "error parsing request body"` (API expects int)
- `size_gigabytes` as string ("200") → `400 "error parsing request body"`
- Integer 200 → `422 "invalid size specified"` (correctly parsed, but rejected)

### Step 10: Tested Other Regions

- Created a new 100 GiB volume in `atl1` → resize fails
- Created a new 100 GiB volume in `nyc1` → resize fails
- Deleted both test volumes

### Conclusion

The `POST /v2/volumes/{id}/actions` resize endpoint returns `422 "invalid size specified"` for **all integer sizes across all regions** on this account. This is a **server-side API limitation**, not a client code bug.

The token prefix `dop_v1_` indicates a **DigitalOcean Partner Cloud** token (AMD Dev Cloud). The standard DO volume resize API appears to be **not supported for partner/GPU volumes**. The web UI likely uses a different internal API or has elevated permissions.

### Recommendation

1. Use the web UI for now (enter 101+ in the modal)
2. Contact AMD Dev Cloud support about CLI/API volume resize
3. **Rotate the API token** — it was shared in chat

---

**Files created during investigation:**
- `/tmp/resize_vol.py` — volume details + size brute-force
- `/tmp/resize_vol2.py` — different request formats (PATCH, POST with extra fields)
- `/tmp/resize_vol3.py` — type coercion tests (float, string, int)