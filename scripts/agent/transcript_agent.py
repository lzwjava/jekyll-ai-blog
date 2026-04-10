import re
import sys
import os
import argparse
from pathlib import Path

# Add parent directories to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from ww.llm.openrouter_client import call_openrouter_api

#!/usr/bin/env python3
"""
Transcript Refinement Agent for Markdown Files
Refines transcript content by fixing grammar, removing filler words, and maintaining original meaning.
Uses Kimi-K2 model through OpenRouter for handling long text.
"""


def refine_transcript_with_ai(content):
    """Refine transcript content using AI to fix grammar and remove filler words."""
    print("Refining transcript with AI...")

    prompt = f"""Please refine this transcript by:

- Fix all grammar and punctuation errors
- Remove filler words and oral expressions like:
   - yeah, yep, uh, um, like, you know, basically, literally
   - Cool, perfect, awesome, great (when not substantial)
   - Repeated phrases, false starts, and verbal ticks

- Identify speakers and label them consistently as A (Speaker 1) and B (Speaker 2)
- Preserve original tone and text as much as possible while making it more coherent and readable
- At transcript start, keep Zoom setup or sound check conversations brief and concise if they discuss
- Preserve technical terms, names, and specific references exactly
- Convert spoken money expressions like "fifty K CNY" to Arabic numerals "50k CNY"
- Output only the refined transcript text - no explanations, no metadata
- Please separate the long text in one reply into smaller paragraphs. The separation should feel natural, based on shifts in topic or focus
- Don't remove information, only restructure it into clearer, shorter blocks
- This is not simplification - keep the original meaning and details intact

Transcript:
{content}"""

    try:
        response = call_openrouter_api(prompt, model="deepseek-v3.1", max_tokens=128000)
        print(f"AI Response length: {len(response)} characters")
        stripped = response.strip()
        return stripped
    except Exception as e:
        print(f"Error calling AI API: {e}", file=sys.stderr)
        return None


def validate_refinement(original_content, refined_content):
    """Validate refined transcript content."""
    validation_issues = []

    # Check length difference (+-10%)
    original_length = len(original_content)
    refined_length = len(refined_content)
    length_diff_percent = abs(original_length - refined_length) / original_length * 100

    if length_diff_percent > 10:
        validation_issues.append(
            f"Content length changed by {length_diff_percent:.1f}% "
            f"(original: {original_length}, refined: {refined_length})"
        )

    # Check for speaker labels (A:, B:, etc.)
    speaker_patterns = [
        r"\bA:\s",
        r"\bB:\s",
        r"\bA1:\s",
        r"\bA2:\s",
        r"\bB1:\s",
        r"\bB2:\s",
    ]
    has_speaker_labels = any(
        re.search(pattern, refined_content, re.IGNORECASE)
        for pattern in speaker_patterns
    )

    if not has_speaker_labels:
        validation_issues.append("No speaker labels found (expected A:, B:, etc.)")

    # Report validation issues but don't fail processing
    if validation_issues:
        print("⚠️  Validation warnings:")
        for issue in validation_issues:
            print(f"   - {issue}")
    else:
        print(
            "✅ Validation passed: Content length within range and speaker labels present"
        )

    return validation_issues


def process_file(file_path, output_only=False):
    """Process a single markdown file containing transcript."""
    print(f"Processing file: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        print(f"Original content length: {len(content)} characters")

        # Refine the transcript using AI
        refined_content = refine_transcript_with_ai(content)

        if refined_content is None:
            print(f"Failed to refine transcript for {file_path}", file=sys.stderr)
            return None

        print(f"Refined content length: {len(refined_content)} characters")

        # Validate the refined content
        validate_refinement(content, refined_content)

        # Generate output filename
        input_path = Path(file_path)
        output_filename = f"{input_path.stem}_refined{input_path.suffix}"
        output_path = input_path.parent / output_filename

        if output_only:
            print("=== REFINED TRANSCRIPT ===")
            print(refined_content)
            print("=== END REFINED TRANSCRIPT ===")
        else:
            print(f"Generating refined version: {output_path}")

            # Write refined content to output file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(refined_content)

            print(f"Refined transcript saved to: {output_path}")
            print(".1f")

        return refined_content

    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return None
    finally:
        print(f"Finished processing: {file_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Refine transcript content in markdown files using AI"
    )
    parser.add_argument(
        "files", nargs="*", help="Markdown files containing transcripts to process"
    )
    parser.add_argument(
        "--output-only",
        action="store_true",
        help="Output refined transcript to console without saving to file",
    )

    args = parser.parse_args()

    if not args.files:
        # If no files specified, look for markdown files in current directory
        md_files = list(Path(".").glob("*.md"))
        if not md_files:
            print("No markdown files found. Please specify files to process.")
            sys.exit(1)
        args.files = [str(f) for f in md_files]

    processed_count = 0
    for file_path in args.files:
        if process_file(file_path, args.output_only):
            processed_count += 1

    success_rate = (processed_count / len(args.files)) * 100 if args.files else 0
    print(
        f"\nProcessing complete: {processed_count}/{len(args.files)} files refined ({success_rate:.1f}%)"
    )


if __name__ == "__main__":
    main()
