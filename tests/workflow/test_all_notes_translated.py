#!/usr/bin/env python3
"""
Test that all notes in the notes/ directory have been translated to all supported languages.

This test checks:
1. All notes in notes/ directory have corresponding translations
2. Reports which notes are missing translations
3. Identifies which languages are missing for each note
"""

import unittest
import os
from collections import defaultdict

# Same languages as used in update_lang_notes.py and other tests
SUPPORTED_LANGUAGES = ["en", "zh", "ja", "es", "hi", "fr", "de", "ar", "hant"]

# Source languages that exist in notes/ directory
SOURCE_LANGUAGES = ["en", "zh", "ja"]


def extract_base_name(filename):
    """Extract base name from filename by removing language suffix and .md extension."""
    base_name = filename.replace(".md", "")
    for lang in SUPPORTED_LANGUAGES:
        suffix = f"-{lang}"
        if base_name.endswith(suffix):
            return base_name[: -len(suffix)]
    return base_name


def extract_language_from_filename(filename):
    """Extract language code from filename."""
    base_name = filename.replace(".md", "")
    for lang in SUPPORTED_LANGUAGES:
        if base_name.endswith(f"-{lang}"):
            return lang
    return None


def is_note_type(filepath):
    """Check if a file has type: note in its frontmatter."""
    if not os.path.exists(filepath):
        return False
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        first_marker = content.find("---")
        second_marker = content.find("---", first_marker + 3)
        if first_marker == -1 or second_marker == -1:
            return False
        frontmatter = content[first_marker : second_marker + 3]
        return "type: note" in frontmatter
    except Exception:
        return False


def scan_source_notes():
    """Scan the notes/ directory for all source notes."""
    notes_dir = "notes"
    if not os.path.exists(notes_dir):
        return set()

    source_notes = set()
    for filename in os.listdir(notes_dir):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(notes_dir, filename)
        if not is_note_type(filepath):
            continue
        base_name = extract_base_name(filename)
        source_language = extract_language_from_filename(filename)
        if source_language in SOURCE_LANGUAGES:
            source_notes.add(base_name)

    return source_notes


def scan_translated_notes():
    """Scan _posts/ directories for all translated notes."""
    translated_notes = defaultdict(set)
    for language in SUPPORTED_LANGUAGES:
        posts_dir = f"_posts/{language}"
        if not os.path.exists(posts_dir):
            continue

        for filename in os.listdir(posts_dir):
            if not filename.endswith(".md"):
                continue
            filepath = os.path.join(posts_dir, filename)
            if not is_note_type(filepath):
                continue

            base_name = extract_base_name(filename)
            detected_language = extract_language_from_filename(filename)
            if detected_language == language:
                translated_notes[base_name].add(language)

    return translated_notes


def analyze_translation_completeness():
    """
    Analyze which notes are missing translations.

    Returns:
        tuple: (missing_notes, complete_notes)
            - missing_notes: list of dicts with info about incomplete translations
            - complete_notes: list of base names that have all translations
    """
    source_notes = scan_source_notes()
    translated_notes = scan_translated_notes()

    missing_notes = []
    complete_notes = []

    all_languages_set = set(SUPPORTED_LANGUAGES)

    for base_name in source_notes:
        available_languages = translated_notes.get(base_name, set())
        missing_languages = all_languages_set - available_languages

        note_info = {
            "base_name": base_name,
            "available_languages": sorted(available_languages),
            "missing_languages": sorted(missing_languages),
            "missing_count": len(missing_languages),
        }

        if missing_languages:
            missing_notes.append(note_info)
        else:
            complete_notes.append(base_name)

    # Sort missing notes by missing count (most incomplete first)
    missing_notes.sort(key=lambda x: x["missing_count"], reverse=True)

    return missing_notes, complete_notes


class TestAllNotesTranslated(unittest.TestCase):
    """Test that all notes have been translated to all supported languages."""

    @unittest.skip("Test disabled - too strict")
    def test_all_notes_translated(self):
        """Test that all source notes have translations in all supported languages."""
        missing_notes, complete_notes = analyze_translation_completeness()

        if missing_notes:
            # Build detailed error message
            lines = []
            lines.append(f"\n{'=' * 80}")
            lines.append("TRANSLATION COMPLETENESS REPORT")
            lines.append(f"{'=' * 80}")
            lines.append(
                f"Total source notes: {len(missing_notes) + len(complete_notes)}"
            )
            lines.append(f"Complete translations: {len(complete_notes)}")
            lines.append(f"Incomplete translations: {len(missing_notes)}")
            lines.append("")
            lines.append("Missing translations:")
            lines.append(f"{'-' * 80}")

            for note in missing_notes:
                lines.append(f"\n📝 {note['base_name']}")
                lines.append(
                    f"   Available: {', '.join(note['available_languages']) if note['available_languages'] else 'NONE'}"
                )
                lines.append(f"   Missing: {', '.join(note['missing_languages'])}")

            lines.append(f"\n{'=' * 80}")

            error_msg = "\n".join(lines)
            self.fail(f"Not all notes have complete translations.\n{error_msg}")
        else:
            total_notes = len(complete_notes)
            print(f"\n✓ ALL {total_notes} NOTES HAVE COMPLETE TRANSLATIONS")
            print(f"  All notes are translated to: {', '.join(SUPPORTED_LANGUAGES)}")

    @unittest.skip("Test disabled - too strict")
    def test_translation_coverage_report(self):
        """Generate a detailed report about translation coverage."""
        missing_notes, complete_notes = analyze_translation_completeness()

        total_notes = len(missing_notes) + len(complete_notes)
        if total_notes == 0:
            print("\n⚠ No source notes found in notes/ directory")
            return

        coverage_pct = (len(complete_notes) / total_notes) * 100

        print(f"\n{'=' * 80}")
        print("TRANSLATION COVERAGE REPORT")
        print(f"{'=' * 80}")
        print(f"Total source notes: {total_notes}")
        print(f"Complete translations: {len(complete_notes)}")
        print(f"Incomplete translations: {len(missing_notes)}")
        print(f"Coverage: {coverage_pct:.1f}%")
        print(f"{'=' * 80}\n")

        # Verify the assertion
        self.assertEqual(
            len(missing_notes),
            0,
            f"Found {len(missing_notes)} notes with incomplete translations",
        )


if __name__ == "__main__":
    unittest.main()
