#!/usr/bin/env python3
"""
Script to extract meaningful text from JSON transcript files and save as markdown.
"""

import json
import sys
import os
from pathlib import Path


def extract_transcript(json_path):
    """Extract transcript from JSON file and save as markdown."""
    # Read the JSON file
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract all transcript text
    transcript_texts = []
    for result in data.get("results", []):
        for alternative in result.get("alternatives", []):
            if "transcript" in alternative:
                transcript_texts.append(alternative["transcript"])

    # Join all transcripts with newlines
    full_transcript = "\n".join(transcript_texts)

    # Create output file path (same directory, .md extension)
    input_path = Path(json_path)
    output_path = input_path.with_suffix(".md")

    # Write transcript to markdown file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_transcript)

    print(f"Transcript extracted to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_transcript.py <json_file_path>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    if not os.path.exists(json_file_path):
        print(f"Error: File not found: {json_file_path}")
        sys.exit(1)

    extract_transcript(json_file_path)
