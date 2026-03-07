#!/usr/bin/env python3
"""
Bullet Point Card Generator

Generates mobile-friendly cards with dark mode background from bullet points.
Supports clipboard input and JSON input.
"""

import json
import os
import tempfile
from PIL import Image, ImageDraw, ImageFont
import pyperclip


def create_bullet_point_card(points, title="Bullet Points", output_dir=None):
    """
    Create a card image with bullet points on a dark background.

    Args:
        points (list): List of bullet point strings
        title (str): Title for the card
        output_dir (str): Directory to save the image (defaults to temp dir)

    Returns:
        str: Path to the generated image
    """
    # Set dark mode colors
    bg_color = (25, 25, 35)  # Dark gray background
    text_color = (240, 240, 240)  # Light gray text
    accent_color = (70, 130, 180)  # Steel blue accent

    # Set dimensions for mobile-friendly viewing
    width = 800
    height = max(600, 100 + len(points) * 60)  # Adjust height based on content

    # Create image with dark background
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Try to use a nice font, fallback to default if not available
    try:
        # Try to use a system font
        title_font = ImageFont.truetype("Arial.ttf", 32)
        text_font = ImageFont.truetype("Arial.ttf", 24)
        bullet_font = ImageFont.truetype("Arial.ttf", 24)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        bullet_font = ImageFont.load_default()

    # Draw title
    draw.text((40, 30), title, fill=accent_color, font=title_font)

    # Draw separator line
    draw.line([(30, 80), (width - 30, 80)], fill=accent_color, width=2)

    # Draw bullet points
    y_position = 110
    bullet_radius = 5

    for point in points:
        # Draw bullet point (circle)
        bullet_y = y_position + 8
        draw.ellipse(
            [
                (50 - bullet_radius, bullet_y - bullet_radius),
                (50 + bullet_radius, bullet_y + bullet_radius),
            ],
            fill=accent_color,
        )

        # Draw text
        draw.text((70, y_position), point, fill=text_color, font=text_font)

        # Move to next line
        y_position += 50

    # Save image
    if output_dir is None:
        output_dir = tempfile.gettempdir()

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename
    filename = f"bullet_card_{len(points)}_points.png"
    filepath = os.path.join(output_dir, filename)

    # Save image
    img.save(filepath)

    return filepath


def read_from_clipboard():
    """
    Read bullet points from clipboard.

    Returns:
        list: List of bullet point strings
    """
    try:
        clipboard_content = pyperclip.paste()
        # Split by newlines and filter out empty lines
        points = [
            line.strip() for line in clipboard_content.split("\n") if line.strip()
        ]
        return points
    except Exception as e:
        print(f"Error reading from clipboard: {e}")
        return []


def read_from_json(json_input):
    """
    Read bullet points from JSON input.

    Args:
        json_input (str): JSON string or file path

    Returns:
        list: List of bullet point strings
    """
    try:
        # Try to parse as JSON string first
        data = json.loads(json_input)
    except json.JSONDecodeError:
        # If that fails, try to read as file path
        try:
            with open(json_input, "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading JSON: {e}")
            return []

    # Handle different JSON structures
    if isinstance(data, list):
        # If it's a list, assume it's a list of points
        return [str(item) for item in data]
    elif isinstance(data, dict):
        # If it's a dict, look for common keys
        for key in ["points", "items", "bullet_points", "bullets"]:
            if key in data and isinstance(data[key], list):
                return [str(item) for item in data[key]]
        # If no common keys found, return the values
        return [str(value) for value in data.values()]
    else:
        return [str(data)]


def main():
    """Main function to handle command line arguments and generate cards."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate bullet point cards with dark mode background"
    )
    parser.add_argument(
        "--title", "-t", default="Bullet Points", help="Title for the card"
    )
    parser.add_argument(
        "--output", "-o", help="Output directory (defaults to temp dir)"
    )
    parser.add_argument("--json", "-j", help="JSON input (string or file path)")
    parser.add_argument(
        "--clipboard", "-c", action="store_true", help="Read from clipboard"
    )
    parser.add_argument("--points", "-p", nargs="+", help="Bullet points as arguments")

    args = parser.parse_args()

    points = []

    # Determine source of bullet points
    if args.json:
        points = read_from_json(args.json)
    elif args.clipboard:
        points = read_from_clipboard()
    elif args.points:
        points = args.points
    else:
        # If no source specified, try clipboard as default
        points = read_from_clipboard()

        # If clipboard is empty, show help
        if not points:
            parser.print_help()
            return

    if not points:
        print("No bullet points found!")
        return

    # Generate card
    try:
        filepath = create_bullet_point_card(points, args.title, args.output)
        print(f"Card generated successfully: {filepath}")
    except Exception as e:
        print(f"Error generating card: {e}")


if __name__ == "__main__":
    main()
