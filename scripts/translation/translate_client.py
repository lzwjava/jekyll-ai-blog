import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from scripts.llm.openrouter_client import call_openrouter_api
from scripts.translation.translate_utils import (
    validate_translated_languages,
    detect_language_with_langid,
)
from scripts.translation.translate_validate_utils import (
    validate_length,
    clean_response,
    check_commentary,
    check_title_strict,
    check_markdown_table_formatting,
    check_prohibited_zh_terms,
    check_yin_wang_mistranslation,
)

LANGUAGE_MAP = {
    "ja": "Japanese",
    "es": "Spanish",
    "hi": "Hindi",
    "fr": "French",
    "zh": "Simplified Chinese",
    "hant": "Traditional Chinese (Hong Kong)",
    "en": "English",
    "de": "German",
    "ar": "Arabic",
}

LANGUAGE_MODEL_MAP = {
    "en": "deepseek-v3.1",
    "zh": "deepseek-v3.1",
    "hant": "deepseek-v3.1",
    "ja": "mistral-medium",
    "es": "mistral-medium",
    "hi": "mistral-medium",
    "fr": "mistral-medium",
    "de": "mistral-medium",
    "ar": "mistral-medium",
}


def get_language_specific_preamble(
    target_language: str, kind: str, original_text: str = ""
) -> str:
    """Return additional translation instructions for specific languages.

    Only includes Chinese-specific rules if the original text contains matching terms.
    """
    if target_language == "zh":
        # Fixed term mapping for zh translations
        zh_term_map = {
            "Zhiwei": "智维",
            "Zhiwei Li": "李智维",
            "Li Zhiwei": "李智维",
            "Meitai Technology Services": "美钛技术服务",
            "Neusiri": "思芮",
            "Chongding Conference": "冲顶大会",
            "Fun Live": "趣直播",
            "MianbaoLive": "面包Live",
            "Beijing Dami Entertainment Co.": "北京大米互娱有限公司",
            "Guangzhou Yuyan Middle School": "广州玉岩中学",
            "Yin Wang": "王垠",
        }

        # Check if any of the source terms are in the original text
        # Only include rules for terms that are actually present
        matching_rules = []
        for src, dst in zh_term_map.items():
            if src in original_text:
                matching_rules.append(f"Translate {src} to {dst}.")

        # Only include rules if we found matching terms in the original text
        if not matching_rules:
            return ""

        rules_str = " ".join(matching_rules)
        if kind == "title":
            return (
                "You are a professional translator. You are translating a title "
                "for a Jekyll blog post from English to Chinese. Translate the "
                f"following text to Chinese. {rules_str} Be careful about code "
                "blocks, if not sure, just do not change."
            )
        return (
            "You are a professional translator. You are translating a markdown "
            "file for a Jekyll blog post from English to Chinese. Translate the "
            f"following text to Chinese. {rules_str} Be careful about code "
            "blocks, if not sure, just do not change."
        )
    return ""


def build_prompt_template(target_language, type_, front_matter, original_text=""):
    lang_name = LANGUAGE_MAP.get(target_language, target_language)
    preamble = get_language_specific_preamble(target_language, type_, original_text)
    if type_ == "title":
        tpl = """Translate the following title into {lang}. Return only the translated title without any extra notes, explanations, or repetition of the input text. If the title is already in {lang}, return it as is. If the target language is English, ensure the title is in Title Case.

IMPORTANT: Do not include any quotes, double quotes, special quotation marks (such as ", ', ", ", «, », 「, 」), or other decorative characters around the title.
"""
        tpl = tpl.format(lang=lang_name)
        if preamble:
            tpl = preamble + "\n\n" + tpl
        return tpl
    else:
        head = """Translate the following markdown text into {lang}. Return only the translated content without any additional notes or explanations. If the text is already in {lang}, return it unchanged.

IMPORTANT: When translating markdown content, ensure proper formatting:
- Always add a blank line between headers (lines starting with #) and tables (lines starting with |)
- Maintain proper markdown table structure
- Preserve all original formatting and spacing except where formatting rules require changes
- DO NOT wrap the entire translation in markdown code blocks (```markdown or ```) - the content will be used directly in Jekyll with Kramdown

TRANSLATION RULES:
- Do not translate specific items such as project names, company names, or school names if you are not sure
- For technology terms, new words, and technical concepts, keep them in English instead of translating
- For Chinese translations: Use English for proper nouns and technical terms instead of Chinese transliterations
- For Japanese translations: Use English for technical terms instead of romaji or katakana when appropriate
- For all languages: Prioritize using English for modern technology words, programming terms, and brand names

"""
        if front_matter:
            head += f"{front_matter}\n"
        tpl = head.format(lang=lang_name)
        if preamble:
            tpl = preamble + "\n\n" + tpl
        return tpl


def run_translate(
    text, target, kind, model, front_matter, orig_lang, need_en, source_file=None
):
    validate_length(text)
    if target == orig_lang:
        return text

    # Use language-specific model mapping, ignore the model parameter
    LANGUAGE_MODEL_MAP.get(target, "mistral-medium")
    prompt = build_prompt_template(target, kind, front_matter, text) + "\n\n" + text
    translated = clean_response(call_openrouter_api(prompt, model))
    check_commentary(translated)
    if kind == "title":
        check_title_strict(translated, target)

    # Fix markdown table formatting for content translations
    if kind == "content":
        translated = check_markdown_table_formatting(translated)

    # Validate specific known-name translations for Chinese across all kinds
    check_yin_wang_mistranslation(text, translated, target)
    check_prohibited_zh_terms(translated, target)

    try:
        detect_language_with_langid(translated)
    except Exception:  # nosec B110 — best-effort detection
        pass
    validate_translated_languages(
        translated, target, require_english=need_en, source_file=source_file
    )
    return translated


def translate_text(
    text,
    target_language,
    type="content",
    model="deepseek-v3.2",
    front_matter_prompt=None,
    original_lang=None,
    front_matter=None,
    source_file=None,
):
    """Wrapper function for markdown_translate_client.py compatibility"""
    kind = type  # Map 'type' parameter to 'kind' parameter used in run_translate
    orig_lang = original_lang if original_lang else "en"
    return run_translate(
        text=text,
        target=target_language,
        kind=kind,
        model=model,
        front_matter=front_matter_prompt or front_matter,
        orig_lang=orig_lang,
        need_en=False,
        source_file=source_file,
    )


def cli_translate():
    parser = argparse.ArgumentParser()
    parser.add_argument("text")
    parser.add_argument("--target", required=True)
    parser.add_argument("--type", default="content")
    parser.add_argument("--model", default="deepseek-v3.2")
    parser.add_argument("--front-matter")
    parser.add_argument("--original-lang")
    parser.add_argument("--require-english", action="store_true")
    args = parser.parse_args()

    translated = translate_text(
        text=args.text,
        target_language=args.target,
        type=args.type,
        model=args.model,
        front_matter_prompt=args.front_matter,
        original_lang=args.original_lang,
        front_matter=args.original_lang,
    )
    print(translated)


if __name__ == "__main__":
    cli_translate()
# Demo runs
# python scripts/translation/translate_client.py "Hello world" --target zh --model mistral-medium --original-lang en
# python scripts/translation/translate_client.py "Nice Day" --target ja --type title
