import os
import argparse
import tempfile
import shutil
import re
import yaml
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.pdf.pdf_base import (
    text_to_pdf_from_markdown,
    generate_title_page_pdf,
    merge_pdfs,
)

OUTPUT_DIRECTORY = "tmp/pdfbooks/"

# Curated list of 9 English originals to mirror across languages.
# We derive the corresponding post path in each target language using the
# filename pattern from scripts/translation/update_lang.py.
ENGLISH_CANDIDATES = [
    "original/2025-01-06-introduction-en.md",
    "original/2024-10-18-books-en.md",
    "original/2025-08-24-links-en.md",
    "original/2025-07-10-english-animation-en.md",
    "original/2006-03-15-primary-school-en.md",
    "original/2024-12-10-life-tips-en.md",
    "original/2025-01-03-programming-en.md",
    "original/2025-01-17-investing-en.md",
    "original/2024-12-12-yin-wang-en.md",
    "original/2023-05-10-answers-en.md",
]

# Only build the three languages requested: English, Japanese, Chinese.
TARGET_LANGS = ["en", "ja", "zh"]


def detect_languages() -> list[str]:
    """Return the fixed set of target languages to build."""
    return TARGET_LANGS[:]


def language_display_name(code: str) -> str:
    mapping = {
        "en": "English",
        "fr": "French",
        "es": "Spanish",
        "ja": "Japanese",
        "zh": "Simplified Chinese",
        "hant": "Traditional Chinese",
        "de": "German",
        "ar": "Arabic",
        "hi": "Hindi",
    }
    return mapping.get(code, code.upper())


def _localize_book_strings(lang: str) -> tuple[str, str, str]:
    """Return (book_title, book_subtitle, toc_title) localized for lang.

    - Title base: "The Little Zhiwei"
    - Subtitle base: "Dedicated to little learners — The Little Java Book Series"
    - Applies deterministic Chinese name mapping per scripts/translation/translate_lang.py.
    - Avoids non-deterministic translations for Japanese; keeps English title/subtitle.
    """
    # Base English strings
    base_title = "The Little Zhiwei"
    base_subtitle = ""
    toc_title = "Contents"

    if lang == "zh":
        # Apply Chinese term mapping: Zhiwei -> 智维, Zhiwei Li -> 李智维
        title = base_title.replace("Zhiwei Li", "李智维").replace("Zhiwei", "智维")
        # "The Little X" -> "小X"
        if title.startswith("The Little "):
            title = "小" + title[len("The Little ") :]
        subtitle = ""
        toc_title = "目录"
        return title, subtitle, toc_title

    if lang == "ja":
        # Keep English to avoid guessy mapping; localize only TOC.
        title = base_title
        subtitle = base_subtitle
        toc_title = "目次"
        return title, subtitle, toc_title

    # Default: English
    return base_title, base_subtitle, toc_title


def combine_markdown(files: list[str]) -> str:
    """Read, strip front matter, normalize image tags, and concatenate two files."""
    combined_content = ""

    def strip_links_images_and_footnotes(md: str) -> str:
        # Remove HTML <img ...> entirely
        md = re.sub(r"<img\b[^>]*>", "", md, flags=re.IGNORECASE)

        # Convert HTML anchors <a href="url">title</a> -> title(url)
        md = re.sub(
            r"<a\b[^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>",
            r"\2(\1)",
            md,
            flags=re.IGNORECASE | re.DOTALL,
        )
        md = re.sub(
            r"<a\b[^>]*href='([^']+)'[^>]*>(.*?)</a>",
            r"\2(\1)",
            md,
            flags=re.IGNORECASE | re.DOTALL,
        )

        # Remove kramdown attribute blocks like {: .centered}
        md = re.sub(r"\{:\s*[^}]*\}", "", md)

        # Remove image markdown (both inline and reference-style)
        md = re.sub(r"!\[[^\]]*\]\([^\)]*\)", "", md)  # inline image
        md = re.sub(r"!\[[^\]]*\]\[[^\]]*\]", "", md)  # reference image

        # Rewrite Markdown links to title(url)
        # 1) Inline: [title](url) -> title(url), avoid images ![...](...)
        # md = re.sub(r"(?<!!)\[([^\]]+)\]\(([^\)]+)\)", r"\1(\2)", md)

        # 2) Reference-style: [title][id] -> title(url) if id defined
        # Build a map of [id]: url from definitions
        ref_defs = dict(
            re.findall(r"^\s*\[([^\]]+)\]:\s*(\S+)", md, flags=re.MULTILINE)
        )

        def _replace_ref_link(m: re.Match) -> str:
            text, ref = m.group(1), m.group(2)
            url = ref_defs.get(ref)
            return f"{text}({url})" if url else text

        # md = re.sub(r"\[([^\]]+)\]\[([^\]]+)\]", _replace_ref_link, md)

        # Keep autolinks and bare URLs as-is

        # Remove inline footnote references like [^1]
        md = re.sub(r"\[\^[^\]]+\]", "", md)

        # Remove reference definitions (e.g., [id]: url "title") after rewriting
        lines = md.splitlines(True)
        out_lines: list[str] = []
        skip_block = False
        for line in lines:
            if skip_block:
                if line.startswith("    ") or line.startswith("\t"):
                    # continuation of a footnote definition block
                    continue
                else:
                    skip_block = False
            # Footnote definition start
            if re.match(r"^\s*\[\^[^\]]+\]:\s*", line):
                skip_block = True
                continue
            # Link reference definition (single line)
            if re.match(r"^\s*\[[^\]]+\]:\s*", line):
                continue
            out_lines.append(line)
        md = "".join(out_lines)

        # Remove LaTeX environments like \begin{equation} ... \end{equation}
        md = re.sub(r"\\begin\{[^}]+\}.*?\\end\{[^}]+\}", "", md, flags=re.DOTALL)

        # Remove block math $$...$$
        md = re.sub(r"\$\$.*?\$\$", "", md, flags=re.DOTALL)

        # Remove display math \[ ... \]
        md = re.sub(r"\\\[.*?\\\]", "", md, flags=re.DOTALL)

        # Remove inline math \( ... \)
        md = re.sub(r"\\\(.*?\\\)", "", md, flags=re.DOTALL)

        # Remove inline math $...$ (non-greedy, avoid $$ handled above)
        md = re.sub(r"(?<!\$)\$[^\$\n]+\$(?!\$)", "", md)

        # Remove simple LaTeX commands like \alpha, \textbf{...}, \LaTeX, etc.
        md = re.sub(r"\\[a-zA-Z]+(\[[^\]]*\])?(\{[^}]*\})?", "", md)

        return md

    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Remove YAML front matter (tolerate BOM and require line-bounded markers)
            front_matter = ""
            match = re.search(r"^\ufeff?---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
            if match:
                front_matter = match.group(1)
                content = content[match.end() :]

            file_title = os.path.splitext(os.path.basename(file_path))[0]
            try:
                if front_matter:
                    yaml_data = yaml.safe_load(front_matter)
                    if isinstance(yaml_data, dict) and "title" in yaml_data:
                        file_title = str(yaml_data["title"])  # best-effort
            except yaml.YAMLError as e:
                print(f"Error parsing YAML in {file_path}: {e}")

            combined_content += f"# {file_title}\n"

            # Strip links, images, refs, footnotes to leave plain text
            content = strip_links_images_and_footnotes(content)

            combined_content += content
            combined_content += "\n\n"
    return combined_content


def _basename_without_lang(path: str) -> str | None:
    """Extract base name (YYYY-MM-DD-title) from an original path ending with -en.md.

    Example: original/2025-08-24-links-en.md -> 2025-08-24-links
    """
    name = os.path.basename(path)
    for orig in ("en", "zh", "ja"):
        suffix = f"-{orig}.md"
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return None


def _post_path_for_lang(base: str, lang: str) -> str:
    """Map a base like 2025-08-24-links to a target post path in _posts/lang.

    Example: ("2025-08-24-links", "zh") -> _posts/zh/2025-08-24-links-zh.md
    """
    return os.path.join("_posts", lang, f"{base}-{lang}.md")


def build_pdf_for_language(lang: str, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    # Helper: first existing path in list
    def pick(existing_paths: list[str]) -> str | None:
        for p in existing_paths:
            if os.path.exists(p):
                return p
        return None

    # Build sources by mirroring ENGLISH_CANDIDATES into the target language posts.
    sources: list[str] = []

    bases: list[str] = []
    for p in ENGLISH_CANDIDATES:
        base = _basename_without_lang(p)
        if base:
            bases.append(base)

    for base in bases:
        target_path = _post_path_for_lang(base, lang)
        if os.path.exists(target_path):
            sources.append(target_path)
        else:
            # If the exact post isn't available in target language, skip it.
            print(f"Missing for {lang}: {target_path}")

    # Ensure we have something to build
    if not sources:
        print(f"Skip {lang}: no source files found for building.")
        return

    # Keep exactly 9 posts as requested (order preserved by ENGLISH_CANDIDATES)

    try:
        tmpdir = tempfile.mkdtemp(prefix=f"epubpdf-{lang}-")
        combined_md_path = os.path.join(tmpdir, f"lzwjava-essays-{lang}.md")
        with open(combined_md_path, "w", encoding="utf-8") as tmp_file:
            # Title page + metadata header
            today = datetime.now().strftime("%Y-%m-%d")
            # Only the book title should appear on the first page.
            # We keep metadata minimal: only 'title'.
            body = combine_markdown(sources)
            tmp_file.write(body)

        # Build content PDF via pandoc (with TOC), and a separate LaTeX title page, then merge.
        print(
            f"Converting to PDF ({language_display_name(lang)}): lzwjava-essays-{lang}.pdf"
        )
        final_pdf_file = os.path.join(output_dir, f"lzwjava-essays-{lang}.pdf")
        content_pdf_file = os.path.join(tmpdir, f"content-{lang}.pdf")
        title_pdf_file = os.path.join(tmpdir, f"title-{lang}.pdf")

        # Create a clean title page as a standalone PDF (localized)
        book_title, book_subtitle, toc_title = _localize_book_strings(lang)
        title_ok = generate_title_page_pdf(
            title=book_title,
            subtitle=book_subtitle,
            lang=lang,
            output_pdf_path=title_pdf_file,
            font_size_pt=48,
        )
        if not title_ok:
            print("Failed to generate title page; skipping merge.")
            return

        # Build the content (with TOC on its own page). Avoid pandoc titlepage.
        try:
            ok = text_to_pdf_from_markdown(
                input_markdown_path=combined_md_path,
                output_pdf_path=content_pdf_file,
                dry_run=False,
                title_page=False,
                toc=True,
                toc_depth=2,
                toc_title=toc_title,
                toc_own_page=True,
            )
            if not ok:
                print(f"Pandoc failed for content PDF: {content_pdf_file}")
                return
        except Exception as e:
            print(f"Error converting content to {content_pdf_file}: {e}")
            return

        # Merge title page + content
        merged = merge_pdfs([title_pdf_file, content_pdf_file], final_pdf_file)
        if merged:
            print(f"Wrote {final_pdf_file}")
    except Exception as e:
        print(f"Error processing {lang}: {e}")
    finally:
        if "tmpdir" in locals() and os.path.isdir(tmpdir):
            shutil.rmtree(tmpdir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="Build curated PDFs across languages.")
    parser.add_argument(
        "-o",
        "--output_dir",
        help="Output directory for the generated PDF files.",
        default=OUTPUT_DIRECTORY,
    )
    parser.add_argument(
        "--langs",
        nargs="*",
        help="Optional list of language codes to build (default: detected).",
    )
    args = parser.parse_args()

    langs_input = args.langs if args.langs else detect_languages()
    # Restrict to the requested target set, preserving CLI order if provided
    langs = [lang for lang in langs_input if lang in TARGET_LANGS]
    if not langs:
        langs = TARGET_LANGS

    print(f"Languages: {', '.join(langs)}")
    for lang in langs:
        build_pdf_for_language(lang, args.output_dir)


if __name__ == "__main__":
    main()
