#!/usr/bin/env python3

import os
import sys
from google import genai
from google.genai.types import GenerateImagesConfig


def generate_image_with_imagen(prompt, output_path):
    """Generate image using Imagen model."""
    print("Generating image with Imagen model...")
    print(f"Output path: {output_path}")

    try:
        print("Setting up Vertex AI client...")
        # Set up Vertex AI client
        client = genai.Client(
            vertexai=True,
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("GOOGLE_CLOUD_LOCATION"),
        )

        print("Calling Imagen API with model: imagen-4.0-generate-preview-06-06")
        image = client.models.generate_images(
            model="imagen-4.0-generate-preview-06-06",
            prompt=prompt,
            config=GenerateImagesConfig(
                aspect_ratio="1:1",  # Square ratio for better center cropping flexibility
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
