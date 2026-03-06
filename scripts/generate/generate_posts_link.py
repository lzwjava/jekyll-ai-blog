import os
from typing import List, Tuple


def _parse_post_filename(filename: str) -> Tuple[int, str]:
    """Extract sortable date (yyyymmdd int) and slug from a post filename.

    Expected pattern: YYYY-MM-DD-<slug>.md
    Returns (date_int, slug). If parsing fails, date_int=0, slug without extension.
    """
    name = filename.rsplit(".", 1)[0]
    parts = name.split("-")
    if len(parts) >= 4 and all(p.isdigit() for p in parts[:3]):
        y, m, d = parts[:3]
        slug = "-".join(parts[3:])
        try:
            date_int = int(f"{int(y):04d}{int(m):02d}{int(d):02d}")
        except Exception:
            date_int = 0
        return date_int, slug
    # Fallbacks
    return 0, name


def generate_posts_links() -> None:
    """Generate a posts index from '_posts/en/' into 'original/2025-09-14-posts-en.md'.

    - Scans only '_posts/en/'
    - Reads front matter to get the title
    - Builds links like '* [Title](/slug)'
    - Sorts by date descending (from filename)
    """
    posts_dir = "_posts/en"
    target_path = os.path.join("original", "2025-09-14-posts-en.md")

    try:
        files = [
            f
            for f in os.listdir(posts_dir)
            if f.endswith(".md") and not f.startswith(".")
        ]
    except Exception as e:
        print(f"Failed to list posts in {posts_dir}: {e}")
        return

    print(f"Found {len(files)} post files in {posts_dir}")

    items: List[Tuple[int, str, str]] = []  # (date_int, filename, link)
    for fname in files:
        fpath = os.path.join(posts_dir, fname)
        try:
            # Lightweight front matter title extraction (no external deps)
            title = fname.rsplit(".", 1)[0]
            with open(fpath, "r", encoding="utf-8") as f:
                first = f.readline().strip()
                if first == "---":
                    # Read front matter until closing '---'
                    for line in f:
                        s = line.strip()
                        if s == "---":
                            break
                        if s.lower().startswith("title:"):
                            # Extract value after first ':' and strip quotes/spaces
                            val = line.split(":", 1)[1].strip()
                            if (
                                val.startswith(("'", '"'))
                                and val.endswith(("'", '"'))
                                and len(val) >= 2
                            ):
                                val = val[1:-1]
                            title = val or title
                            # Keep scanning in case of multiple, last wins
            date_int, slug = _parse_post_filename(fname)
            link = f"* [{title}](/{slug})"
            items.append((date_int, fname, link))
            print(f"  Parsed: title='{title}', slug='{slug}', date={date_int}")
        except Exception as e:
            print(f"Error processing {fname}: {e}")

    # Sort: newest first, then filename asc
    items.sort(key=lambda x: (-x[0], x[1]))
    links = [it[2] for it in items]

    content = f"""---
audio: false
lang: en
layout: post
title: Blog Posts
translated: false
generated: false
image: false
---

Here are all blog posts on this site.

{chr(10).join(links)}
"""

    try:
        with open(target_path, "w", encoding="utf-8") as md:
            md.write(content)
        print(f"Updated {target_path}")
    except Exception as e:
        print(f"Error updating {target_path}: {e}")


if __name__ == "__main__":
    generate_posts_links()
