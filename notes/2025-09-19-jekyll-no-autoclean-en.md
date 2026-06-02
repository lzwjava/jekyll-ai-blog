---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Jekyll Build Lacks Auto-Clean Feature
translated: false
type: note
---

Jekyll itself doesn’t have a `--replace` or `--refresh` flag. Each `jekyll build` run will write (or overwrite) the generated files into the `--destination` folder you specify, but it **doesn’t automatically remove old files** that no longer exist in your source. That means stale files can remain.

If you want a clean build output, you need to clear the destination directory yourself before running `jekyll build`. Two common approaches:

**1. Manual clean-up in your script**
Before calling `jekyll build`, wipe the destination directory:

```python
import shutil

def run_jekyll(destination: str, extra_args: list[str]) -> int:
    # Remove old files
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

**2. Use Jekyll’s own `_site`**
If you let Jekyll use the default `_site` under your project root (instead of a custom `--destination`), `jekyll clean` is available to purge the output before rebuilding:

```bash
jekyll clean && jekyll build
```

But `jekyll clean` only knows about `_site`, not a custom folder.

---

So:

* There is no `--replace` built-in.
* If you’re using a custom destination (like in your script), you should explicitly delete it before building if you want a fresh output.

Would you like me to adjust your script so it has a `--clean` option (like `jekyll clean`) that automatically clears the destination before building?
