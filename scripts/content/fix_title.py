import os
import re
import time
import argparse
from dotenv import load_dotenv
from openai import OpenAI
import yaml
import concurrent.futures
import frontmatter

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
MODEL_NAME = "deepseek-chat"
INPUT_DIR = "_posts"
MAX_THREADS = 20

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")


def create_translation_prompt(target_language):
    if target_language == "ja":
        return "You are a professional translator. You are translating a markdown file for a Jekyll blog post. Translate the following text to Japanese. Do not translate English names. Be careful about code blocks, if not sure, just do not change."
    elif target_language == "es":
        return "You are a professional translator. You are translating a markdown file for a Jekyll blog post. Translate the following text to Spanish. Do not translate English names. Be careful about code blocks, if not sure, just do not change."
    elif target_language == "hi":
        return "You are a professional translator. You are translating a markdown file for a Jekyll blog post. Translate the following text to Hindi. Do not translate English names. Be careful about code blocks, if not sure, just do not change."
    else:
        return f"You are a professional translator. You are translating a markdown file for a Jekyll blog post. Translate the following text to {target_language}. Do not translate English names. Be careful about code blocks, if not sure, just do not change."


def translate_text(text, target_language):
    print(f"  Translating text: {text[:50]}...")
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": create_translation_prompt(target_language),
                },
                {"role": "user", "content": text},
            ],
            stream=False,
        )
        if response and response.choices:
            print(f"  Translation successful.")
            return response.choices[0].message.content
        else:
            print(f"  Translation failed.")
            return None
    except Exception as e:
        print(f"  Translation failed with error: {e}")
        return None


def translate_front_matter(front_matter, target_language):
    if not front_matter:
        return ""
    try:
        front_matter_dict = {}
        if front_matter:
            front_matter_dict = yaml.safe_load(front_matter)
        if "title" in front_matter_dict:
            if len(front_matter_dict["title"]) > 500:
                translated_title = translate_text(
                    front_matter_dict["title"], target_language
                )
                if translated_title:
                    front_matter_dict["title"] = translated_title
        # Always set lang to target_language
        front_matter_dict["lang"] = target_language
        return "---\n" + yaml.dump(front_matter_dict, allow_unicode=True) + "---"
    except yaml.YAMLError as e:
        print(f"  Error parsing front matter: {e}")
        return front_matter


def fix_title_in_file(input_file, target_language, original_file):
    print(f"  Processing file: {input_file}")
    try:
        with open(original_file, "r", encoding="utf-8") as infile:
            original_content = infile.read()
        original_post = frontmatter.loads(original_content)
        original_title = original_post.get("title", None)
        if not original_title:
            print(f"  No title found in original file: {original_file}")
            return

        with open(input_file, "r", encoding="utf-8") as infile:
            content = infile.read()

        # Extract front matter
        front_matter_match = re.match(r"---\n(.*?)\n---", content, re.DOTALL)
        if not front_matter_match:
            print(f"  No front matter found in {input_file}")
            return
        front_matter = front_matter_match.group(1)

        print(f"  Front matter: {front_matter[:50]}...")

        translated_front_matter = translate_front_matter(front_matter, target_language)

        translated_content = (
            translated_front_matter + content[len(front_matter_match.group(0)) :]
        )

        with open(input_file, "w", encoding="utf-8") as outfile:
            outfile.write(translated_content)
        print(f"  Finished processing file: {input_file}")
    except Exception as e:
        print(f"  Error processing file {input_file}: {e}")


if __name__ == "__main__":
    if not DEEPSEEK_API_KEY:
        print("Error: DEEPSEEK_API_KEY is not set in .env file.")
        exit()

    parser = argparse.ArgumentParser(
        description="Translate markdown files to a specified language."
    )
    parser.add_argument(
        "--lang",
        type=str,
        default="ja",
        help="Target language for translation (e.g., ja, es).",
    )
    args = parser.parse_args()
    target_language = args.lang

    print(f"Starting title fix for language: {target_language}")

    input_dir = os.path.join(INPUT_DIR, target_language)
    if not os.path.exists(input_dir):
        print(f"  Creating directory: {input_dir}")
        os.makedirs(input_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(f"-{target_language}.md"):
            input_file = os.path.join(input_dir, filename)
            original_filename = filename.replace(f"-{target_language}", "-en")
            original_file = os.path.join(INPUT_DIR, "en", original_filename)
            if not os.path.exists(original_file):
                print(f"  Original file not found: {original_file}")
                continue
            print(f"  Processing file: {input_file}")

            with open(original_file, "r", encoding="utf-8") as infile:
                original_content = infile.read()
            original_post = frontmatter.loads(original_content)

            if "title" in original_post:
                translated_title = None
                with open(input_file, "r", encoding="utf-8") as infile:
                    content = infile.read()

                # Extract front matter
                front_matter_match = re.match(r"---\n(.*?)\n---", content, re.DOTALL)
                if not front_matter_match:
                    print(f"  No front matter found in {input_file}")
                    continue
                front_matter = front_matter_match.group(1)

                front_matter_dict = {}
                if front_matter:
                    front_matter_dict = yaml.safe_load(front_matter)
                if "title" in front_matter_dict:
                    translated_title = front_matter_dict["title"]

                if translated_title and len(translated_title) > 500:
                    print(f"  Front matter: {front_matter[:50]}...")

                    translated_front_matter = translate_front_matter(
                        front_matter, target_language
                    )

                    translated_content = (
                        translated_front_matter
                        + content[len(front_matter_match.group(0)) :]
                    )

                    with open(input_file, "w", encoding="utf-8") as outfile:
                        outfile.write(translated_content)
                    print(f"  Finished processing file: {input_file}")
            else:
                print(f"  No title found in original file: {original_file}")
                continue
    print(f"Finished title fix for language: {target_language}")
