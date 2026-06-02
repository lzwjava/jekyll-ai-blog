import os
import argparse
import subprocess
from dotenv import load_dotenv
import concurrent.futures
import frontmatter
from markdown_translate_client import translate_markdown_file

import sys

# Add the project root to the Python path to import from tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from tests.workflow.test_posts_complete import (
    analyze_post_completeness,
    analyze_notes_completeness,
)

# Import utility functions for handling note and post files
sys.path.append(os.path.dirname(__file__))
from update_lang_utils import get_original_file_for_md_file

load_dotenv()

INPUT_DIR = "original"
MAX_THREADS = 10


def get_output_filename(filename, target_lang):
    orig_langs = ["en", "zh", "ja"]
    for orig in orig_langs:
        suffix = f"-{orig}.md"
        if filename.endswith(suffix):
            return filename.replace(suffix, f"-{target_lang}.md")
    raise Exception(f"Unexpected filename format: {filename}")


def get_changed_files(commits=10):
    changed_files = set()
    languages = ["ja", "es", "hi", "zh", "en", "fr", "de", "ar", "hant"]

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
        for possible in ["en", "zh", "ja"]:
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
        help="Model to use for translation (e.g., deepseek-v3.2, mistral-medium, gemini-flash).",
    )
    parser.add_argument(
        "--commits",
        type=int,
        default=10,
        help="Number of recent commits to check for changes (default: 10).",
    )
    parser.add_argument(
        "--fix_orphaned",
        action="store_true",
        help="Fix orphaned posts by translating missing languages.",
    )
    args = parser.parse_args()
    fix_orphaned = args.fix_orphaned
    target_language = args.lang
    dry_run = args.dry_run
    input_file = args.file
    max_files = args.max_files
    model = args.model
    commits = args.commits

    if target_language == "all":
        languages = ["ja", "es", "hi", "zh", "en", "fr", "de", "ar", "hant"]
    else:
        languages = [target_language]

    if input_file:
        changed_files = {(input_file, lang) for lang in languages}
        if max_files and len(changed_files) > max_files:
            changed_files = set(list(changed_files)[:max_files])
        total_files_to_process = len(changed_files)
    elif fix_orphaned:
        print("Fixing orphaned posts and notes...")
        orphaned_posts, _ = analyze_post_completeness()
        orphaned_notes, _ = analyze_notes_completeness()
        changed_files = set()

        # Handle orphaned posts
        for post in orphaned_posts:
            if not post["has_original_source"]:
                print(f"Skipping {post['base_name']} - no original source")
                continue

            # Find an existing translated file for this post to determine the original source
            original_file = None
            found_lang = None

            # Check if any translated version exists in _posts
            for lang in ["en", "zh", "ja", "es", "hi", "fr", "de", "ar", "hant"]:
                candidate = os.path.join(
                    "_posts", lang, f"{post['base_name']}-{lang}.md"
                )
                if os.path.exists(candidate):
                    # Use the utility function to find the original file
                    result = get_original_file_for_md_file(candidate)
                    if result:
                        original_file, found_lang = result
                        break

            if not original_file:
                print(f"Could not find original source for {post['base_name']}")
                continue

            print(f"Found original file for {post['base_name']}: {original_file}")
            for missing_lang in post["missing_languages"]:
                if target_language == "all" or missing_lang == target_language:
                    changed_files.add((original_file, missing_lang))

        # Handle orphaned notes
        for note in orphaned_notes:
            if not note["has_original_source"]:
                print(f"Skipping {note['base_name']} - no original source")
                continue

            # For notes, the original file is in the notes directory with -en.md suffix
            # since notes use _posts/en as the reference
            for orig_lang in ["en", "zh", "ja"]:
                candidate = os.path.join("notes", f"{note['base_name']}-{orig_lang}.md")
                if os.path.exists(candidate):
                    original_file = candidate
                    break

            if not original_file:
                print(f"Could not find original source for {note['base_name']}")
                continue

            print(f"Found original file for note {note['base_name']}: {original_file}")
            for missing_lang in note["missing_languages"]:
                if target_language == "all" or missing_lang == target_language:
                    changed_files.add((original_file, missing_lang))
        if max_files and len(changed_files) > max_files:
            changed_files = set(list(changed_files)[:max_files])
        total_files_to_process = len(changed_files)
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
            output_dir = f"_posts/{lang}"
            os.makedirs(output_dir, exist_ok=True)
            output_filename = get_output_filename(os.path.basename(filename), lang)
            output_file = os.path.join(output_dir, output_filename)
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
