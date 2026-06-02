---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: Jekyll构建缺少自动清理功能
translated: true
type: note
---

Jekyll 本身没有 `--replace` 或 `--refresh` 标志。每次运行 `jekyll build` 都会将生成的文件写入（或覆盖）到指定的 `--destination` 目录，但它**不会自动删除源目录中已不存在**的旧文件。这意味着残留文件可能会继续存在。

如果需要干净的构建输出，必须在运行 `jekyll build` 前手动清空目标目录。两种常见方案：

**1. 在脚本中手动清理**
调用 `jekyll build` 前清空目标目录：

```python
import shutil

def run_jekyll(destination: str, extra_args: list[str]) -> int:
    # 删除旧文件
    dest_path = Path(destination)
    if dest_path.exists():
        shutil.rmtree(dest_path)

    command = [
        "jekyll",
        "build",
        "--destination",
        destination,
        *extra_args,
    ]
    completed = subprocess.run(command, check=False)
    return completed.returncode
```

**2. 使用 Jekyll 默认的 `_site` 目录**
如果让 Jekyll 使用项目根目录下的默认 `_site` 目录（而非自定义 `--destination`），可通过 `jekyll clean` 在重建前清理输出：

```bash
jekyll clean && jekyll build
```

但 `jekyll clean` 仅识别 `_site` 目录，不适用于自定义文件夹。

---

结论：

* 没有内置的 `--replace` 参数
* 如果使用自定义目标目录（如脚本中所示），需要构建前显式删除该目录以确保输出全新

是否需要我为您的脚本添加 `--clean` 选项（类似 `jekyll clean`），实现构建前自动清空目标目录的功能？
