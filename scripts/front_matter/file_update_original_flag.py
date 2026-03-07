import os
import re
from ruamel.yaml import YAML
from io import StringIO


def update_front_matter(file_path, audio_flag=False, lang=None):
    try:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return

        with open(file_path, "r", encoding="utf-8") as infile:
            content = infile.read()

        front_matter_match = re.match(r"---\n(.*?)\n---", content, re.DOTALL)
        front_matter = front_matter_match.group(1) if front_matter_match else None

        if not front_matter:
            print(f"No front matter found in {file_path}")
            raise Exception(f"No front matter found in {file_path}")

        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.indent(mapping=2, sequence=4, offset=2)
        front_matter_dict = yaml.load(front_matter)

        if lang:
            if "lang" in front_matter_dict:
                if front_matter_dict["lang"] != lang:
                    print(
                        f"  Correcting language from {front_matter_dict['lang']} to {lang} in {file_path}"
                    )
                    front_matter_dict["lang"] = lang
            else:
                print(f"  Adding language {lang} in {file_path}")
                front_matter_dict["lang"] = lang

        if audio_flag:
            front_matter_dict["audio"] = True
        else:
            if "audio" not in front_matter_dict:
                front_matter_dict["audio"] = False

        string_stream = StringIO()
        yaml.dump(front_matter_dict, string_stream)
        updated_front_matter = "---\n" + string_stream.getvalue() + "---"
        updated_content = (
            updated_front_matter + content[len(front_matter_match.group(0)) :]
            if front_matter_match
            else updated_front_matter + content
        )

        with open(file_path, "w", encoding="utf-8") as outfile:
            outfile.write(updated_content)
        print(
            f"Updated front matter in {file_path}, audio set to {audio_flag}, lang set to {lang}"
        )

    except Exception as e:
        print(f"Error processing {file_path}: {e}")


def main():
    original_dir = "original"
    audio_dir = "assets/audios"

    if not os.path.exists(original_dir):
        print(f"Directory not found: {original_dir}")
        return

    for filename in os.listdir(original_dir):
        if filename.endswith(".md"):
            file_base = filename[:-3]

            if filename.endswith("-en.md"):
                lang = "en"
            elif filename.endswith("-zh.md"):
                lang = "zh"
            else:
                print(
                    f"Skipping file {filename} as it does not end with -en.md or -zh.md"
                )
                continue

            file_path = os.path.join(original_dir, filename)
            audio_file = f"{file_base}.mp3"
            audio_path = os.path.join(audio_dir, audio_file)

            audio_flag = os.path.exists(audio_path)

            update_front_matter(file_path, audio_flag, lang)


if __name__ == "__main__":
    main()
