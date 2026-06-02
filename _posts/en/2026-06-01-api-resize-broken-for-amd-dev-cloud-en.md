---
audio: false
generated: true
image: false
lang: en
layout: post
title: API Resize Broken for AMD Dev Cloud
translated: false
type: note
---

Here's what I found after thorough testing:

**The resize action is broken at the API level for your AMD Dev Cloud (partner) account.** This is not a code bug or a wrong size value.

Evidence:

- Tested sizes 101, 110, 125, 128, 150, 200, 250, 256, 300, 400, 500, 512, 1024 — ALL return `422 "invalid size specified"`
- Created a brand-new 100 GiB volume in atl1 — resize still fails
- Created a volume in nyc1 — resize still fails
- Tried with/without `droplet_id`, with/without `region`, detached/attached — all fail
- The API correctly parses the request (rejects float/string with 400), but rejects every integer size

**Root cause:** Your token (`dop_v1_...`) is a DigitalOcean Partner Cloud token (AMD Dev Cloud). The standard DO API's `POST /v2/volumes/{id}/actions` resize endpoint appears to be **not supported for partner/GPU volumes**. The web UI likely uses a different internal API or has elevated permissions that bypass this restriction.

**Options:**

1. Use the web UI — enter `101` or higher in the modal (it should work from the UI even though the CLI fails)
2. Contact AMD Dev Cloud support to ask about CLI/API volume resize for GPU Droplets
3. Create a new larger volume, copy data over, swap attachments

Side note: **rotate your API token** — you shared it in this chat. Go to your AMD Dev Cloud / DigitalOcean dashboard and generate a new one.
