---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FineWeb 数据下载与提取脚本
translated: true
type: note
---

这是该命令 — 请将其粘贴到您的 SSH 会话中：

```bash
cd /root/zz && nohup python3 -c "
import urllib.request, pyarrow.parquet as pq, gc, os

shards = [f'000_000{i:02d}.parquet' for i in range(5, 21)]
base = 'https://huggingface.co/datasets/HuggingFaceFW/fineweb/resolve/main/data/CC-MAIN-2013-20'
os.makedirs('fineweb_parquet', exist_ok=True)

log = open('download_log.txt', 'a', buffering=1)
total = 0

def p(msg):
    print(msg, flush=True)
    log.write(msg + '\n')
    log.flush()

p('Starting shards 5-20')

with open('fineweb_extracted_all.txt', 'a', encoding='utf-8') as out:
    for shard in shards:
        p(f'=== {shard} ===')
        try:
            url = f'{base}/{shard}?download=true'
            dest = f'fineweb_parquet/{shard}'
            urllib.request.urlretrieve(url, dest)
            p(f'Downloaded: {os.path.getsize(dest)/1024/1024:.0f} MB')

            pf = pq.ParquetFile(dest)
            for batch in pf.iter_batches(batch_size=4096):
                text_col = batch.column('text')
                for i in range(len(text_col)):
                    t = str(text_col[i].as_py()).strip()
                    if t:
                        out.write(t + '\n<|endoftext|>\n')
                        total += 1
                if total % 100000 == 0:
                    p(f'Docs: {total:,}')
                    out.flush()

            os.remove(dest)
            gc.collect()
            p(f'Shard done. New docs: {total:,}')
        except Exception as e:
            p(f'ERROR on {shard}: {e}')
            continue

p(f'ALL DONE. Total new docs: {total:,}')
log.close()
" > nohup.out 2>&1 &
echo "Started PID=$!"
```

稍后查看进度：

```bash
tail -f /root/zz/download_log.txt
```
