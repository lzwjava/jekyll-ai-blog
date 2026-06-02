import os
import json

CACHE_DIR = "cache"

from translate_client import translate_text  # noqa: E402


def load_cache_for_lang(target_lang):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(CACHE_DIR, f"{target_lang}.json")
    cache = {}
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as cf:
            cache = json.load(cf)
    return cache, cache_file


def save_cache_for_lang(cache, cache_file):
    with open(cache_file, "w", encoding="utf-8") as cf:
        json.dump(cache, cf, ensure_ascii=False, indent=4)


def translate_text_with_cache(
    text,
    target_language,
    type="content",
    model="deepseek",
    front_matter_prompt=None,
    original_lang=None,
):
    cache, cache_file = load_cache_for_lang(target_language)
    cache_key = f"{text}"

    if cache_key in cache:
        return cache[cache_key]

    translated_text = translate_text(
        text, target_language, type, model, front_matter_prompt, original_lang
    )
    cache[cache_key] = translated_text
    save_cache_for_lang(cache, cache_file)
    return translated_text


if __name__ == "__main__":
    print("Debug: Running main test translation")
    text = translate_text_with_cache(
        "Hi, it is sunny today. Hahaa...", "ja", model="mistral", original_lang="en"
    )
    print(f"Debug: Final translated text: {text}")
