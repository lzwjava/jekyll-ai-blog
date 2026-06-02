import os
import argparse
from dotenv import load_dotenv
import concurrent.futures
from markdown_translate_client import translate_markdown_file
import shutil

load_dotenv()

INPUT_DIR = "notes"
MAX_THREADS = 10

# Target languages for translation
TARGET_LANGUAGES = ["zh", "en"]

# TARGET_LANGUAGES = ["ja", "es", "hi", "zh", "en", "fr", "de", "ar", "hant"]


def get_output_filename(filename, target_lang):
    orig_langs = ["en", "zh", "ja"]
    for orig in orig_langs:
        suffix = f"-{orig}.md"
        if filename.endswith(suffix):
            return filename.replace(suffix, f"-{target_lang}.md")
    raise Exception(f"Unexpected filename format: {filename}")


def copy_original_file(source_file, dest_file):
    """Copy original file for source language translations."""
    try:
        shutil.copy2(source_file, dest_file)
        print(f"Successfully copied {source_file} to {dest_file}")
        return True
    except Exception as e:
        print(f"Error copying {source_file} to {dest_file}: {e}")
        raise e


def get_recent_files(n):
    """Get the n most recent files by modification time."""
    try:
        files = []
        for filename in os.listdir(INPUT_DIR):
            if filename.endswith(".md"):
                filepath = os.path.join(INPUT_DIR, filename)
                mtime = os.path.getmtime(filepath)
                files.append((filepath, mtime))

        # Sort by modification time, newest first
        files.sort(key=lambda x: x[1], reverse=True)

        # Return just the file paths
        recent_files = [f[0] for f in files[:n]] if n else [f[0] for f in files]
        print(f"Found {len(recent_files)} recent files: {recent_files}")
        return recent_files
    except Exception as e:
        print(f"Error getting recent files: {e}")
        return []


def main():
    parser = argparse.ArgumentParser(
        description="Translate markdown files to a specified language."
    )
    parser.add_argument(
        "--lang",
        type=str,
        default="all",
        help="Target language for translation (e.g., ja, es, all).",
    )
    parser.add_argument(
        "--file", type=str, default=None, help="Specific file to translate."
    )
    parser.add_argument(
        "--max_files",
        type=int,
        default=None,
        help="Maximum number of files to process.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="deepseek-v3.2",
        help="Model to use for translation (e.g., deepseek-v3.1, mistral-medium, gemini-flash).",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=None,
        help="Number of most recent files to process by modification time.",
    )
    args = parser.parse_args()
    target_language = args.lang
    input_file = args.file
    model = args.model
    n = args.n

    if target_language == "all":
        languages = TARGET_LANGUAGES
    else:
        languages = [target_language]

    # Create _posts directory and language subdirectories (consistent with update_lang.py)
    os.makedirs("_posts", exist_ok=True)
    for lang in languages:
        os.makedirs(f"_posts/{lang}", exist_ok=True)

    if input_file:
        changed_files = {
            (input_file, lang)
            for lang in languages
            if not os.path.exists(
                os.path.join(
                    f"_posts/{lang}",
                    get_output_filename(os.path.basename(input_file), lang),
                )
            )
        }
        total_files_to_process = len(changed_files)
    elif n is not None:
        recent_files = get_recent_files(n)
        changed_files = set()
        for input_file in recent_files:
            orig_lang = None
            filename = os.path.basename(input_file)
            for possible in ["en", "zh", "ja"]:
                if filename.endswith(f"-{possible}.md"):
                    orig_lang = possible
                    break
            if orig_lang:
                for lang in languages:
                    target_filename = get_output_filename(filename, lang)
                    target_file = os.path.join(f"_posts/{lang}", target_filename)
                    if not os.path.exists(target_file):
                        changed_files.add((input_file, lang))
        total_files_to_process = len(changed_files)
    else:
        print("Error: Must specify either --file, --n, or another valid option")
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = []
        for filename, lang in changed_files:
            input_file = filename
            output_dir = f"_posts/{lang}"
            os.makedirs(output_dir, exist_ok=True)
            output_filename = get_output_filename(os.path.basename(filename), lang)
            output_file = os.path.join(output_dir, output_filename)

            # Get the original language from the filename
            orig_lang = None
            filename_base = os.path.basename(filename)
            for possible in ["en", "zh", "ja"]:
                if filename_base.endswith(f"-{possible}.md"):
                    orig_lang = possible
                    break

            if orig_lang == lang:
                # If target language is same as source language, copy the file
                print(f"Copying original file {filename} to {output_file}...")
                future = executor.submit(copy_original_file, input_file, output_file)
            else:
                # Otherwise, translate it
                print(f"Submitting translation job for {filename} to {lang}...")
                future = executor.submit(
                    translate_markdown_file, input_file, output_file, lang, model
                )
            futures.append(future)
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"A thread failed: {e}")
    print(f"Total Markdown files to process: {total_files_to_process}")


if __name__ == "__main__":
    main()
