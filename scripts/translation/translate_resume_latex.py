import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
MODEL_NAME = "deepseek-chat"
INPUT_DIR = "latex/en/resume-en"
OUTPUT_DIR = "latex"

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")


def create_translation_prompt(target_language):
    if target_language == "zh":
        return """You are a professional translator. You are translating a LaTeX file from English to Chinese. Translate the following text to Chinese. Translate Zhiwei Li to 李智维. Translate Meitai Technology Services to 美钛技术服务. Translate Neusiri to 思芮 instead of 纽思瑞. Translate Chongding Conference to 冲顶大会. Translate Fun Live to 趣直播. Translate MianbaoLive to 面包Live. Translate Beijing Dami Entertainment Co. to 北京大米互娱有限公司. Translate Guangzhou Yuyan Middle School to 广州玉岩中学. Do not translate English names or LaTeX commands. Be careful about code blocks, if not sure, just do not change."""
    elif target_language == "ja":
        return "You are a professional translator. You are translating a LaTeX file. Translate the following text to Japanese. Translate Zhiwei Li to 李智维 as chinese translation. Do not translate English names or LaTeX commands. Be careful about code blocks, if not sure, just do not change."
    elif target_language == "es":
        return "You are a professional translator. You are translating a LaTeX file. Translate the following text to Spanish. Translate Zhiwei Li to 李智维 as chinese translation. Do not translate English names or LaTeX commands. Be careful about code blocks, if not sure, just do not change."
    elif target_language == "hi":
        return "You are a professional translator. You are translating a LaTeX file. Translate the following text to Hindi. Translate Zhiwei Li to 李智维 as chinese translation. Do not translate English names or LaTeX commands. Be careful about code blocks, if not sure, just do not change."
    elif target_language == "fr":
        return "You are a professional translator. You are translating a LaTeX file. Translate the following text to French. Translate Zhiwei Li to 李智维 as chinese translation. Do not translate English names or LaTeX commands. Be careful about code blocks, if not sure, just do not change."
    elif target_language == "en":
        return "You are a professional translator. You are translating a LaTeX file. Translate the following text to English. Translate Zhiwei Li to 李智维 as chinese translation. Do not translate English names or LaTeX commands. Be careful about code blocks, if not sure, just do not change."
    else:
        return f"You are a professional translator. You are translating a LaTeX file. Translate the following text to {target_language}. Translate Zhiwei Li to 李智维 as chinese translation. Do not translate English names or LaTeX commands. Be careful about code blocks, if not sure, just do not change."


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
            print("  Translation successful.")
            return response.choices[0].message.content
        else:
            print("  Translation failed.")
            return None
    except Exception as e:
        print(f"  Translation failed with error: {e}")
        return None


def translate_latex_file(input_file, output_file, target_language):
    print(f"  Processing file: {input_file}")
    try:
        with open(input_file, "r", encoding="utf-8") as infile:
            content = infile.read()

        translated_content = translate_text(content, target_language)

        if translated_content:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as outfile:
                outfile.write(translated_content)
            print(f"  Replaced file: {output_file}")
        else:
            print(f"  Translation failed for {input_file}")
    except Exception as e:
        print(f"  Error processing file {input_file}: {e}")


def main():
    if not DEEPSEEK_API_KEY:
        print("Error: DEEPSEEK_API_KEY is not set in .env file.")
        return

    parser = argparse.ArgumentParser(
        description="Translate a specific LaTeX resume section."
    )
    parser.add_argument(
        "--section",
        type=str,
        required=True,
        help="Section file to translate (e.g., blogposts.tex).",
    )
    parser.add_argument(
        "--lang",
        type=str,
        default="zh",
        help="Target language for translation (e.g., ja, es, hi, zh, en, fr).",
    )
    parser.add_argument(
        "--kind",
        type=str,
        default="resume",
        help="Kind of document to translate (resume only).",
    )
    args = parser.parse_args()
    target_language = args.lang
    section_to_translate = args.section
    kind = args.kind

    languages = ["ja", "es", "hi", "zh", "en", "fr"]
    if target_language not in languages:
        print(
            f"Error: Invalid target language: {target_language}. Please choose from {languages}"
        )
        return

    if kind != "resume":
        print(f"Error: This script only supports 'resume' kind, not {kind}.")
        return

    if not section_to_translate.endswith(".tex"):
        print(f"Error: Section file {section_to_translate} must be a .tex file.")
        return

    input_file = os.path.join(INPUT_DIR, section_to_translate)
    if not os.path.exists(input_file):
        print(f"Error: Section file {input_file} not found.")
        return

    output_dir = os.path.join(OUTPUT_DIR, target_language, f"resume-{target_language}")
    output_file = os.path.join(output_dir, section_to_translate)

    print(f"Submitting translation job for section {section_to_translate}...")
    translate_latex_file(input_file, output_file, target_language)


if __name__ == "__main__":
    main()

# python scripts/translation/translate_resume_latex.py --section corporateprojects.tex --lang zh --kind resume
