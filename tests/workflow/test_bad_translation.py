import argparse
import os
import sys
import unittest


FORBIDDEN_PHRASES = []
TARGET_DIR = os.path.join("_posts", "zh")
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def scan_chinese_posts_for_forbidden_phrase():
    violations = []
    if not os.path.exists(TARGET_DIR):
        return violations

    for filename in os.listdir(TARGET_DIR):
        if not filename.endswith(".md"):
            continue
        path = os.path.join(TARGET_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                for idx, line in enumerate(f, start=1):
                    for phrase in FORBIDDEN_PHRASES:
                        if phrase in line:
                            violations.append(
                                {
                                    "file": path,
                                    "line_number": idx,
                                    "line": line.rstrip("\n"),
                                    "phrase": phrase,
                                }
                            )
        except Exception as e:
            violations.append(
                {
                    "file": path,
                    "line_number": 0,
                    "line": f"<error reading file: {e}>",
                    "phrase": "<io>",
                }
            )
    return violations


class TestBadTranslation(unittest.TestCase):
    def test_no_forbidden_phrase_in_zh_posts(self):
        violations = scan_chinese_posts_for_forbidden_phrase()
        if violations:
            details = "\n".join(
                [
                    f"{v['file']}:{v['line_number']} [contains '{v['phrase']}']: {v['line']}"
                    for v in violations
                ]
            )
            phrases = ", ".join(FORBIDDEN_PHRASES)
            self.fail(f"Found forbidden phrases in Chinese posts: {phrases}\n{details}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Retranslate posts containing forbidden phrases.",
    )
    parser.add_argument(
        "--model",
        default="deepseek-v3.1",
        help="Model to use when re-translating posts in fix mode.",
    )
    args, remaining = parser.parse_known_args()

    if args.fix:
        violations = scan_chinese_posts_for_forbidden_phrase()
        unique_files = sorted({v["file"] for v in violations})
        if unique_files:
            translation_module_path = os.path.join(REPO_ROOT, "scripts", "translation")
            if translation_module_path not in sys.path:
                sys.path.insert(0, translation_module_path)
            from markdown_translate_client import translate_markdown_file

            for translated_path in unique_files:
                filename = os.path.basename(translated_path)
                if not filename.endswith("-zh.md"):
                    print(f"Skipping {translated_path}: unsupported filename")
                    continue
                original_filename = filename.replace("-zh.md", "-en.md")
                original_path = os.path.join(REPO_ROOT, "original", original_filename)
                if not os.path.exists(original_path):
                    print(
                        f"Cannot retranslate {translated_path}: missing original file {original_path}"
                    )
                    continue
                print(
                    f"Retranslating {original_path} -> {translated_path} using model {args.model}"
                )
                translate_markdown_file(
                    original_path,
                    translated_path,
                    "zh",
                    model=args.model,
                )
        else:
            print("No forbidden phrases found; nothing to fix.")

    sys.argv = [sys.argv[0]] + remaining
    unittest.main()
