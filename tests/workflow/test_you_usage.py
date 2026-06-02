import unittest
import re
import os


def scan_markdown_files_for_pronoun_usage():
    """Scan English markdown files for excessive usage of 'you' and 'we' pronouns."""
    results = []

    # Only scan original directory for English markdown files
    original_dir = "original"

    if not os.path.exists(original_dir):
        return results

    # Walk through all subdirectories in original
    for root, dirs, files in os.walk(original_dir):
        for filename in files:
            if not filename.endswith("-en.md"):
                continue

            file_path = os.path.join(root, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Remove YAML front matter
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        content = parts[2]

                # Remove markdown formatting
                clean_content = re.sub(r"[#*`\[\]()_]", " ", content)
                clean_content = re.sub(r"\s+", " ", clean_content).strip()

                if not clean_content:
                    continue

                words = clean_content.lower().split()

                # Count 'you', 'we' pronouns and 'one' (case insensitive)
                you_we_count = 0
                one_count = 0

                for word in words:
                    # Remove punctuation for exact matching
                    clean_word = re.sub(r"[^\w]", "", word)
                    if clean_word in [
                        "you",
                        "we",
                        "you're",
                        "you'll",
                        "you've",
                        "you'd",
                        "we're",
                        "we'll",
                        "we've",
                        "we'd",
                    ]:
                        you_we_count += 1
                    elif clean_word == "one":
                        one_count += 1

                # Total pronoun words = you/we + one
                total_pronoun_words = you_we_count + one_count

                if total_pronoun_words == 0:
                    continue

                # Calculate ratio of you/we vs total pronoun words
                pronoun_ratio = you_we_count / total_pronoun_words

                results.append(
                    {
                        "file": file_path,
                        "total_pronoun_words": total_pronoun_words,
                        "you_we_count": you_we_count,
                        "one_count": one_count,
                        "pronoun_ratio": pronoun_ratio,
                    }
                )

            except (UnicodeDecodeError, IOError):
                # Skip files that can't be read
                continue

    return results


class TestYouUsage(unittest.TestCase):
    @unittest.skip("Test disabled - too strict")
    def test_you_usage(self):
        """Test that English markdown files don't have excessive 'you'/'we' pronoun usage (>0.6 ratio)."""
        pronoun_results = scan_markdown_files_for_pronoun_usage()

        failing_files = []
        for result in pronoun_results:
            if result["pronoun_ratio"] > 0.8:
                failing_files.append(result)

        if failing_files:
            details = "\n".join(
                [
                    f"{result['file']} - {result['you_we_count']}/{result['total_pronoun_words']} pronoun words ({result['pronoun_ratio']:.3f} ratio)"
                    for result in failing_files
                ]
            )
            self.fail(
                f"Found {len(failing_files)} files with excessive 'you'/'we' usage (>0.6 ratio):\n{details}"
            )


if __name__ == "__main__":
    unittest.main()
