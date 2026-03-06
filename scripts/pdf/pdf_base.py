import os
import subprocess
import platform
import tempfile
import shutil
from typing import Iterable

try:
    # pypdf is listed in requirements/requirements.local.txt
    from pypdf import PdfReader, PdfWriter
except Exception:  # pragma: no cover - optional import for environments without pypdf
    PdfReader = None  # type: ignore
    PdfWriter = None  # type: ignore


def text_to_pdf_from_markdown(
    input_markdown_path,
    output_pdf_path,
    dry_run=False,
    extra_pandoc_args=None,
    *,
    pt: int = 16,
    title_page: bool = False,
    toc: bool = False,
    toc_depth: int = 2,
    toc_title: str | None = None,
    toc_own_page: bool = True,
):
    if dry_run:
        print(f"Dry run: Would generate PDF from: {input_markdown_path}")
        return

    print(f"Generating PDF from: {input_markdown_path}")

    CJK_FONT = "Heiti SC"
    GEOMETRY = "left=1.4cm, top=.8cm, right=1.4cm, bottom=1.8cm, footskip=.5cm"

    if not os.path.exists(input_markdown_path):
        raise Exception(f"Input file does not exist: {input_markdown_path}")

    lang = os.path.basename(input_markdown_path).split("-")[-1].split(".")[0]

    if platform.system() == "Darwin":
        if lang == "hi":
            CJK_FONT = "Kohinoor Devanagari"
        elif lang == "ar":
            CJK_FONT = "Geeza Pro"
        elif lang in ["en", "fr", "de", "es"]:
            CJK_FONT = "Helvetica"
        elif lang == "zh":
            CJK_FONT = "PingFang SC"
        elif lang == "hant":
            CJK_FONT = "PingFang TC"
        elif lang == "ja":
            CJK_FONT = "Hiragino Sans"
        else:
            CJK_FONT = "Arial Unicode MS"
    else:
        if lang == "hi":
            CJK_FONT = "Noto Sans Devanagari"
        elif lang == "ar":
            CJK_FONT = "Noto Naskh Arabic"
        elif lang in ["en", "fr", "de", "es"]:
            CJK_FONT = "DejaVu Sans"
        elif lang == "zh":
            CJK_FONT = "Noto Sans CJK SC"
        elif lang == "hant":
            CJK_FONT = "Noto Sans CJK TC"
        elif lang == "ja":
            CJK_FONT = "Noto Sans CJK JP"
        else:
            CJK_FONT = "Noto Sans"
    command = [
        "pandoc",
        input_markdown_path,
        "-o",
        output_pdf_path,
        "-f",
        # Disable YAML metadata block and raw LaTeX to avoid alias/\n issues
        "markdown-yaml_metadata_block-raw_tex",
        "--pdf-engine",
        "xelatex",
        "-V",
        f"romanfont={CJK_FONT}",
        "-V",
        f"mainfont={CJK_FONT}",
        "-V",
        f"CJKmainfont={CJK_FONT}",
        "-V",
        f"CJKsansfont={CJK_FONT}",
        "-V",
        f"CJKmonofont={CJK_FONT}",
        "-V",
        f"geometry:{GEOMETRY}",
        "-V",
        f"classoption={pt}pt",
        "-V",
        "CJKoptions=Scale=1.1",
        "-V",
        "linestretch=1.5",
    ]

    # Book-like toggles
    if toc:
        command.extend(["--toc", "--toc-depth", str(int(toc_depth))])
        if toc_title:
            command.extend(["-V", f"toc-title={toc_title}"])
        if toc_own_page:
            command.extend(["-V", "toc-own-page=true"])
    if title_page:
        # Relying on pandoc's titlepage can be tricky when TOC is also used.
        # Keep this available, but for book builds prefer a separate LaTeX title page.
        command.extend(["-V", "titlepage=true"])

    # Allow callers to override/extend pandoc behavior (e.g., --toc)
    if extra_pandoc_args:
        if not isinstance(extra_pandoc_args, (list, tuple)):
            raise TypeError("extra_pandoc_args must be a list or tuple of strings")
        command.extend([str(x) for x in extra_pandoc_args])

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Pandoc error for {output_pdf_path}: {result.stderr}")
        # raise Exception(f"Pandoc failed for {input_markdown_path}")
        return False

    print(f"PDF content written to {output_pdf_path}")
    return True


def _font_for_lang(lang: str) -> str:
    """Return a good default font for the language and platform, matching pandoc settings."""
    if platform.system() == "Darwin":
        if lang == "hi":
            return "Kohinoor Devanagari"
        if lang == "ar":
            return "Geeza Pro"
        if lang in ["en", "fr", "de", "es"]:
            return "Helvetica"
        if lang == "zh":
            return "PingFang SC"
        if lang == "hant":
            return "PingFang TC"
        if lang == "ja":
            return "Hiragino Sans"
        return "Arial Unicode MS"
    else:
        if lang == "hi":
            return "Noto Sans Devanagari"
        if lang == "ar":
            return "Noto Naskh Arabic"
        if lang in ["en", "fr", "de", "es"]:
            return "DejaVu Sans"
        if lang == "zh":
            return "Noto Sans CJK SC"
        if lang == "hant":
            return "Noto Sans CJK TC"
        if lang == "ja":
            return "Noto Sans CJK JP"
        return "Noto Sans"


def generate_title_page_pdf(
    *,
    title: str,
    output_pdf_path: str,
    subtitle: str | None = None,
    lang: str = "en",
    font_size_pt: int = 48,
    geom: str = "left=1.4cm, top=.8cm, right=1.4cm, bottom=1.8cm, footskip=.5cm",
) -> bool:
    """Render a single-page PDF title page via xelatex.

    - Uses fontspec + \setmainfont with a language-appropriate font.
    - Suppresses page numbers and centers the title.
    """
    font_name = _font_for_lang(lang)

    # Minimal LaTeX document for a clean title page
    lines = [
        r"\documentclass[12pt]{article}",
        r"\usepackage{fontspec}",
        r"\usepackage{geometry}",
        rf"\geometry{{{geom}}}",
        rf"\setmainfont{{{font_name}}}",
        r"\pagenumbering{gobble}",
        r"\begin{document}",
        r"\thispagestyle{empty}",
        r"\vspace*{0.25\textheight}",
        r"\begin{center}",
        rf"{{\fontsize{{{font_size_pt}}}{{{int(font_size_pt * 1.15)}}}\selectfont {title}\par}}",
    ]
    if subtitle:
        lines.extend(
            [
                r"\vspace{1.2em}",
                rf"{{\Large {subtitle}\par}}",
            ]
        )
    lines.extend(
        [
            r"\end{center}",
            r"\end{document}",
            "",
        ]
    )

    workdir = tempfile.mkdtemp(prefix="titlepage-")
    tex_path = os.path.join(workdir, "titlepage.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    try:
        cmd = [
            "xelatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-output-directory",
            workdir,
            tex_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("Failed to compile title page with xelatex:")
            print(result.stderr)
            return False

        pdf_src = os.path.join(workdir, "titlepage.pdf")
        if not os.path.exists(pdf_src):
            print("Title page PDF was not produced by xelatex.")
            return False

        os.makedirs(os.path.dirname(output_pdf_path) or ".", exist_ok=True)
        shutil.copyfile(pdf_src, output_pdf_path)
        print(f"Title page written to {output_pdf_path}")
        return True
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def merge_pdfs(inputs: Iterable[str], output_pdf_path: str) -> bool:
    """Merge multiple PDFs into one using pypdf. Returns True on success."""
    if PdfWriter is None or PdfReader is None:
        print("pypdf not available; cannot merge PDFs.")
        return False

    writer = PdfWriter()
    added_any = False

    for path in inputs:
        if not path or not os.path.exists(path):
            print(f"Skipping missing PDF: {path}")
            continue
        try:
            reader = PdfReader(path)
            for page in reader.pages:
                writer.add_page(page)
            added_any = True
        except Exception as e:
            print(f"Error reading {path}: {e}")

    if not added_any:
        print("No valid PDFs to merge.")
        return False

    os.makedirs(os.path.dirname(output_pdf_path) or ".", exist_ok=True)
    with open(output_pdf_path, "wb") as f:
        writer.write(f)
    print(f"Merged PDF written to {output_pdf_path}")
    return True
