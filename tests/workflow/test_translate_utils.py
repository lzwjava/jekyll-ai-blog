import unittest
import sys
import os

# Add the scripts directory to the path so we can import translate_utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))

from translation.translate_utils import (
    detect_language_with_langid,
    validate_translated_languages,
    _map_target_code,
)


class TestTranslateUtils(unittest.TestCase):
    def test_detect_language_with_langid_english(self):
        """Test language detection for English text"""
        text = "Hello world, this is a test sentence in English."
        lang, confidence = detect_language_with_langid(text)
        self.assertEqual(lang, "en")
        self.assertIsInstance(confidence, float)

    def test_detect_language_with_langid_spanish(self):
        """Test language detection for Spanish text"""
        text = "Hola mundo, esta es una oración de prueba en español."
        lang, confidence = detect_language_with_langid(text)
        self.assertEqual(lang, "es")
        self.assertIsInstance(confidence, float)

    def test_detect_language_with_langid_french(self):
        """Test language detection for French text"""
        text = "Bonjour le monde, ceci est une phrase de test en français."
        lang, confidence = detect_language_with_langid(text)
        self.assertEqual(lang, "fr")
        self.assertIsInstance(confidence, float)

    def test_detect_language_with_langid_german(self):
        """Test language detection for German text"""
        text = "Hallo Welt, das ist ein Testsatz auf Deutsch."
        lang, confidence = detect_language_with_langid(text)
        self.assertEqual(lang, "de")
        self.assertIsInstance(confidence, float)

    def test_detect_language_with_langid_chinese(self):
        """Test language detection for Chinese text"""
        text = "你好世界，这是一个中文测试句子。"
        lang, confidence = detect_language_with_langid(text)
        self.assertEqual(lang, "zh")
        self.assertIsInstance(confidence, float)

    def test_detect_language_with_langid_japanese(self):
        """Test language detection for Japanese text"""
        text = "こんにちは世界、これは日本語のテスト文です。"
        lang, confidence = detect_language_with_langid(text)
        self.assertEqual(lang, "ja")
        self.assertIsInstance(confidence, float)

    def test_detect_language_with_langid_empty_text(self):
        """Test language detection for empty text"""
        lang, confidence = detect_language_with_langid("")
        self.assertIsNone(lang)
        self.assertEqual(confidence, 0.0)

    def test_detect_language_with_langid_whitespace_only(self):
        """Test language detection for whitespace-only text"""
        lang, confidence = detect_language_with_langid("   \n\t  ")
        self.assertIsNone(lang)
        self.assertEqual(confidence, 0.0)

    # TODO: analyze_text_languages function not implemented yet
    # def test_analyze_text_languages_mixed_text(self):
    #     """Test language analysis for mixed language text"""
    #     text = "Hello world this is a longer sentence. Hola mundo esta es una oracion mas larga. Bonjour le monde ceci est une phrase plus longue."
    #     results = analyze_text_languages(text, min_confidence=-1000)  # Lower threshold since langid uses negative log probabilities
    #     self.assertIsInstance(results, list)
    #
    #     # Check that each result has the expected structure
    #     for result in results:
    #         self.assertIn('text', result)
    #         self.assertIn('language', result)
    #         self.assertIn('confidence', result)
    #         self.assertIsInstance(result['confidence'], float)
    #
    # def test_analyze_text_languages_english_only(self):
    #     """Test language analysis for English-only text"""
    #     text = "This is a test sentence. This is another test sentence. And this is a third one."
    #     results = analyze_text_languages(text, min_confidence=-1000)  # Lower threshold since langid uses negative log probabilities
    #
    #     # All detected languages should be English
    #     for result in results:
    #         self.assertEqual(result['language'], 'en')
    #
    # def test_analyze_text_languages_empty_text(self):
    #     """Test language analysis for empty text"""
    #     results = analyze_text_languages("")
    #     self.assertEqual(results, [])
    #
    # def test_analyze_text_languages_short_sentences(self):
    #     """Test language analysis with very short sentences (should be filtered out)"""
    #     text = "Hi. Yes. No. Maybe so."
    #     results = analyze_text_languages(text, min_confidence=-1000)
    #     # Short sentences (<=10 chars) should be filtered out
    #     self.assertEqual(len(results), 0)

    def test_validate_translated_languages_valid_text(self):
        """Test validation with valid non-empty text"""
        try:
            validate_translated_languages("This is valid translated text", "en")
        except RuntimeError:
            self.fail("validate_translated_languages raised RuntimeError unexpectedly")

    def test_validate_translated_languages_empty_text(self):
        """Test validation with empty text should raise RuntimeError"""
        with self.assertRaises(RuntimeError):
            validate_translated_languages("", "en")

    def test_validate_translated_languages_whitespace_only(self):
        """Test validation with whitespace-only text should raise RuntimeError"""
        with self.assertRaises(RuntimeError):
            validate_translated_languages("   \n\t  ", "en")

    def test_validate_translated_languages_source_file_param(self):
        """Ensure providing source_file does not affect validation for non-empty text"""
        # Use non-empty text since empty text should always raise
        try:
            validate_translated_languages(
                "dummy non-empty text",
                "es",
                source_file="path/to/2025-08-23-growth-reason-en.md",
            )
        except RuntimeError:
            self.fail(
                "validate_translated_languages raised RuntimeError unexpectedly for non-empty text with source_file"
            )

    def test_map_target_code(self):
        """Test the _map_target_code function"""
        test_cases = {
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
            "unknown": "unknown",  # Should return unchanged
        }

        for input_code, expected_output in test_cases.items():
            self.assertEqual(_map_target_code(input_code), expected_output)


if __name__ == "__main__":
    unittest.main()
