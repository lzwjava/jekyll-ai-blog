---
audio: false
generated: true
image: false
lang: en
layout: post
title: Implementing Adjustable Compression Levels
translated: false
type: note
---

Now I have a complete picture. Here's what the code tells us:

**Current `/compress` behavior:**

1. **Already supports focus topics**: `/compress database schema` guides the summarizer to preserve info related to that topic while being more aggressive about everything else.

2. **Running `/compress` twice works, but for iterative updates, not more aggressive compression**:
   - First pass: compresses middle turns into a summary
   - Second pass: finds the previous summary in the head, then summarizes any NEW middle content that accumulated since the first pass
   - If you run it twice without new messages between them, the second pass is likely a no-op (already compressed)

3. **The code explicitly warns about repeated compression** (line 447-450):
   ```python
   if _cc >= 2:
       agent._vprint(
           f"{agent.log_prefix}⚠️  Session compressed {_cc} times — "
           f"accuracy may degrade. Consider /new to start fresh.",
       )
   ```

4. **Compression aggressiveness is controlled by these parameters** (config.yaml):
   ```yaml
   compression:
     threshold: 0.50      # when to auto-compress (50% of context)
     target_ratio: 0.20   # fraction of threshold to preserve as recent tail
     protect_last_n: 20   # minimum recent messages to keep uncompressed
     protect_first_n: 3   # non-system head messages always preserved
   ```

**So what would high/medium/low do?**

- **Low** (current defaults): gentle compression, keeps 20% of threshold as tail, 20 recent messages protected
- **Medium**: lower `target_ratio` (e.g., 0.15), fewer protected tail messages (e.g., 15)
- **High**: very low `target_ratio` (e.g., 0.10), minimal tail protection (e.g., 10 messages), fewer protected head messages (e.g., 1)

**Running `/compress` twice vs. high/medium/low:**

Running `/compress` twice is NOT the same as "high" compression. The second pass just updates the summary with new content—it doesn't compress the existing summary further.

If you want more aggressive compression in a single pass, you need the high/medium/low parameters. The `/compress <focus>` feature already provides a way to be more aggressive about non-focused content, but it's topic-specific rather than a general aggressiveness level.

**Recommendation:**

Adding `/compress high` or `/compress low` would be genuinely useful. The implementation would be straightforward—just temporarily override the compressor's `target_ratio`, `protect_last_n`, and `protect_first_n` for that single compression call.

Want me to implement this feature?