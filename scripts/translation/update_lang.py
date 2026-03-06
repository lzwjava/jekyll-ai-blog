import os
import argparse
import subprocess
from dotenv import load_dotenv
import concurrent.futures
import frontmatter
import shutil
from markdown_translate_client import translate_markdown_file

load_dotenv()

INPUT_DIR = "original"
INPUT_DIR_NOTES = "notes"
MAX_THREADS = 10

# Configurable language lists
# TARGET_LANGUAGES = ["ja", "es", "hi", "zh", "en", "fr", "de", "ar", "hant"]
TARGET_LANGUAGES = ["zh", "en"]

ORIGINAL_LANGUAGES = ["en", "zh"]


def get_output_filename(filename, target_lang):
    for orig in ORIGINAL_LANGUAGES:
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


def get_recent_files(n, input_dir=INPUT_DIR):
    """Get the n most recent files by modification time."""
    try:
        files = []
        for filename in os.listdir(input_dir):
            if filename.endswith(".md"):
                filepath = os.path.join(input_dir, filename)
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


def get_changed_files(commits=10):
    changed_files = set()
    languages = TARGET_LANGUAGES

    # Get files changed in the original directory from the last N commits
    print(f"Checking for changes in original directory from last {commits} commits...")
    try:
        result = subprocess.run(
            [
                "git",
                "log",
                "--name-only",
                "--pretty=format:",
                f"-{commits}",
                "--",
                "original/",
            ],
            capture_output=True,
            text=True,
            cwd=".",
        )
        if result.returncode != 0:
            print(f"Git command failed: {result.stderr}")
            # Fall back to scanning all files if git fails
            changed_original_files = set()
            for filename in os.listdir(INPUT_DIR):
                if filename.endswith(".md"):
                    changed_original_files.add(os.path.join(INPUT_DIR, filename))
        else:
            # Filter for markdown files in original directory
            git_changed_files = [
                line.strip()
                for line in result.stdout.strip().split("\n")
                if line.strip()
            ]
            changed_original_files = set()
            for file_path in git_changed_files:
                if file_path.startswith("original/") and file_path.endswith(".md"):
                    changed_original_files.add(file_path)

            # If no changes found in git, check all files
            if not changed_original_files:
                print("No changes found in git history, scanning all files...")
                for filename in os.listdir(INPUT_DIR):
                    if filename.endswith(".md"):
                        changed_original_files.add(os.path.join(INPUT_DIR, filename))
    except Exception as e:
        print(f"Error running git command: {e}")
        # Fall back to scanning all files
        changed_original_files = set()
        for filename in os.listdir(INPUT_DIR):
            if filename.endswith(".md"):
                changed_original_files.add(os.path.join(INPUT_DIR, filename))

    print(
        f"Found {len(changed_original_files)} files to check: {list(changed_original_files)}"
    )

    for input_file in changed_original_files:
        filename = os.path.basename(input_file)
        print(f"Processing file: {input_file}")

        # Check if file exists, skip if not
        if not os.path.exists(input_file):
            print(f"  File does not exist, skipping: {input_file}")
            continue

        if not filename.endswith(".md"):
            print(f"Skipping non-markdown file: {filename}")
            continue

        # Extract orig_lang from filename
        orig_lang = None
        for possible in ORIGINAL_LANGUAGES:
            if filename.endswith(f"-{possible}.md"):
                orig_lang = possible
                break
        if not orig_lang:
            print(f"Unexpected filename format: {filename}")
            continue

        try:
            with open(input_file, "r", encoding="utf-8") as infile:
                content = infile.read()
            if not content.lstrip().startswith("---"):
                raise Exception(f"No front matter found in markdown file: {input_file}")
            front_matter_dict, content_without_front_matter = frontmatter.parse(content)
            front_matter_dict = front_matter_dict or {}
            original_title = front_matter_dict.get("title", "")
            print(
                f"  Original language (from filename): {orig_lang}, Title: {original_title}"
            )

            output_dir = f"_posts/{orig_lang}"
            output_filename = filename
            output_file = os.path.join(output_dir, output_filename)
            print(f"  Checking original output file: {output_file}")

            needs_retranslate_all = True  # Default to True if file doesn't exist
            if os.path.exists(output_file):
                with open(output_file, "r", encoding="utf-8") as translated_infile:
                    translated_content = translated_infile.read()
                (
                    translated_front_matter_dict,
                    translated_content_without_front_matter,
                ) = frontmatter.parse(translated_content)
                translated_front_matter_dict = translated_front_matter_dict or {}
                translated_title = translated_front_matter_dict.get("title", "")
                print(f"  Translated title: {translated_title}")
                if (
                    translated_title == original_title
                    and translated_content_without_front_matter.strip()
                    == content_without_front_matter.strip()
                ):
                    needs_retranslate_all = False
                else:
                    print(
                        f"  File {input_file} needs update due to content change in original lang {orig_lang}"
                    )
            else:
                print(f"  Original output file does not exist: {output_file}")

            if needs_retranslate_all:
                # Add all target language files for retranslation
                for target_lang in languages:
                    changed_files.add((input_file, target_lang))
                    print(
                        f"  Added {input_file} for {target_lang} translation due to changes"
                    )
            else:
                # Only add missing translations
                for target_lang in languages:
                    target_dir = f"_posts/{target_lang}"
                    target_filename = get_output_filename(filename, target_lang)
                    target_file = os.path.join(target_dir, target_filename)
                    if not os.path.exists(target_file):
                        changed_files.add((input_file, target_lang))
                        print(
                            f"  Added {input_file} for {target_lang} - missing translation"
                        )

        except Exception as e:
            print(f"Error processing file {input_file}: {e}")

    print(f"Finished scanning. Total files needing updates: {len(changed_files)}")
    return changed_files


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
        "--dry_run",
        action="store_true",
        help="Perform a dry run without modifying files.",
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
        "--commits",
        type=int,
        default=10,
        help="Number of recent commits to check for changes (default: 10).",
    )
    parser.add_argument(
        "--notes",
        action="store_true",
        help="Process notes instead of posts.",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=None,
        help="Number of most recent files to process by modification time (notes only).",
    )
    args = parser.parse_args()
    target_language = args.lang
    dry_run = args.dry_run
    input_file = args.file
    max_files = args.max_files
    model = args.model
    commits = args.commits
    is_notes = args.notes
    n_recent = args.n

    if target_language == "all":
        languages = TARGET_LANGUAGES
    else:
        languages = [target_language]

    # Determine input directory based on --notes flag
    current_input_dir = INPUT_DIR_NOTES if is_notes else INPUT_DIR

    if input_file:
        changed_files = {(input_file, lang) for lang in languages}
        total_files_to_process = len(changed_files)
    elif is_notes:
        if n_recent is not None:
            # Handle notes case with --n option
            recent_files = get_recent_files(n_recent, current_input_dir)
            changed_files = set()
            for input_file in recent_files:
                orig_lang = None
                filename = os.path.basename(input_file)
                for possible in ORIGINAL_LANGUAGES:
                    if filename.endswith(f"-{possible}.md"):
                        orig_lang = possible
                        break
                if orig_lang:
                    for lang in languages:
                        target_filename = get_output_filename(filename, lang)
                        target_file = os.path.join(
                            f"_posts/{lang}", target_filename
                        )  # Always check _posts
                        if not os.path.exists(target_file):
                            changed_files.add((input_file, lang))
            total_files_to_process = len(changed_files)
        else:
            # For notes without --n, we need all files in notes directory
            print("Error: Must specify --n for notes processing")
            return
    else:
        changed_files = get_changed_files(commits)
        if max_files and len(changed_files) > max_files:
            changed_files = set(list(changed_files)[:max_files])
        total_files_to_process = len(changed_files)

    if dry_run:
        print("Dry run mode enabled. No files will be modified.")
        print("Files that would be processed:")
        for filename, lang in changed_files:
            print(f"  - {filename} to language {lang}")
        print(f"Total Markdown files to process: {total_files_to_process}")
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = []
        for filename, lang in changed_files:
            input_file = filename
            output_dir = f"_posts/{lang}"  # Always use _posts for output
            os.makedirs(output_dir, exist_ok=True)
            output_filename = get_output_filename(os.path.basename(filename), lang)
            output_file = os.path.join(output_dir, output_filename)

            # Get the original language from the filename
            orig_lang = None
            filename_base = os.path.basename(filename)
            for possible in ORIGINAL_LANGUAGES:
                if filename_base.endswith(f"-{possible}.md"):
                    orig_lang = possible
                    break

            if orig_lang == lang:
                # If target language is same as source language, copy the file (notes case)
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
