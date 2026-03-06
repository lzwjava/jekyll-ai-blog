import os
import json
import argparse
from datetime import datetime
import subprocess
import platform
from pdf_base import text_to_pdf_from_markdown

OUTPUT_DIRECTORY = "assets/pdfs"
INPUT_DIRECTORY = "_posts"
LANGUAGES = ["en", "zh", "ja", "es", "hi", "fr", "de", "ar", "hant"]


def get_all_md_files(input_dir):
    md_files = []
    for lang in LANGUAGES:
        lang_dir = os.path.join(input_dir, lang)
        if os.path.exists(lang_dir):
            md_files.extend(
                [
                    os.path.join(lang_dir, f)
                    for f in os.listdir(lang_dir)
                    if f.endswith(".md")
                ]
            )
    return md_files


def get_last_n_files(input_dir, n=10):
    try:
        md_files = get_all_md_files(input_dir)
        md_files_sorted = sorted(
            md_files, key=lambda x: os.path.getmtime(x), reverse=True
        )
        last_n_files = md_files_sorted[:n]
        return last_n_files
    except Exception as e:
        print(f"Error retrieving files from {input_dir}: {e}")
        return []


def process_markdown_files(
    input_dir, output_dir, max_files=10000, dry_run=False, n=None
):

    files_processed = 0
    files_skipped = 0

    for lang in LANGUAGES:
        lang_dir = os.path.join(input_dir, lang)
        if not os.path.exists(lang_dir):
            print(f"Skipping language {lang}: directory does not exist.")
            continue

        if n is not None:
            md_files_to_process = get_last_n_files(lang_dir, n)
        else:
            md_files_to_process = [
                os.path.join(lang_dir, f)
                for f in os.listdir(lang_dir)
                if f.endswith(".md")
            ]

        total_files = len(md_files_to_process)
        print(f"Total Markdown files to process for {lang}: {total_files}")

        if total_files == 0:
            print(f"No Markdown files to process in '{lang_dir}' directory.")
            continue

        for idx, md_file_path in enumerate(md_files_to_process, start=1):
            filename = os.path.basename(md_file_path)
            pdf_filename = f"{os.path.splitext(filename)[0]}.pdf"
            output_lang_dir = os.path.join(output_dir, lang)
            os.makedirs(output_lang_dir, exist_ok=True)
            output_filename = os.path.join(output_lang_dir, pdf_filename)

            if os.path.exists(output_filename):
                print(f"Skipping {filename}: {output_filename} already exists.")
                files_skipped += 1
                continue

            print(
                f"\nProcessing {files_processed + 1}/{total_files - files_skipped}: {filename}"
            )
            try:
                with open(md_file_path, "r", encoding="utf-8") as file:
                    markdown_content = file.read()

                title_line = None

                if markdown_content.startswith("---"):
                    lines = markdown_content.split("\n")
                    try:
                        second_delim_index = lines[1:].index("---") + 1
                        front_matter_lines = lines[1:second_delim_index]
                        cleaned_lines = lines[second_delim_index + 1 :]

                        for fm_line in front_matter_lines:
                            fm_line_stripped = fm_line.strip()
                            if fm_line_stripped.lower().startswith("title:"):
                                title_value = fm_line_stripped.split(":", 1)[1].strip()
                                if (
                                    title_value.startswith('"')
                                    and title_value.endswith('"')
                                ) or (
                                    title_value.startswith("'")
                                    and title_value.endswith("'")
                                ):
                                    title_value = title_value[1:-1].strip()
                                if title_value:
                                    title_line = f"# {title_value}"
                                break

                        markdown_content = "\n".join(cleaned_lines)
                    except ValueError:
                        markdown_content = ""

                    if not markdown_content.strip():
                        print(
                            f"Skipping {filename}: No content to convert after cleaning front matter."
                        )
                        files_skipped += 1
                        continue

                    if title_line:
                        markdown_content = title_line + "\n\n" + markdown_content

                    cleaned_md_path = md_file_path + ".cleaned"
                    with open(cleaned_md_path, "w", encoding="utf-8") as temp:
                        temp.write(markdown_content)

                    try:
                        if not text_to_pdf_from_markdown(
                            input_markdown_path=cleaned_md_path,
                            output_pdf_path=output_filename,
                            dry_run=dry_run,
                        ):
                            print(f"Skipping {filename} due to pandoc error.")
                            continue
                    except Exception as e:
                        print(f"Error processing {filename}: {e}")
                        continue
                    finally:
                        if os.path.exists(cleaned_md_path):
                            os.remove(cleaned_md_path)
                        tmp_pdf_path = output_filename.replace(".pdf", "-tmp.pdf")
                        if os.path.exists(tmp_pdf_path):
                            os.remove(tmp_pdf_path)

                    files_processed += 1
                    if files_processed >= max_files:
                        print(f"Processed {max_files} files. Stopping.")
                        break

            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Markdown files to PDFs.")
    parser.add_argument(
        "--max_files",
        type=int,
        default=10000,
        help="Maximum number of files to process (default: 10000).",
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Simulate the conversion without actual file generation.",
    )
    parser.add_argument(
        "--n",
        type=int,
        help="Number of last updated files to process for each language.",
    )
    args = parser.parse_args()

    process_markdown_files(
        INPUT_DIRECTORY,
        OUTPUT_DIRECTORY,
        max_files=args.max_files,
        dry_run=args.dry_run,
        n=args.n,
    )
