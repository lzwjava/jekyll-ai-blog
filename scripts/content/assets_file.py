import os
import argparse
import re
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def log_infrequently(message):
    logging.info(message)


def delete_asset_if_no_original_md(asset_type, asset_dir, posts_dir, dry_run=False):
    """Deletes assets (pdf or audio) if no corresponding markdown file exists."""
    log_infrequently(f"Checking {asset_type} files in {asset_dir}...")

    if not os.path.exists(asset_dir):
        log_infrequently(f"  Directory not found: {asset_dir}")
        return

    files_to_delete = []
    for asset_file in os.listdir(asset_dir):
        if asset_file.endswith(f".{asset_type}"):
            log_infrequently(f"  Processing {asset_type} file: {asset_file}")
            base_name = asset_file.rsplit(".", 1)[0]

            potential_md_files = []

            date_match = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)", base_name)
            if date_match:
                log_infrequently(f"    Detected date pattern in filename: {base_name}")
                date_str = date_match.group(1)
                name_with_lang = date_match.group(2)
                name_without_lang = name_with_lang.rsplit("-", 1)[0]

                for lang in ["en", "zh", "ja", "es", "hi", "fr", "de", "ar", "hant"]:
                    potential_md_files.append(
                        os.path.join(
                            posts_dir, lang, f"{date_str}-{name_without_lang}-{lang}.md"
                        )
                    )
                    log_infrequently(
                        f"      Checking for markdown file: {os.path.join(posts_dir, lang, f'{date_str}-{name_without_lang}-{lang}.md')}"
                    )
            else:
                potential_md_files.append(os.path.join("notes", f"{base_name}.md"))
                log_infrequently(
                    f"    Checking for markdown file: {os.path.join('notes', f'{base_name}.md')}"
                )

            original_md_exists = any(
                os.path.exists(md_file) for md_file in potential_md_files
            )

            if not original_md_exists:
                asset_path = os.path.join(asset_dir, asset_file)
                files_to_delete.append(asset_path)
                log_infrequently(
                    f"    Will delete {asset_type} file: {asset_path} (no corresponding markdown file)"
                )
            else:
                log_infrequently(
                    f"    Kept {asset_type} file: {os.path.join(asset_dir, asset_file)} (corresponding markdown file exists)"
                )

    if dry_run:
        if files_to_delete:
            log_infrequently(
                f"  Dry run: The following {asset_type} files in {asset_dir} would be deleted (posts_dir: {posts_dir}):"
            )
            for file_path in files_to_delete:
                log_infrequently(f"    {file_path}")
        else:
            log_infrequently(
                f"  Dry run: No {asset_type} files in {asset_dir} to delete (posts_dir: {posts_dir})."
            )
    else:
        for file_path in files_to_delete:
            os.remove(file_path)
            log_infrequently(
                f"  Deleted {asset_type} file: {file_path} (no corresponding markdown file, posts_dir: {posts_dir})"
            )


def main():
    parser = argparse.ArgumentParser(
        description="Delete assets if no corresponding markdown file exists."
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Perform a dry run, printing files to delete without actually deleting them.",
    )
    args = parser.parse_args()

    pdf_base_dir = "assets/pdfs"
    audio_dir = "assets/audios"
    posts_dir = "_posts"

    for lang_dir in os.listdir(pdf_base_dir):
        pdf_dir = os.path.join(pdf_base_dir, lang_dir)
        if os.path.isdir(pdf_dir):
            delete_asset_if_no_original_md(
                "pdf", pdf_dir, posts_dir, dry_run=args.dry_run
            )

    delete_asset_if_no_original_md("mp3", audio_dir, posts_dir, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
