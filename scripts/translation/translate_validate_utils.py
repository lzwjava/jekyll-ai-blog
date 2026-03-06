def validate_length(text):
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    length = len(text)
    if not 1 <= length <= 200000:
        raise ValueError(f"text length {length} outside allowed range [1, 200000]")


def clean_response(text):
    if not isinstance(text, str):
        raise RuntimeError("Model returned non-text response")
    return text.strip()


def check_commentary(translated):
    indicators = [
        "the output is",
        "output is",
        "translated title",
        "the translation is",
        "translation is",
        "translated:",
        "result:",
        "output:",
        "return only",
        "return only the translated",
    ]
    low = translated.lower()
    for ind in indicators:
        if low.startswith(ind):
            raise RuntimeError("Model included commentary")

    # Check for markdown code blocks
    if low.startswith("```markdown"):
        raise RuntimeError("Model included markdown code blocks")


def check_title_strict(title, target_lang):
    """Strict title validation - removes quotes and special chars based on language"""
    if "\n" in title.strip():
        raise RuntimeError("Model returned multi-line title")

    # Define forbidden characters - only double quotes for all languages
    forbidden_chars = {
        "ja": ['"'],
        "zh": ['"'],
        "hant": ['"'],
        "hi": [],
        "ar": ['"'],
        "es": ['"'],
        "fr": ['"'],
        "de": ['"'],
        "en": ['"'],
    }

    # Get forbidden chars for target language, default to only double quotes
    chars_to_remove = forbidden_chars.get(target_lang, ['"'])

    # Check if title contains any forbidden characters
    for char in chars_to_remove:
        if char in title:
            raise RuntimeError(
                f"Title contains forbidden character: {char} title: {title}"
            )

    return title.strip()


def check_markdown_table_formatting(text):
    """Fix markdown table formatting by adding blank lines between headers and tables"""
    import re

    lines = text.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        fixed_lines.append(line)

        # Check if current line is a header (starts with #)
        if re.match(r"^#+\s+", line.strip()):
            # Look for the next non-empty line
            next_line_idx = i + 1
            while next_line_idx < len(lines) and not lines[next_line_idx].strip():
                next_line_idx += 1

            # Check if the next non-empty line is a table (starts with |)
            if next_line_idx < len(lines) and lines[next_line_idx].strip().startswith(
                "|"
            ):
                # Add a blank line if there isn't one already
                if i + 1 < len(lines) and lines[i + 1].strip():
                    fixed_lines.append("")

    return "\n".join(fixed_lines)


def check_prohibited_zh_terms(translated_text: str, target_lang: str) -> None:
    """Raise if translated Chinese text contains known forbidden phrases."""
    if target_lang != "zh":
        return
    if not isinstance(translated_text, str):
        return

    if "志炜" in translated_text:
        raise RuntimeError("Translated text contains forbidden Chinese term: 志炜")


def check_yin_wang_mistranslation(
    original_text: str, translated_text: str, target_lang: str
):
    """Raise if 'Yin Wang' is mistranslated in Chinese titles/content.

    Rules:
    - If target language is zh
    - And the original text contains 'Yin Wang' (case-sensitive match; common form)
    - And the translated text contains either '阴王' or '王寅'
    Then raise a RuntimeError to signal a bad translation. The preferred translation is '王垠'.
    """
    if not isinstance(original_text, str) or not isinstance(translated_text, str):
        return
    if target_lang != "zh":
        return
    if "Yin Wang" not in original_text:
        return
    if ("阴王" in translated_text) or ("王寅" in translated_text):
        raise RuntimeError(
            "Incorrect translation for 'Yin Wang': found '阴王' or '王寅'; expected '王垠'."
        )
