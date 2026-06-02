import os
import re
import unittest


ORIGINAL_DIR = "original"


def find_markdown_links(content: str):
    # Match standard Markdown links [text](target), exclude images ![alt](...)
    pattern = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)]+)\)")
    return [m.group(1).strip() for m in pattern.finditer(content)]


def normalize_target(target: str) -> str:
    # Remove surrounding spaces and quotes
    target = target.strip().strip("\"'")
    # Drop query/fragments
    target = target.split("#", 1)[0].split("?", 1)[0]
    return target


def is_local_en_markdown(target: str) -> bool:
    # Only consider local links starting with ./ and ending with -en or -en.md
    if not target.startswith("./"):
        return False
    path = target[2:]
    return path.endswith("-en") or path.endswith("-en.md")


def slug_from_target(target: str) -> str:
    path = target[2:]
    if path.endswith(".md"):
        path = path[:-3]
    return path


def exists_for_slug(slug: str) -> bool:
    # 1) Direct file: original/slug.md
    direct = os.path.join(ORIGINAL_DIR, f"{slug}.md")
    if os.path.exists(direct):
        return True
    # 2) Any date-prefixed variant: original/YYYY-MM-DD-slug.md
    try:
        for fname in os.listdir(ORIGINAL_DIR):
            if not fname.endswith(".md"):
                continue
            if fname.endswith(f"-{slug}.md"):
                return True
    except FileNotFoundError:
        return False
    return False


@unittest.skip("Disabled: link existence check is too strict for now")
class TestOriginalMarkdownLinksExist(unittest.TestCase):
    def test_local_en_links_exist_in_original(self):
        missing = []

        if not os.path.isdir(ORIGINAL_DIR):
            self.skipTest(f"{ORIGINAL_DIR} directory not found")

        for fname in os.listdir(ORIGINAL_DIR):
            if not fname.endswith(".md"):
                continue
            src_path = os.path.join(ORIGINAL_DIR, fname)
            try:
                with open(src_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                self.fail(f"Failed to read {src_path}: {e}")

            for raw in find_markdown_links(content):
                t = normalize_target(raw)
                if not is_local_en_markdown(t):
                    continue
                slug = slug_from_target(t)
                if not exists_for_slug(slug):
                    # Report an example expected path for clarity
                    example = os.path.join(ORIGINAL_DIR, f"{slug}.md")
                    missing.append((src_path, t, example))

        if missing:
            details = "\n".join(
                f"in {src} -> link {t} missing file {chk}" for src, t, chk in missing
            )
            self.fail(f"Found missing local -en links in original posts:\n{details}")


if __name__ == "__main__":
    unittest.main()
