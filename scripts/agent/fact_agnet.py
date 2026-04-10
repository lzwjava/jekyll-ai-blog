import sys
import argparse
from pathlib import Path
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from ww.llm.openrouter_client import call_openrouter_api

#!/usr/bin/env python3
"""
Fact Checker for Jekyll Posts
Checks numbered claims (fact 1, fact 2, ...) in markdown files using AI and confirms their correctness.
Supports --prompt to provide a guiding keyword for the check.
"""


def fact_check_with_ai(content, prompt_word=None):
    """Extract numbered facts like 'fact 1' or 'fact 2' and ask AI to confirm each.

    Returns a markdown report with each numbered fact followed by AI's confirmation.
    """
    # Build prompt to enumerate and check numbered facts
    helper = f"Use the keyword '{prompt_word}' when relevant." if prompt_word else ""
    prompt = f"""You will be given markdown content. Find numbered claims like 'fact 1', 'fact 2', or lines that start with 'Fact X:' or similar.
For each claim, do the following:
1) Extract the claim text.
2) Assign it a number (if not already numbered) in the order found.
3) Check whether the claim is factually correct, partially correct, or incorrect.
4) Provide a brief (1-2 sentence) justification and a reliable source URL if available.
5) If unsure, say 'unknown' and explain what additional info is needed.
{helper}

Markdown content:
{content}

Return the results as a markdown numbered list with entries like:
1. Claim: <claim text>\n   Verdict: <Correct|Partially correct|Incorrect|Unknown>\n   Reason: <brief justification>\n   Source: <url or 'none'>

If no numbered claims are found, return: 'No numbered claims found.'
"""
    try:
        response = call_openrouter_api(prompt)
        return response.strip()
    except Exception as e:
        print(f"Error calling AI API: {e}", file=sys.stderr)
        return None


def process_file(file_path, output_only=False, prompt_word=None):
    """Process a single Jekyll post file for fact checking."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        report = fact_check_with_ai(content, prompt_word=prompt_word)

        if report is None:
            return None

        if output_only:
            print(report)
        else:
            print(f"Fact-check report for {file_path}:")
            print(report)
            print()

        return report

    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Fact-check numbered claims in Jekyll posts using AI"
    )
    parser.add_argument("files", nargs="*", help="Markdown files to process")
    parser.add_argument(
        "--output-only",
        action="store_true",
        help="Output only the report without file info",
    )
    parser.add_argument(
        "--prompt",
        dest="prompt_word",
        help="Optional prompt word to guide the fact checking",
    )

    args = parser.parse_args()

    if not args.files:
        md_files = list(Path(".").glob("*.md"))
        if not md_files:
            print("No markdown files found. Please specify files to process.")
            sys.exit(1)
        args.files = md_files

    for file_path in args.files:
        process_file(file_path, args.output_only, prompt_word=args.prompt_word)


if __name__ == "__main__":
    main()
