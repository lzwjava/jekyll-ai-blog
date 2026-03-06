import argparse
import os
import re

def parse_front_matter(file_content):
    match = re.search(r'---\n(.*?)\n---', file_content, re.DOTALL)
    if match:
        front_matter_str = match.group(1)
        front_matter = {}
        for line in front_matter_str.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                front_matter[key.strip()] = value.strip()
        return front_matter, match.end()
    return {}, 0

def update_front_matter(file_content, new_front_matter):
    front_matter, end_index = parse_front_matter(file_content)
    if front_matter:
        new_front_matter_str = ''
        for key, value in new_front_matter.items():
            new_front_matter_str += f'{key}: {value}\n'
        return f'---\n{new_front_matter_str}---{file_content[end_index:]}'
    return file_content

def extract_url_from_filename(filename):
    # Remove date and .md extension
    match = re.match(r'\d{4}-\d{2}-\d{2}-(.*?)\.md', filename)
    if match:
        return match.group(1)
    return None

def find_and_replace_hyperlinks(directory, old_url_slug, old_title, new_title):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                updated_content = content

                # Regex to find [old_title](old_url_slug) or [old_title](old_url_slug/something)
                # and replace link text with new_title
                # updated_content = re.sub(rf'\[{re.escape(old_title)}\]\({re.escape(old_url_slug)}([^)]*?)\)',
                #                          f'[{new_title}]({old_url_slug}\1)', updated_content)

                # Generic regex for links with 'old_url_slug' in them, to change perceived link text
                # This regex captures any link text that points to old_url_slug
                # and replaces it with the new_title
                updated_content = re.sub(rf'\[(.*?)\]\({re.escape(old_url_slug)}([^)]*?)\)',
                                         f'[{new_title}]({old_url_slug}\2)', updated_content)

                if updated_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f'Updated link text in: {file_path}')

def change_post_title(file_path, new_title):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    front_matter, _ = parse_front_matter(content)
    if 'title' in front_matter:
        old_title = front_matter['title']
        front_matter['title'] = new_title
        updated_content = update_front_matter(content, front_matter)

        # Get old URL slug from filename (e.g., "change-habit-en" from "2025-07-28-change-habit-en.md")
        filename = os.path.basename(file_path)
        old_url_slug = extract_url_from_filename(filename)

        # Generate new URL slug from new_title. This is used for updating hyperlinks.
        # The file itself will NOT be renamed. Its slug will remain old_url_slug.
        new_url_slug = old_url_slug # The slug remains the same as the filename won't change.

        # Pass old_title to find_and_replace_hyperlinks to update the link text
        if old_url_slug: # Ensure we have a valid slug to search for
            find_and_replace_hyperlinks('original', old_url_slug, old_title, new_title)


        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f'Updated title in {os.path.basename(file_path)} from "{old_title}" to "{new_title}"')
    else:
        print(f'No title found in front matter of {file_path}')

def main():
    parser = argparse.ArgumentParser(description="Change the title of a Markdown post and update related files.")
    parser.add_argument("file_path", help="The path to the Markdown file.")
    parser.add_argument("new_title", help="The new title for the post.")

    args = parser.parse_args()
    change_post_title(args.file_path, args.new_title)

if __name__ == "__main__":
    main()
