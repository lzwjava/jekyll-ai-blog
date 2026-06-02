import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.audio.audio_pipeline import split_into_sentences, split_text


class TestAudioPipeline(unittest.TestCase):
    def test_split_into_sentences_english(self):
        # Test English sentence splitting
        text = "This is sentence one. This is sentence two! Is this sentence three? Yes it is."
        sentences = split_into_sentences(text)

        expected = [
            "This is sentence one.",
            "This is sentence two!",
            "Is this sentence three?",
            "Yes it is.",
        ]
        self.assertEqual(sentences, expected)

    def test_split_into_sentences_chinese(self):
        # Test Chinese sentence splitting
        text = "这是第一句话。这是第二句话！这是第三句话？是的。"
        sentences = split_into_sentences(text)

        expected = ["这是第一句话。", "这是第二句话！", "这是第三句话？", "是的。"]
        self.assertEqual(sentences, expected)

    def test_split_into_sentences_empty(self):
        # Test with empty string
        text = ""
        sentences = split_into_sentences(text)
        self.assertEqual(sentences, [""])

    def test_split_into_sentences_no_punctuation(self):
        # Test with text that has no sentence endings
        text = "This is just one long text without proper punctuation"
        sentences = split_into_sentences(text)
        self.assertEqual(sentences, [text])

    def test_split_text_short_text(self):
        # Test with text shorter than max_bytes
        text = "This is a short text."
        chunks = split_text(text, max_bytes=1000)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0], text)

    def test_split_text_multiple_sentences(self):
        # Test with multiple sentences that fit in one chunk
        text = "First sentence. Second sentence. Third sentence."
        chunks = split_text(text, max_bytes=1000)
        self.assertEqual(len(chunks), 1)
        self.assertIn("First sentence.", chunks[0])
        self.assertIn("Second sentence.", chunks[0])
        self.assertIn("Third sentence.", chunks[0])

    def test_split_text_exceeds_max_bytes(self):
        # Test with text that exceeds max_bytes
        long_sentence = "A" * 100 + ". "
        text = long_sentence * 50  # Create very long text
        chunks = split_text(text, max_bytes=500)

        # Should create multiple chunks
        self.assertGreater(len(chunks), 1)

        # Each chunk should not exceed max_bytes (with some tolerance for UTF-8 encoding)
        for chunk in chunks:
            self.assertLessEqual(len(chunk.encode("utf-8")), 600)  # Small tolerance

    def test_split_text_single_long_sentence(self):
        # Test with a single sentence that exceeds max_bytes
        long_text = "This is a very long sentence that contains many words and commas, semicolons; and colons: which should be used as split points when the sentence is too long for a single chunk."
        chunks = split_text(long_text, max_bytes=50)

        # Should split the sentence at delimiters
        self.assertGreater(len(chunks), 1)

        # Verify each chunk is not empty
        for chunk in chunks:
            self.assertGreater(len(chunk.strip()), 0)

    def test_split_text_chinese_delimiters(self):
        # Test with Chinese delimiters
        text = "这是第一部分，这是第二部分；这是第三部分：这是第四部分。"
        chunks = split_text(text, max_bytes=30)

        # Should split at Chinese delimiters when needed
        self.assertGreater(len(chunks), 1)

        # Verify each chunk is not empty
        for chunk in chunks:
            self.assertGreater(len(chunk.strip()), 0)

    def test_split_text_empty_string(self):
        # Test with empty string
        text = ""
        chunks = split_text(text)
        self.assertEqual(chunks, [])

    def test_split_text_whitespace_only(self):
        # Test with whitespace-only text
        text = "   \n   \t   "
        chunks = split_text(text)
        self.assertEqual(chunks, [])


if __name__ == "__main__":
    unittest.main()
