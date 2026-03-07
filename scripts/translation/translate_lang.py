import os
import re
import argparse
from dotenv import load_dotenv
from openai import OpenAI
import yaml
import concurrent.futures

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
MODEL_NAME = "deepseek-chat"
INPUT_DIR = "original"
MAX_THREADS = 10

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")


def create_translation_prompt(target_language):
    if target_language == "zh":
        # Fixed term mapping for zh translations
        zh_term_map = {
            "Zhiwei": "智维",
            "Zhiwei Li": "李智维",
            "Li Zhiwei": "李智维",
            "Meitai Technology Services": "美钛技术服务",
            "Neusiri": "思芮",
            "Chongding Conference": "冲顶大会",
            "Fun Live": "趣直播",
            "MianbaoLive": "面包Live",
            "Beijing Dami Entertainment Co.": "北京大米互娱有限公司",
            "Guangzhou Yuyan Middle School": "广州玉岩中学",
            "Yin Wang": "王垠",
        }
        rules = [f"Translate {src} to {dst}." for src, dst in zh_term_map.items()]
        rules_str = " ".join(rules)
        return (
            "You are a professional translator. You are translating a markdown file "
            "for a Jekyll blog post from English to Chinese. Translate the following "
            f"text to Chinese. {rules_str} Be careful about code blocks, if not sure, "
            "just do not change."
        )
    elif target_language == "hant":
        return "Translate the following text to Traditional Chinese (Hong Kong)."
    elif target_language == "ja":
        return "You are a professional translator. You are translating a markdown file for a Jekyll blog post. Translate the following text to Japanese. Be careful about code blocks, if not sure, just do not change."
    elif target_language == "es":
        return "You are a professional translator. You are translating a markdown file for a Jekyll blog post. Translate the following text to Spanish. Be careful about code blocks, if not sure, just do not change."
    elif target_language == "hi":
        return "You are a professional translator. You are translating a markdown file for a Jekyll blog post. Translate the following text to Hindi. Be careful about code blocks, if not sure, just do not change."
    elif target_language == "fr":
        return "You are a professional translator. You are translating a markdown file for a Jekyll blog post. Translate the following text to French. Be careful about code blocks, if not sure, just do not change."
    elif target_language == "de":
        return "You are a professional translator. You are translating a markdown file for a Jekyll blog post. Translate the following text to German. Be careful about code blocks, if not sure, just do not change."
    elif target_language == "ar":
        return "You are a professional translator. You are translating a markdown file for a Jekyll blog post. Translate the following text to Arabic. Be careful about code blocks, if not sure, just do not change."
    else:
        return f"You are a professional translator. You are translating a markdown file for a Jekyll blog post. Translate the following text to {target_language}. Be careful about code blocks, if not sure, just do not change."


def translate_text(text, target_language):
    print(f"  Translating text: {text[:50]}...")
    prompt = create_translation_prompt(target_language)
    print(f"  Prompt: {prompt}")
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ],
            stream=False,
        )
        if response and response.choices:
            print("  Translation successful.")
            return response.choices[0].message.content
        else:
            print("  Translation failed.")
            return None
    except Exception as e:
        print(f"  Translation failed with error: {e}")
        if "This model's maximum context length is" in str(e):
            print("  Skipping translation due to context length error.")
            return None
        return None


def translate_front_matter(front_matter, target_language, input_file):
    print(f"  Translating front matter for: {input_file}")
    if not front_matter:
        print(f"  No front matter found for: {input_file}")
        return ""
    try:
        front_matter_dict = {}
        if front_matter:
            front_matter_dict = yaml.safe_load(front_matter)
            print(f"  Front matter after safe_load: {front_matter_dict}")

        front_matter_dict_copy = front_matter_dict.copy()

        if "title" in front_matter_dict_copy:
            print(f"  Translating title: {front_matter_dict_copy['title']}")
            translated_title = translate_text(
                front_matter_dict_copy["title"], target_language
            )
            if translated_title:
                translated_title = translated_title.strip()
                if len(translated_title) > 300:
                    translated_title = translated_title.split("\n")[0]
                front_matter_dict_copy["title"] = translated_title
                print(f"  Translated title to: {translated_title}")
            else:
                print(f"  Title translation failed for: {input_file}")
        # Always set lang to target_language
        front_matter_dict_copy["lang"] = target_language
        front_matter_dict_copy["translated"] = True

        result = "---\n" + yaml.dump(front_matter_dict_copy, allow_unicode=True) + "---"
        print(f"  Front matter translation complete for: {input_file}")
        return result
    except yaml.YAMLError as e:
        print(f"  Error parsing front matter: {e}")
        return front_matter


def translate_markdown_file(input_file, output_file, target_language):
    print(f"  Processing file: {input_file}")
    try:
        with open(input_file, "r", encoding="utf-8") as infile:
            content = infile.read()

        # Extract front matter
        front_matter_match = re.match(r"---\n(.*?)\n---", content, re.DOTALL)
        front_matter = front_matter_match.group(1) if front_matter_match else ""
        content_without_front_matter = (
            content[len(front_matter_match.group(0)) :]
            if front_matter_match
            else content
        )
        print(f"  Front matter: {front_matter[:50]}...")

        translated_front_matter = translate_front_matter(front_matter, target_language)

        translated_content = translate_text(
            content_without_front_matter, target_language
        )
        if translated_content:
            translated_content = translated_front_matter + "\n\n" + translated_content
        else:
            translated_content = content

        with open(output_file, "w", encoding="utf-8") as outfile:
            outfile.write(translated_content)
        print(f"  Finished processing file: {output_file}")
    except Exception as e:
        print(f"  Error processing file {input_file}: {e}")


def main():
    if not DEEPSEEK_API_KEY:
        print("Error: DEEPSEEK_API_KEY is not set in .env file.")
        return

    parser = argparse.ArgumentParser(
        description="Translate markdown files to a specified language."
    )
    parser.add_argument(
        "--n", type=int, default=None, help="Maximum number of files to translate."
    )
    parser.add_argument(
        "--lang",
        type=str,
        default="ja",
        help="Target language for translation (e.g., ja, es).",
    )
    args = parser.parse_args()
    max_files = args.n
    target_language = args.lang

    output_dir = f"_posts/{target_language}"
    if target_language == "hi":
        output_dir = "_posts/hi"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created directory {output_dir}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        translated_count = 0
        futures = []
        for filename in os.listdir(INPUT_DIR):
            if max_files is not None and translated_count >= max_files:
                print(f"Reached max files limit: {max_files}. Stopping translation.")
                break
            if filename.endswith(".md"):
                input_file = os.path.join(INPUT_DIR, filename)
                output_filename = filename.replace(".md", f"-{target_language}.md")

                # Check if the original file is named with "-en.md" or "-zh.md"
                if filename.endswith("-en.md") or filename.endswith("-zh.md"):
                    output_filename = filename.replace(
                        "-en.md", f"-{target_language}.md"
                    ).replace("-zh.md", f"-{target_language}.md")

                output_file = os.path.join(output_dir, output_filename)
                if not os.path.exists(output_file):
                    print(f"Submitting translation job for {filename}...")
                    future = executor.submit(
                        translate_markdown_file,
                        input_file,
                        output_file,
                        target_language,
                    )
                    futures.append(future)
                    translated_count += 1
                else:
                    print(f"Skipping {filename} because {output_file} already exists.")

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"A thread failed: {e}")


if __name__ == "__main__":
    main()
