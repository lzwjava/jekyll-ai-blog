import os
import re
import yaml
import sys


def update_front_matter(file_path, generated_flag):
    try:
        with open(file_path, "r+", encoding="utf-8") as infile:
            content = infile.read()

        front_matter_match = re.match(r"---\n(.*?)\n---", content, re.DOTALL)
        if front_matter_match:
            front_matter = front_matter_match.group(1)
            front_matter_dict = yaml.safe_load(front_matter) if front_matter else {}
        else:
            front_matter_dict = {}

        front_matter_dict["generated"] = generated_flag

        updated_front_matter = (
            "---\n" + yaml.dump(front_matter_dict, allow_unicode=True) + "---"
        )
        updated_content = (
            updated_front_matter + content[len(front_matter_match.group(0)) :]
            if front_matter_match
            else updated_front_matter + content
        )

        with open(file_path, "w", encoding="utf-8") as outfile:
            outfile.write(updated_content)
        print(f"Updated front matter in {file_path} to generated={generated_flag}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")


def process_file_name(file_name_base, generated_flag):
    original_dir = "original"
    posts_dir = "_posts"

    # Process files in original directory
    for filename in os.listdir(original_dir):
        if filename.startswith(file_name_base) and filename.endswith(".md"):
            file_path = os.path.join(original_dir, filename)
            update_front_matter(file_path, generated_flag)

    # Process files in _posts directories
    for lang_dir in os.listdir(posts_dir):
        lang_dir_path = os.path.join(posts_dir, lang_dir)
        if os.path.isdir(lang_dir_path):
            for filename in os.listdir(lang_dir_path):
                if filename.startswith(file_name_base) and filename.endswith(".md"):
                    file_path = os.path.join(lang_dir_path, filename)
                    update_front_matter(file_path, generated_flag)


def main():
    if len(sys.argv) != 3:
        print("Usage: script.py <file_name_base> <generated_flag>")
        return

    file_name_base = sys.argv[1]
    generated_flag_str = sys.argv[2].lower()
    if generated_flag_str == "true":
        generated_flag = True
    elif generated_flag_str == "false":
        generated_flag = False
    else:
        print("generated_flag must be 'true' or 'false'")
        return

    process_file_name(file_name_base, generated_flag)


if __name__ == "__main__":
    main()
