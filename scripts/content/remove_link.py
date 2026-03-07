import os
from datetime import date
import yaml


def remove_link_from_frontmatter(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    try:
        # Attempt to split frontmatter from content
        parts = content.split("---", 2)
        if len(parts) < 3:
            print(f"Skipped: {file_path} (no frontmatter)")
            return

        frontmatter_str = parts[1]
        body = parts[2]

        frontmatter = yaml.safe_load(frontmatter_str)
        if frontmatter and "link" in frontmatter:
            del frontmatter["link"]
            modified_frontmatter_str = yaml.dump(frontmatter, sort_keys=False)
            modified_content = f"---\n{modified_frontmatter_str}---{body}"
        else:
            modified_content = content
    except yaml.YAMLError as e:
        print(f"Skipped: {file_path} (YAML error: {e})")
        return
    except Exception as e:
        print(f"Skipped: {file_path} (Error processing file: {e})")
        return

    with open(file_path, "w") as f:
        f.write(modified_content)


if __name__ == "__main__":
    target_dir = "original"
    today = date.today()
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)

                # Extract date from filename (assuming format like YYYY-MM-DD-title.md)
                try:
                    date_str = file[:10]
                    file_date = date.fromisoformat(date_str)
                    if file_date == today:
                        remove_link_from_frontmatter(file_path)
                        print(f"Processed: {file_path}")
                except (ValueError, IndexError):
                    # If date extraction fails, skip the file
                    print(
                        f"Skipped: {file_path} (date not in filename or invalid format)"
                    )
