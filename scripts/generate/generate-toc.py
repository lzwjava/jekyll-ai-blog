import os
import re
from datetime import datetime

current_date = datetime.today().strftime("%Y-%m-%d")

english_titles = []
chinese_titles = []

for file_name in os.listdir("_posts"):
    if file_name.endswith(".md"):
        file_path = os.path.join("_posts", file_name)

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        match = re.search(r'title:\s+"(.*?)"', content)
        if match:
            title = match.group(1)
        else:
            continue

        file_name_without_ext = file_name.replace(".md", "")
        file_name_parts = file_name_without_ext.split("-")

        if len(file_name_parts) > 3:
            file_name_parts = file_name_parts[3:]

        if file_name_parts[-1] in ["en", "zh"]:
            file_name_parts.pop()

        title_slug = "-".join(file_name_parts)

        post_date = file_name[:10]

        if "-en" in file_name:
            english_titles.append((title, title_slug, post_date))
        elif "-zh" in file_name:
            chinese_titles.append((title, title_slug, post_date))

# Sorting: first by date descending, second by title alphabetically ascending
english_titles.sort(
    key=lambda x: (datetime.strptime(x[2], "%Y-%m-%d"), x[0]), reverse=True
)
chinese_titles.sort(
    key=lambda x: (datetime.strptime(x[2], "%Y-%m-%d"), x[0]), reverse=True
)

english_content = ""
for title, slug, _ in english_titles:
    link = f"* [{title}](../{slug}-en)"
    english_content += f"{link}\n"

chinese_content = ""
for title, slug, _ in chinese_titles:
    link = f"* [{title}](../{slug}-zh)"
    chinese_content += f"{link}\n"

english_post_filename = f"_posts/{current_date}-posts-en.md"
chinese_post_filename = f"_posts/{current_date}-posts-zh.md"

with open(english_post_filename, "w", encoding="utf-8") as file:
    file.write('---\nlayout: post\ntitle: "English Posts"\naudio: true\n---\n\n')
    file.write(english_content)

with open(chinese_post_filename, "w", encoding="utf-8") as file:
    file.write('---\nlayout: post\ntitle: "中文文章"\naudio: true\n---\n\n')
    file.write(chinese_content)

print(f"Posts created: {english_post_filename}, {chinese_post_filename}")
