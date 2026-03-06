import os
import re

dirs = [
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "notes")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "_posts/en")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "_posts/zh")),
]


def count_exam_options(content):
    # Count occurrences of " A.", " B.", etc. (case insensitive, word boundary)
    pattern = r"\b([A-D])\.\s"
    return len(re.findall(pattern, content, re.IGNORECASE))


def fix_exam_options(content):
    # Replace " A." -> "- A.", etc. Preserve leading whitespace, assume line start
    pattern = r"^(\s*)([A-D])\.\s"
    replacement = r"\1- \2. "
    return re.sub(pattern, replacement, content, flags=re.MULTILINE)


fixed_count = 0
for dir_path in dirs:
    if not os.path.exists(dir_path):
        continue
    print(f"Processing directory: {dir_path}")
    for filename in os.listdir(dir_path):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(dir_path, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        option_count = count_exam_options(content)
        if option_count > 10:
            new_content = fix_exam_options(content)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Fixed {filename} ({option_count} options)")
            fixed_count += 1

print(f"Fixed {fixed_count} files across all directories.")
