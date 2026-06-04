---
audio: false
generated: true
image: false
lang: en
layout: post
title: Model Migration and Token Query
translated: false
type: note
---

Done. Here's what happened:

```
Remote switched:  github.com/lzwjava/zz  ->  huggingface.co/lzwjava/zz
Fast-forward merge: 108bc6b..9db74d9 (9 files, +2593 lines)

New content pulled:
  - 760M model inference samples (code, facts, story, ai_history)
  - 760M training logs from MI300X run
  - inference quality audit
  - FineWeb download script for AMD/US environment
```

For pushing, you'll need HF auth. Run this when ready:

```
huggingface-cli login
```

Or if you want to use a token:

```
git config --global credential.helper store
echo "https://lzwjava:YOUR_HF_TOKEN@huggingface.co" >> ~/.git-credentials
```

Now -- want me to dig into the zz repo and figure out how to get more tokens for nanochat training?
