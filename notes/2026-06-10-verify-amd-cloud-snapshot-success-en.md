---
audio: false
generated: true
image: false
lang: en
layout: post
title: Verify AMD Cloud Snapshot Success
translated: false
type: note
---

Question: When taking a snapshot in AMD Developer Cloud, how do I verify it actually succeeded before relying on it — so I don't lose work and have to redo setup?

Answer:

The core problem: a snapshot row appearing in the UI does **not** mean the snapshot is restorable. The DigitalOcean-based API (AMD Dev Cloud runs on a DO-derived stack) marks snapshots through states, and only one of them is safe.

Verify by polling the action and the snapshot state — never trust the UI list alone.

```bash
# Set these once
export DO_TOKEN="<API_KEY>"
DROPLET_ID=574444990   # your MI300X droplet

API="https://api.digitalocean.com/v2"
AUTH=(-H "Authorization: Bearer $DO_TOKEN" -H "Content-Type: application/json")
```

Trigger the snapshot and capture the action ID — this is the thing you actually watch:

```bash
ACTION_ID=$(curl -s -X POST "${API}/droplets/${DROPLET_ID}/actions" \
  "${AUTH[@]}" \
  -d '{"type":"snapshot","name":"mi300x-'"$(date +%Y%m%d-%H%M%S)"'"}' \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["action"]["id"])')

echo "action: $ACTION_ID"
```

Poll until the action resolves to `completed` (not `in-progress`, and definitely catch `errored`):

```bash
while true; do
  STATUS=$(curl -s "${API}/actions/${ACTION_ID}" "${AUTH[@]}" \
    | python3 -c 'import sys,json; print(json.load(sys.stdin)["action"]["status"])')
  echo "$(date +%T) -> $STATUS"
  case "$STATUS" in
    completed) echo "✅ snapshot action done"; break ;;
    errored)   echo "❌ snapshot FAILED — do not delete source, rerun"; exit 1 ;;
    *)         sleep 20 ;;
  esac
done
```

The action completing is necessary but still not sufficient. Confirm the snapshot exists, has a non-zero size, and the reported size is sane for a 192GB box (your existing one is ~133GB):

```bash
curl -s "${API}/droplets/${DROPLET_ID}/snapshots" "${AUTH[@]}" \
  | python3 -c '
import sys, json
snaps = json.load(sys.stdin)["snapshots"]
latest = sorted(snaps, key=lambda s: s["created_at"])[-1]
gb = latest["size_gigabytes"]
print(f'\''name={latest["name"]} size={gb}GB regions={latest["regions"]}'\'')
assert gb and gb > 1, "❌ zero/tiny size — snapshot is junk, redo it"
assert latest["regions"], "❌ no region attached — not restorable"
print("✅ snapshot looks restorable")
'
```

One-liner sanity check you can rerun anytime:

```bash
curl -s "${API}/droplets/${DROPLET_ID}/snapshots" "${AUTH[@]}" \
  | python3 -c 'import sys,json;[print(s["name"],s["size_gigabytes"],"GB",s["created_at"]) for s in json.load(sys.stdin)["snapshots"]]'
```

The three gates that mean "safe to tear down and rework later":

1. Action `status == completed` (not just submitted)
2. Snapshot appears in `/snapshots` with `size_gigabytes > 0`
3. `regions` is non-empty (a snapshot with no region can't be used to create a droplet)

A practical gotcha on the MI300X box specifically: snapshots require the droplet to be quiesced. If you have live ROCm processes or large dirty pages in HBM-backed workflows, sync and ideally power off first so the disk image is consistent:

```bash
sync && sync
# optional but safest for a clean image:
# sudo poweroff   # then snapshot the powered-off droplet via API
```

Wrap the whole thing so you never proceed on a false positive:

```bash
snapshot_safe() {
  local id=$1 name=$2
  local aid=$(curl -s -X POST "${API}/droplets/${id}/actions" "${AUTH[@]}" \
    -d "{\"type\":\"snapshot\",\"name\":\"${name}\"}" \
    | python3 -c 'import sys,json;print(json.load(sys.stdin)["action"]["id"])')
  while :; do
    local st=$(curl -s "${API}/actions/${aid}" "${AUTH[@]}" \
      | python3 -c 'import sys,json;print(json.load(sys.stdin)["action"]["status"])')
    [ "$st" = completed ] && break
    [ "$st" = errored ] && { echo "FAILED"; return 1; }
    sleep 20
  done
  curl -s "${API}/droplets/${id}/snapshots" "${AUTH[@]}" \
    | python3 -c 'import sys,json;s=sorted(json.load(sys.stdin)["snapshots"],key=lambda x:x["created_at"])[-1];import os;os._exit(0 if s["size_gigabytes"]>1 and s["regions"] else 1)' \
    && echo "✅ verified" || { echo "❌ unverified"; return 1; }
}
```

Only after `snapshot_safe` returns 0 should you destroy the droplet to stop the ~$2/hr burn.

One caveat: AMD Dev Cloud may not expose the full DigitalOcean public API at `api.digitalocean.com` — it could be a separate endpoint or token scope. Check the actual base URL in their dashboard/docs; if the API isn't reachable, the same logic applies manually: refresh the snapshots list, confirm the size is in the expected ~130GB+ range, and don't tear down until it shows up with a real size.
