import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
import concurrent.futures

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
MODEL_NAME = "deepseek-chat"
INPUT_DIR = "."
MAX_THREADS = 3
# TARGET_LANGUAGE = "zh" # Removed hardcoded target language

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
            with open(output_file, "w", encoding="utf-8") as outfile:
                outfile.write(translated_content)
            print(f"  Finished processing file: {output_file}")
        else:
            print(f"  Translation failed for {input_file}")
    except Exception as e:
        print(f"  Error processing file {input_file}: {e}")


def main():
    if not DEEPSEEK_API_KEY:
        print("Error: DEEPSEEK_API_KEY is not set in .env file.")
        return

    parser = argparse.ArgumentParser(description="Translate LaTeX files.")
    parser.add_argument("--file", type=str, help="Path to the LaTeX file to translate.")
    parser.add_argument(
        "--lang",
        type=str,
        default="zh",
        help="Target language for translation (e.g., ja, es, all).",
    )
    parser.add_argument(
        "--kind",
        type=str,
        default="resume",
        help="Kind of document to translate (resume, coverletter, introduction).",
    )
    args = parser.parse_args()
    target_language = args.lang
    kind = args.kind

    languages = ["ja", "es", "hi", "zh", "en", "fr"]
    if target_language not in languages:
        print(
            f"Error: Invalid target language: {target_language}. Please choose from {languages}"
        )
        return

    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}")
            return

        filename = args.file
        output_dir = os.path.dirname(filename)
        output_filename = os.path.basename(filename)

        os.path.basename(filename).replace(".tex", "")

        if kind == "resume":
            if "awesome-cv/en/resume-en/resume-en.tex" in filename:
                output_dir = os.path.join(
                    os.path.dirname(os.path.dirname(filename)),
                    target_language,
                    "resume-" + target_language,
                )
                output_filename = f"resume-{target_language}.tex"
        elif kind == "coverletter":
            if "awesome-cv/en/coverletter-en.tex" in filename:
                output_dir = os.path.join(
                    os.path.dirname(os.path.dirname(filename)), target_language
                )
                output_filename = f"coverletter-{target_language}.tex"
        elif kind == "introduction":
            if "awesome-cv/en/introduction-en.tex" in filename:
                output_dir = os.path.join(
                    os.path.dirname(os.path.dirname(filename)), target_language
                )
                output_filename = f"introduction-{target_language}.tex"
        else:
            print(
                f"Error: Invalid kind: {kind}. Please choose from resume, coverletter, or introduction"
            )
            return

        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, output_filename)

        print(f"Submitting translation job for {filename}...")
        translate_latex_file(filename, output_file, target_language)

    input_dir = "."

    files_to_translate = []
    for root, _, files in os.walk(input_dir):
        if "_site" in root:
            continue
        for file in files:
            full_path = os.path.join(root, file)
            if file.endswith(".tex") and (
                (
                    kind == "resume"
                    and "awesome-cv/en/resume-en/resume-en.tex" in full_path
                )
                or (
                    kind == "coverletter"
                    and "awesome-cv/en/coverletter-en.tex" in full_path
                )
                or (
                    kind == "introduction"
                    and "awesome-cv/en/introduction-en.tex" in full_path
                )
            ):
                files_to_translate.append(full_path)

    if not files_to_translate:
        print(f"No .tex files found in specified locations in {input_dir}")
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = []
        for filename in files_to_translate:
            if os.path.exists(filename):
                output_dir = os.path.dirname(filename)
                output_filename = os.path.basename(filename)

                os.path.basename(filename).replace(".tex", "")

                if kind == "resume":
                    if "awesome-cv/en/resume-en/resume-en.tex" in filename:
                        output_dir = os.path.join(
                            os.path.dirname(os.path.dirname(filename)),
                            target_language,
                            "resume-" + target_language,
                        )
                        output_filename = f"resume-{target_language}.tex"
                elif kind == "coverletter":
                    if "awesome-cv/en/coverletter-en.tex" in filename:
                        output_dir = os.path.join(
                            os.path.dirname(os.path.dirname(filename)), target_language
                        )
                        output_filename = f"coverletter-{target_language}.tex"
                elif kind == "introduction":
                    if "awesome-cv/en/introduction-en.tex" in filename:
                        output_dir = os.path.join(
                            os.path.dirname(os.path.dirname(filename)), target_language
                        )
                        output_filename = f"introduction-{target_language}.tex"

                os.makedirs(output_dir, exist_ok=True)
                output_file = os.path.join(output_dir, output_filename)

                print(f"Submitting translation job for {filename}...")
                future = executor.submit(
                    translate_latex_file, filename, output_file, target_language
                )
                futures.append(future)
            else:
                print(f"Skipping {filename} because it does not exist.")

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"A thread failed: {e}")


if __name__ == "__main__":
    main()
