---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 批处理 Fineweb 数据集切片
translated: true
type: note
---

还有 59GB 剩余空间。每个 shard 循环（下载 2GB → 解压约 2.6GB → 删除 parquet）峰值需要约 2.6GB。你可以一次性运行剩余的所有 16 个 shards，但这将耗费数小时（匿名状态下的 rate limit 约为 1GB/hr = 约 32 小时）。

更安全的方法是分批处理，每批 4 个。命令如下：

**Shards 5-8（先运行这个）：**

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

完成后，依次为 **shards 9-12**、**13-16**、**17-20** 运行——只需修改 range 即可：

```bash
# Batch 3:
range(9, 13)

# Batch 4:
range(13, 17)

# Batch 5:
range(17, 21)
```

或者，如果你想一次性提交并在夜间自动运行（修改为 `range(5, 21)`），我可以为你启动。
