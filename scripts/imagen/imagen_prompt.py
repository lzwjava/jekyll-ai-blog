import sys
import argparse
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from scripts.llm.openrouter_client import call_openrouter_api

#!/usr/bin/env python3
"""
Image Generator for Jekyll Posts
Generates images for Jekyll post files using AI.
"""


def generate_image_prompt_with_ai(content):
    """Generate image prompt using AI."""
    prompt = f"""Please generate a detailed image prompt for the following markdown content.
Follow these rules:
1. Create a vivid, descriptive prompt for image generation (1-2 sentences)
2. Focus on visual elements that represent the main topic
3. Include artistic style suggestions (e.g., "digital art", "illustration", "photorealistic")
4. Avoid text or words in the image description
5. Make it suitable for creating an engaging blog post header image

Markdown content:
{content}

Return only the image prompt:"""

    try:
        response = call_openrouter_api(prompt)
        return response.strip()
    except Exception as e:
        print(f"Error calling AI API: {e}", file=sys.stderr)
        return None


def imagen_prompt(file_path, debug=False):
    """Process a single Jekyll post file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        image_prompt = generate_image_prompt_with_ai(content)

        if image_prompt is None:
            return None

        if debug:
            print(f"Image prompt for {file_path}:")
            print(image_prompt)
            print()

        return image_prompt
    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate images for Jekyll posts using AI"
    )
    parser.add_argument("file", help="Markdown file to process")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")

    args = parser.parse_args()

    imagen_prompt(args.file, debug=args.debug)


if __name__ == "__main__":
    main()
