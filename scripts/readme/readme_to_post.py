import os
import argparse


def extract_title(content):
    title = content.splitlines()[0]
    if title.startswith("## "):
        title = title[3:]
    elif title.startswith("# "):
        title = title[2:]
    return title.strip()


def post_front(title):
    return f"""---
audio: false
lang: en
layout: post
title: {title}
translated: false
---
"""


def create_post_from_readme(project_dir, target_post):
    """
    Creates a new markdown post from a README file.

    Args:
        project_dir (str): The root directory of the project.
        target_post (str): The target directory for the new post.
    """
    readme_path = os.path.join(project_dir, "README.md")
    if not os.path.exists(readme_path):
        print(f"Error: README file not found at {readme_path}")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    title = extract_title(readme_content)
    post_frontmatter = post_front(title)

    repo_name = os.path.basename(os.path.abspath(project_dir))
    github_link = f"\nThis is the README.md from github project [https://github.com/lzwjava/{repo_name}](https://github.com/lzwjava/{repo_name}).\n\n---\n\n"
    post_content = post_frontmatter + github_link + readme_content

    # Create a new filename based on the title
    new_filepath = os.path.join(".", "original", target_post)

    if os.path.exists(new_filepath):
        print(f"Skipping creation of {new_filepath} as it already exists.")
        return

    # Write the new post file
    with open(new_filepath, "w", encoding="utf-8") as f:
        f.write(post_content)

    print(f"Created new post at: {new_filepath}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a new post from a README file."
    )
    parser.add_argument(
        "project_dir", type=str, help="The root directory of the project."
    )
    parser.add_argument(
        "target_post", type=str, help="The target directory for the new post."
    )
    args = parser.parse_args()

    create_post_from_readme(args.project_dir, args.target_post)
