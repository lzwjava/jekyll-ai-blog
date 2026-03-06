import copy
import yaml
import os
import re

from translate_client import translate_text


def translate_front_matter(
    front_matter, target_language, input_file, model="deepseek-v3.2"
):
    print(f"  Translating front matter for: {input_file}")
    if not front_matter:
        print(f"  No front matter found for: {input_file}")
        return "", None, None
    try:
        front_matter_dict = {}
        if front_matter:
            front_matter_dict = yaml.safe_load(front_matter)
            print(f"  Front matter after safe_load: {front_matter_dict}")

        original_lang = front_matter_dict.get("lang", "en")

        front_matter_dict_copy = copy.deepcopy(front_matter_dict)

        # Extract prompt from front matter, if it exists
        front_matter_prompt = front_matter_dict_copy.get("prompt", None)

        if "title" in front_matter_dict_copy:
            print(f"  Translating title: {front_matter_dict_copy['title']}")
            translated_title = translate_text(
                front_matter_dict_copy["title"],
                target_language,
                type="title",
                model=model,
                front_matter_prompt=front_matter_prompt,
                original_lang=original_lang,
                source_file=input_file,
            )
            if translated_title:
                translated_title = translated_title.strip()
                front_matter_dict_copy["title"] = translated_title
                print(f"  Translated title to: {translated_title}")
            else:
                print(f"  Title translation failed for: {input_file}")
        else:
            print(f"  Skipping title translation for {input_file} to {target_language}")

        front_matter_dict_copy["lang"] = target_language
        front_matter_dict_copy["translated"] = target_language != original_lang

        front_matter_dict_copy["audio"] = False

        result = "---\n" + yaml.dump(front_matter_dict_copy, allow_unicode=True) + "---"
        print(f"  Front matter translation complete for: {input_file}")
        return result, front_matter_prompt, original_lang
    except yaml.YAMLError as e:
        print(f"  Error parsing front matter: {e}")
        return front_matter, None, None


def translate_markdown_file(
    input_file, output_file, target_language, model="deepseek-v3.2"
):
    print(f"  Processing file: {input_file}")
    try:
        with open(input_file, "r", encoding="utf-8") as infile:
            content = infile.read()

        front_matter_match = re.match(r"---\n(.*?)\n---", content, re.DOTALL)
        if front_matter_match:
            front_matter = front_matter_match.group(1)
        else:
            raise Exception("No front matter found in markdown file")
        content_without_front_matter = (
            content[len(front_matter_match.group(0)) :]
            if front_matter_match
            else content
        )

        print(f"front_matter_match: {front_matter_match}")
        print(f"front_matter: {front_matter}")

        translated_front_matter, front_matter_prompt, original_lang = (
            translate_front_matter(
                front_matter, target_language, input_file, model=model
            )
        )

        translated_content = translate_text(
            content_without_front_matter,
            target_language,
            model=model,
            front_matter_prompt=front_matter_prompt,
            original_lang=original_lang,
            source_file=input_file,
        )
        if translated_content:
            translated_content = (
                translated_front_matter + "\n\n" + translated_content.strip()
            )
        else:
            raise Exception(f"Translation failed for: {input_file}")

        if os.path.exists(output_file):
            os.remove(output_file)

        with open(output_file, "w", encoding="utf-8") as outfile:
            outfile.write(translated_content)
        print(f"  Finished processing file: {output_file}")
    except Exception as e:
        print(
            f"  Error processing file {input_file} target language{target_language}: {e}"
        )


if __name__ == "__main__":
    translate_markdown_file(
        input_file="original/2025-07-18-japanese-essay-ja.md",
        output_file="test-ja.md",
        target_language="ja",
        model="deepseek-v3.2",
    )
