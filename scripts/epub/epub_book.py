import os
import subprocess
import argparse
import glob
from datetime import datetime
import tempfile
import re
import yaml

OUTPUT_DIRECTORY = "assets/epub/"
RESOURCE_DIR = "assets/images"


def convert_markdown_to_kindle(input_path, output_dir):
    """Converts a directory of markdown files to a single epub, ordered by date."""

    if not input_path:
        print("Error: Input path is required.")
        return

    if not os.path.exists(input_path):
        print(f"Error: Input path '{input_path}' does not exist.")
        return

    if not os.path.isdir(input_path):
        print("Error: Input must be a directory containing markdown files.")
        return

    md_files = glob.glob(os.path.join(input_path, "*.md"))
    if not md_files:
        print(f"No markdown files found in {input_path}")
        return

    # Extract date from filename and sort by date desc
    def get_date_from_filename(filename):
        try:
            match = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(filename))
            if match:
                date_str = match.group(1)
                return datetime.strptime(date_str, "%Y-%m-%d")
            else:
                return datetime.min
        except (ValueError, IndexError):
            return datetime.min  # if no date, put at the beginning

    md_files.sort(key=get_date_from_filename, reverse=True)

    _convert_multiple_files(md_files, output_dir)


def _convert_multiple_files(file_paths, output_dir):
    """Converts multiple markdown files to a single epub file."""
    if not output_dir:
        output_dir = OUTPUT_DIRECTORY

    os.makedirs(output_dir, exist_ok=True)

    # Sort file_paths by date desc
    def get_date_from_filepath(filepath):
        try:
            match = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(filepath))
            if match:
                date_str = match.group(1)
                return datetime.strptime(date_str, "%Y-%m-%d")
            else:
                return datetime.min
        except (ValueError, IndexError):
            return datetime.min

    file_paths.sort(key=get_date_from_filepath, reverse=True)

    if file_paths:
        first_file_path = file_paths[0]
        if "_posts" in first_file_path:
            lang = os.path.basename(os.path.dirname(first_file_path))

            if lang == "en":
                lang_name = "English"
            elif lang == "fr":
                lang_name = "French"
            elif lang == "es":
                lang_name = "Spanish"
            elif lang == "ja":
                lang_name = "Japanese"
            elif lang == "zh":
                lang_name = "Simplified Chinese"
            elif lang == "hant":
                lang_name = "Traditional Chinese"
            elif lang == "de":
                lang_name = "German"
            elif lang == "ar":
                lang_name = "Arabic"
            elif lang == "hi":
                lang_name = "Hindi"
            else:
                lang_name = lang.upper()
            output_epub_file = os.path.join(output_dir, f"lzwjava-blog-{lang}.epub")
            title = f"Zhiwei Li's Blog ({lang_name})"
        elif "notes" in first_file_path:
            output_epub_file = os.path.join(output_dir, "lzwjava-notes.epub")
            title = "Zhiwei Li's Notes"
        else:
            output_epub_file = os.path.join(output_dir, "lzwjava-ebook.epub")
            title = "Zhiwei Li's Ebook"
    else:
        output_epub_file = os.path.join(output_dir, "lzwjava-ebook.epub")
        title = "Zhiwei Li's Ebook"

    if os.path.exists(output_epub_file):
        print(f"Skipping: {output_epub_file} already exists.")
        return

    try:
        # Create a temporary file to store the combined markdown content
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False
        ) as tmp_file:
            combined_content = ""
            for file_path in file_paths:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Remove YAML front matter
                    front_matter = ""
                    match = re.search(r"^---(.*?)---", content, re.DOTALL)
                    if match:
                        front_matter = match.group(1)
                        content = content[match.end() :]

                    file_title = os.path.splitext(os.path.basename(file_path))[0]
                    try:
                        if front_matter:
                            yaml_data = yaml.safe_load(front_matter)
                            if "title" in yaml_data:
                                file_title = yaml_data["title"]
                    except yaml.YAMLError as e:
                        print(f"Error parsing YAML in {file_path}: {e}")

                    combined_content += f"# {file_title}\n"

                    if "](assets" in content:

                        def replace_image_tag(match):
                            if match:
                                image_tag = match.group(0)
                                image_url_match = re.search(r"\((.*?)\)", image_tag)
                                if image_url_match:
                                    image_url = image_url_match.group(1)
                                    return f"![]({image_url})"
                                return image_tag
                            return ""

                        # Handle centered images with optional captions
                        def replace_centered_image(match):
                            if match:
                                image_tag = match.group(1)
                                return replace_image_tag(
                                    re.search(r"(!\[.*?\])", image_tag)
                                )
                            return ""

                        content, count = re.subn(
                            r"{:\s*\.centered\s*}\s*(!\[.*?\])(\s*\*.*?\*{:\s*\.caption\s*})?",
                            replace_centered_image,
                            content,
                        )
                        if count > 0:
                            print(
                                f"Replaced {count} centered image tags with optional captions."
                            )

                        # Handle responsive images
                        content = re.sub(
                            r"(!\[.*?\]){:\s*\.responsive\s*}",
                            lambda match: replace_image_tag(match) if match else "",
                            content,
                        )
                        count = len(re.findall(r"!\[.*?\]", content))
                        if count > 0:
                            print("Replaced responsive image tags.")

                        # Remove captions
                        content, count = re.subn(
                            r"\*.*?\*{:\s*\.caption\s*}", "", content
                        )
                        if count > 0:
                            print(f"Removed {count} captions.")

                    combined_content += content
                    combined_content += "\n\n"  # Add a separator between files
            tmp_file.write(combined_content)
            temp_file_path = tmp_file.name

        # Convert the combined markdown file to epub using pandoc
        print(
            f"Converting {len(file_paths)} markdown files to {output_epub_file} using pandoc"
        )
        pandoc_command = [
            "pandoc",
            temp_file_path,
            "-o",
            output_epub_file,
            "--toc",
            "--toc-depth=1",
            "--metadata",
            f"title={title}",
            "--metadata",
            "author=Zhiwei Li",
            "--resource-path",
            RESOURCE_DIR,
        ]
        pandoc_result = subprocess.run(pandoc_command, capture_output=True, text=True)
        if pandoc_result.returncode != 0:
            print(
                f"Error converting to {output_epub_file} using pandoc: {pandoc_result.stderr}"
            )
        else:
            print(f"Successfully converted to {output_epub_file} using pandoc")
    except Exception as e:
        print(f"Error processing files: {e}")
    finally:
        if "temp_file_path" in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown files to epub format."
    )
    parser.add_argument(
        "input_path", help="Path to the directory containing markdown files."
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        help="Output directory for the generated epub files.",
        default=OUTPUT_DIRECTORY,
    )

    args = parser.parse_args()

    convert_markdown_to_kindle(args.input_path, args.output_dir)


if __name__ == "__main__":
    main()
