from google import genai
from google.genai.types import GenerateImagesConfig
import os

import sys
import argparse
from pathlib import Path
from imagen_prompt import imagen_prompt


def generate_image_with_imagen(prompt, output_path):
    """Generate image using Imagen model."""
    print(f"Generating image with Imagen model...")
    print(f"Output path: {output_path}")

    try:
        print("Setting up Vertex AI client...")
        # Set up Vertex AI client
        client = genai.Client(
            vertexai=True,
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("GOOGLE_CLOUD_LOCATION"),
        )

        print(f"Calling Imagen API with model: imagen-4.0-generate-preview-06-06")
        image = client.models.generate_images(
            model="imagen-4.0-generate-preview-06-06",
            prompt=prompt,
            config=GenerateImagesConfig(
                aspect_ratio="16:9",
                image_size="1K",
                output_compression_quality=90,
                output_mime_type="image/jpeg",
                number_of_images=1,
                safety_filter_level="BLOCK_LOW_AND_ABOVE",
                person_generation="ALLOW_ADULT",
            ),
        )

        print("Saving generated image...")
        image.generated_images[0].image.save(output_path)
        print(
            f"✓ Successfully created image at {output_path} using {len(image.generated_images[0].image.image_bytes)} bytes"
        )
        return True

    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        return False


def process_file(file_path, debug=False):
    """Process a single Jekyll post file."""
    print(f"\n=== Processing file: {file_path} ===")

    try:
        print("Generating image prompt from content...")
        # Get image prompt using the imported function
        prompt = imagen_prompt(file_path, debug=debug)

        if prompt is None:
            print("❌ Failed to generate image prompt")
            return None

        print(f"✓ Generated prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")

        # Create output filename
        file_stem = Path(file_path).stem
        output_path = f"test/{file_stem}.jpg"

        print(f"Creating output directory: test/")
        # Ensure test directory exists
        Path("test").mkdir(exist_ok=True)

        # Generate image
        success = generate_image_with_imagen(prompt, output_path)

        if success:
            print(f"✓ Successfully processed {file_path}")
        else:
            print(f"❌ Failed to process {file_path}")

        return prompt if success else None

    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return None


def imagen_og_files(files, debug=False):
    """Process multiple files to generate OG images.

    Args:
        files: List of file paths to process
        debug: Enable debug output

    Returns:
        Number of successfully processed files
    """
    print(f"\nProcessing {len(files)} files...")
    success_count = 0

    for i, file_path in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Processing: {file_path}")
        result = process_file(file_path, debug)
        if result:
            success_count += 1

    print(f"\n=== Summary ===")
    print(f"Processed: {len(files)} files")
    print(f"Successful: {success_count} files")
    print(f"Failed: {len(files) - success_count} files")

    return success_count


def main():
    parser = argparse.ArgumentParser(
        description="Generate images for Jekyll posts using AI"
    )
    parser.add_argument("files", nargs="*", help="Markdown files to process")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output",
    )

    args = parser.parse_args()

    if not args.files:
        raise ValueError(
            "No files specified. Please provide markdown files to process."
        )

    imagen_og_files(args.files, args.debug)


if __name__ == "__main__":
    main()
