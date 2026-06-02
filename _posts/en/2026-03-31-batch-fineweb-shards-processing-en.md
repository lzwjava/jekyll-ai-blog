---
audio: false
generated: true
image: false
lang: en
layout: post
title: Batch Processing Fineweb Dataset Shards
translated: false
type: note
---

59GB free. Each shard cycle (download 2GB → extract ~2.6GB → delete parquet) needs ~2.6GB peak. You can run all 16 remaining shards in one go, but it'll take hours (anonymous rate limit ~1GB/hr = ~32 hours).

Safer to do them in batches of 4. Here's the command:

**Shards 5-8 (run this first):**

```bash
cd /root/zz && python3 -c "
import urllib.request, pyarrow.parquet as pq, gc, os

shards = [f'000_000{i:02d}.parquet' for i in range(5, 9)]
base = 'https://huggingface.co/datasets/HuggingFaceFW/fineweb/resolve/main/data/CC-MAIN-2013-20'
os.makedirs('fineweb_parquet', exist_ok=True)

total = 0
with open('fineweb_extracted_all.txt', 'a', encoding='utf-8') as out:
    for shard in shards:
        print(f'=== {shard} ===', flush=True)
        url = f'{base}/{shard}?download=true'
        dest = f'fineweb_parquet/{shard}'
        urllib.request.urlretrieve(url, dest)
        print(f'Downloaded: {os.path.getsize(dest)/1024/1024:.0f} MB', flush=True)

        pf = pq.ParquetFile(dest)
        for batch in pf.iter_batches(batch_size=4096):
            text_col = batch.column('text')
            for i in range(len(text_col)):
                t = str(text_col[i].as_py()).strip()
                if t:
                    out.write(t + '\n<|endoftext|>\n')
                    total += 1
            if total % 50000 == 0:
                print(f'Docs: {total:,}', flush=True)
                out.flush()

        os.remove(dest)
        gc.collect()
        print(f'Shard done. New docs: {total:,}', flush=True)

print(f'Batch complete. New docs: {total:,}', flush=True)
"
```

After that finishes, run for **shards 9-12**, then **13-16**, then **17-20** — just change the range:

```bash
# Batch 3:
range(9, 13)

# Batch 4:
range(13, 17)

# Batch 5:
range(17, 21)
```

Or if you want to send it all at once and let it rip overnight (change `range(5, 21)`), I can kick it off for you.
