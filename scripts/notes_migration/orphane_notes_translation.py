#!/usr/bin/env python3
"""
Analyze note translation coverage across 9 languages.
Find orphaned notes and translation completeness.
"""

import re
from collections import defaultdict
from pathlib import Path

LANGUAGES = ["ar", "de", "en", "es", "fr", "hant", "hi", "ja", "zh"]
NOTES_DIR = Path("_notes")


def get_note_base_name(filename, lang):
    """Extract base name from filename, removing the language suffix."""
    # Pattern: basename-lang.md -> basename
    pattern = rf"^(.*)-{lang}\.md$"
    match = re.match(pattern, filename)
    if match:
        return match.group(1)
    return None


def analyze_notes():
    """Analyze note translation coverage."""
    # Structure: base_name -> set of languages that have this note
    notes_coverage = defaultdict(set)

    # Reverse mapping: lang -> set of base names
    notes_per_lang = {lang: set() for lang in LANGUAGES}

    # Find all md files
    for lang in LANGUAGES:
        lang_dir = NOTES_DIR / lang
        if not lang_dir.exists():
            print(f"Warning: Directory {lang_dir} does not exist")
            continue

        for md_file in lang_dir.glob("*.md"):
            base_name = get_note_base_name(md_file.name, lang)
            if base_name:
                notes_coverage[base_name].add(lang)
                notes_per_lang[lang].add(base_name)
            else:
                print(f"Warning: Could not parse base name from {md_file}")

    return notes_coverage, notes_per_lang


def print_summary(notes_coverage, notes_per_lang):
    """Print comprehensive analysis."""
    total_unique_notes = len(notes_coverage)
    total_files = sum(len(notes) for notes in notes_per_lang.values())

    print("=== NOTES TRANSLATION ANALYSIS ===\n")

    # Summary statistics
    print("SUMMARY STATISTICS:")
    print(f"- Total unique notes (base names): {total_unique_notes}")
    print(f"- Total translation files: {total_files}")
    print()

    # Coverage per language
    print("NOTES COUNT PER LANGUAGE:")
    for lang in sorted(LANGUAGES):
        count = len(notes_per_lang[lang])
        print(f"- {lang}: {count} notes")
    print()

    # Translation completeness levels
    completeness_counts = defaultdict(int)
    fully_translated = []
    partially_translated = []

    for base_name, langs in notes_coverage.items():
        coverage = len(langs)
        completeness_counts[coverage] += 1

        if coverage == len(LANGUAGES):
            fully_translated.append(base_name)
        else:
            missing_langs = set(LANGUAGES) - langs
            partially_translated.append((base_name, sorted(missing_langs)))

    print("TRANSLATION COMPLETENESS:")
    for coverage in range(len(LANGUAGES) + 1):
        if completeness_counts[coverage] > 0:
            percentage = coverage / len(LANGUAGES) * 100
            print(
                f"- {completeness_counts[coverage]} notes: {percentage:.1f}% coverage ({coverage}/{len(LANGUAGES)} languages)"
            )
    print()

    # Fully translated notes
    print(f"FULLY TRANSLATED NOTES ({len(fully_translated)}/{total_unique_notes}):")
    if fully_translated:
        for note in sorted(fully_translated):
            print(f"- {note}")
    else:
        print("- None")
    print()

    # Notes missing translations
    print(
        f"NOTES MISSING TRANSLATIONS ({len(partially_translated)}/{total_unique_notes}):"
    )
    if partially_translated:
        for base_name, missing_langs in sorted(partially_translated):
            print(f"- {base_name}: missing {', '.join(missing_langs)}")
    else:
        print("- All notes are fully translated!")
    print()

    # Check for orphaned translations (exist in other languages but not English)
    orphaned_translations = []
    for lang in [lang for lang in LANGUAGES if lang != "en"]:
        lang_notes = notes_per_lang[lang]
        english_notes = notes_per_lang.get("en", set())

        orphaned = lang_notes - english_notes
        if orphaned:
            orphaned_translations.extend([(base, lang) for base in orphaned])

    print("ORPHANED TRANSLATIONS (exist in other languages but not English):")
    if orphaned_translations:
        orphaned_translations.sort()
        for base_name, lang in orphaned_translations:
            print(f"- {base_name}: exists in {lang} but not in English")
    else:
        print("- No orphaned translations found")
    print()

    # Notes that exist only in English
    english_only = []
    for base_name, langs in notes_coverage.items():
        if len(langs) == 1 and "en" in langs:
            english_only.append(base_name)

    print(f"ENGLISH-ONLY NOTES ({len(english_only)}):")
    if english_only:
        for note in sorted(english_only):
            print(f"- {note}")
    else:
        print("- None")
    print()


if __name__ == "__main__":
    notes_coverage, notes_per_lang = analyze_notes()
    if notes_coverage:
        print_summary(notes_coverage, notes_per_lang)
    else:
        print("No notes found to analyze.")
