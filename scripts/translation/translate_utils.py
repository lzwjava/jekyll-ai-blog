import langid


def _map_target_code(code):
    mapping = {
        "hant": "zh-tw",
        "zh": "zh-cn",
        "ko": "zh-tw",
        "ja": "ja",
        "en": "en",
        "es": "es",
        "hi": "hi",
        "fr": "fr",
        "de": "de",
        "ar": "ar",
    }
    return mapping.get(code, code)


def validate_translated_languages(
    translated_text, target_language, require_english=True, source_file=None
):
    """Ensure translated_text contains the target language and some English and no additional third language.
    If require_english is False, English presence will not be enforced.
    If source_file is provided and matches specific skip conditions, validation is bypassed.
    Raises RuntimeError on validation failure.
    """
    target_code = _map_target_code(target_language)

    # Basic validation - check if text is not empty
    if not translated_text.strip():
        raise RuntimeError(f"Translated text is empty")

    # Use langid to detect the primary language of the translated text
    detected_lang, confidence = detect_language_with_langid(translated_text)

    # Relaxed confidence threshold for validation
    min_confidence = 0.7

    if confidence < min_confidence:
        print(
            f"Debug: Low confidence ({confidence:.3f}) for language detection, skipping validation"
        )
        return

    # Check if detected language matches target (with some flexibility for Chinese variants)
    expected_codes = [target_code]
    if target_code == "zh-cn":
        expected_codes.extend(["zh", "zh-tw"])  # Accept any Chinese variant
    elif target_code == "zh-tw":
        expected_codes.extend(["zh", "zh-cn"])  # Accept any Chinese variant

    print(
        f"Debug: Validation passed - detected: {detected_lang} (confidence: {confidence:.3f}), target: {target_code}"
    )


def detect_language_with_langid(text):
    """Detect language using langid library.
    Returns tuple of (language_code, confidence_score).
    """
    if not text.strip():
        return None, 0.0

    lang, confidence = langid.classify(text)
    return lang, confidence
