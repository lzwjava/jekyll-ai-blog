import os
import re
import yaml
import traceback


def validate_front_matter(file_path):
    print(f"Validating front matter for file: {file_path}")
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    with open(file_path, "r", encoding="utf-8") as infile:
        content = infile.read()

    front_matter_match = re.match(r"---(.*?)---", content, re.DOTALL)
    front_matter = front_matter_match.group(1) if front_matter_match else None

    if not front_matter:
        print(f"No front matter found in {file_path}")
        return False

    if "layout" not in front_matter:
        print(f"Layout key not found in {file_path}")
        return False

    if "title" not in front_matter:
        print(f"Title key not found in {file_path}")
        return False

    if "lang" not in front_matter:
        print(f"Lang key not found in {file_path}")
        return False

    print(f"Front matter is valid for {file_path}")
    return True


def update_front_matter(file_path, translated_flag, lang=None):
    print(f"Starting to process file: {file_path}")
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Reading content from {file_path}")
    with open(file_path, "r", encoding="utf-8") as infile:
        content = infile.read()
        print(f"Successfully read {len(content)} characters from {file_path}")

    print(f"Extracting front matter from {file_path}")
    front_matter_match = re.match(r"---(.*?)---", content, re.DOTALL)
    front_matter = front_matter_match.group(1) if front_matter_match else None
    print(front_matter)

    if not front_matter:
        print(f"No front matter found in {file_path}")
        raise Exception("No front matter found in {file_path}")

    if "layout" not in front_matter:
        print(f"Layout key not found in {file_path}")
        raise Exception(f"Layout key not found in {file_path}")

    if "title" not in front_matter:
        print(f"Title key not found in {file_path}")
        raise Exception(f"Title key not found in {file_path}")

    if "lang" in front_matter:
        print(f"Lang key found in {file_path}")
    else:
        print(f"Lang key not found in {file_path}")
        raise Exception(f"Lang key not found in {file_path}")

    print(f"Front matter found in {file_path}")

    print(f"Loading front matter YAML for {file_path}")
    front_matter_dict = yaml.safe_load(front_matter) if front_matter else {}
    print(f"Current front matter content: {front_matter_dict}")

    print(f"Setting translated flag to {translated_flag} for {file_path}")
    front_matter_dict["translated"] = translated_flag

    if lang:
        print(f"Setting language to {lang} for {file_path}")
        front_matter_dict["lang"] = lang

    print(f"Generating updated front matter for {file_path}")
    updated_front_matter = (
        "---\n" + yaml.dump(front_matter_dict, allow_unicode=True) + "---"
    )
    print(f"Updated front matter content: {updated_front_matter}")

    print(f"Creating updated content for {file_path}")
    updated_content = (
        updated_front_matter + content[len(front_matter_match.group(0)) :]
        if front_matter_match
        else updated_front_matter + content
    )

    print(f"Writing updated content to {file_path}")
    with open(file_path, "w", encoding="utf-8") as outfile:
        outfile.write(updated_content)
    print(
        f"Successfully updated front matter in {file_path}, translated set to {translated_flag}"
    )


def main():
    posts_dir = "_posts"
    languages = ["ja", "es", "hi", "zh", "en", "fr", "de", "ar", "hant"]
    original_dir = "original"

    if not os.path.exists(original_dir):
        print(f"Directory not found: {original_dir}")
        return

    # First, validate all files
    files_to_process = []
    invalid_files = []
    for lang_dir in languages:
        target_dir = os.path.join(posts_dir, lang_dir)
        if not os.path.exists(target_dir):
            print(f"Directory not found: {target_dir}")
            continue
        print(f"Checking files in {target_dir}")
        for filename in os.listdir(target_dir):
            if filename.endswith(".md"):
                file_path = os.path.join(target_dir, filename)
                if not validate_front_matter(file_path):
                    invalid_files.append(file_path)
                else:
                    files_to_process.append((file_path, True, lang_dir))

    print(f"Checking files in {original_dir}")
    for filename in os.listdir(original_dir):
        if filename.endswith(".md"):
            if filename.endswith("-en.md"):
                file_path = os.path.join(posts_dir, "en", filename)
                if not validate_front_matter(file_path):
                    invalid_files.append(file_path)
                else:
                    files_to_process.append((file_path, False, "en"))
            elif filename.endswith("-zh.md"):
                file_path = os.path.join(posts_dir, "zh", filename)
                if not validate_front_matter(file_path):
                    invalid_files.append(file_path)
                else:
                    files_to_process.append((file_path, False, "zh"))
            else:
                print(
                    f"  Skipping file {filename} as it does not end with -en.md or -zh.md"
                )

    if invalid_files:
        print("The following files have invalid front matter:")
        for file_path in invalid_files:
            print(f"  - {file_path}")
        raise Exception("Front matter validation failed for one or more files.")

    # Now, process the files
    for file_path, translated_flag, lang in files_to_process:
        update_front_matter(file_path, translated_flag, lang)


main()
