#!/usr/bin/env python3

import argparse
import os
import sys
from PIL import Image, ImageFilter
import numpy as np
from typing import Tuple, Optional


def convert_to_png(image_path: str, output_path: Optional[str] = None) -> str:
    img = Image.open(image_path)

    if output_path is None:
        base_name = os.path.splitext(image_path)[0]
        output_path = f"{base_name}.png"

    if img.mode != "RGBA":
        img = img.convert("RGBA")

    img.save(output_path, "PNG")
    print(f"Converted to PNG: {output_path}")
    return output_path


def remove_white_background(
    image_path: str, output_path: str, tolerance: int = 30
) -> None:
    img = Image.open(image_path).convert("RGBA")
    data = np.array(img)

    white_mask = (
        (data[:, :, 0] >= 255 - tolerance)
        & (data[:, :, 1] >= 255 - tolerance)
        & (data[:, :, 2] >= 255 - tolerance)
    )

    data[white_mask, 3] = 0

    result_img = Image.fromarray(data, "RGBA")
    result_img.save(output_path, "PNG")
    print(f"White background removed: {output_path}")


def remove_color_background(
    image_path: str,
    output_path: str,
    bg_color: Tuple[int, int, int],
    tolerance: int = 30,
) -> None:
    img = Image.open(image_path).convert("RGBA")
    data = np.array(img)

    color_mask = (
        (np.abs(data[:, :, 0] - bg_color[0]) <= tolerance)
        & (np.abs(data[:, :, 1] - bg_color[1]) <= tolerance)
        & (np.abs(data[:, :, 2] - bg_color[2]) <= tolerance)
    )

    data[color_mask, 3] = 0

    result_img = Image.fromarray(data, "RGBA")
    result_img.save(output_path, "PNG")
    print(f"Color background removed: {output_path}")


def detect_background_color(image_path: str) -> Tuple[int, int, int]:
    img = Image.open(image_path).convert("RGB")
    data = np.array(img)
    height, width = data.shape[:2]

    corner_size = min(50, height // 10, width // 10)
    corners = [
        data[:corner_size, :corner_size],
        data[:corner_size, -corner_size:],
        data[-corner_size:, :corner_size],
        data[-corner_size:, -corner_size:],
    ]

    corner_pixels = np.concatenate([corner.reshape(-1, 3) for corner in corners])

    unique_colors, counts = np.unique(corner_pixels, axis=0, return_counts=True)
    most_common_color = unique_colors[np.argmax(counts)]

    return tuple(most_common_color)


def remove_background_smart(
    image_path: str, output_path: str, tolerance: int = 30
) -> None:
    bg_color = detect_background_color(image_path)
    print(f"Detected background color: RGB{bg_color}")

    remove_color_background(image_path, output_path, bg_color, tolerance)


def apply_edge_smoothing(image_path: str, output_path: str) -> None:
    img = Image.open(image_path).convert("RGBA")

    alpha = img.split()[3]
    alpha_blurred = alpha.filter(ImageFilter.GaussianBlur(radius=0.5))

    r, g, b, _ = img.split()
    smoothed_img = Image.merge("RGBA", (r, g, b, alpha_blurred))

    smoothed_img.save(output_path, "PNG")
    print(f"Edge smoothing applied: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Remove background from images")
    parser.add_argument("input", help="Input image path")
    parser.add_argument(
        "-o", "--output", help="Output image path (default: input_nobg.png)"
    )
    parser.add_argument(
        "-m",
        "--method",
        choices=["white", "color", "smart"],
        default="smart",
        help="Background removal method",
    )
    parser.add_argument(
        "-c",
        "--color",
        help="Background color to remove (R,G,B format, e.g., 255,255,255)",
    )
    parser.add_argument(
        "-t",
        "--tolerance",
        type=int,
        default=30,
        help="Color tolerance (0-255, default: 30)",
    )
    parser.add_argument(
        "--smooth",
        action="store_true",
        help="Apply edge smoothing after background removal",
    )
    parser.add_argument(
        "--convert-only",
        action="store_true",
        help="Only convert to PNG without removing background",
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found")
        sys.exit(1)

    if args.output is None:
        base_name = os.path.splitext(args.input)[0]
        args.output = f"{base_name}_nobg.png"

    try:
        if args.convert_only:
            convert_to_png(args.input, args.output)
            return

        png_path = convert_to_png(args.input)

        if args.method == "white":
            remove_white_background(png_path, args.output, args.tolerance)
        elif args.method == "color":
            if not args.color:
                print("Error: --color is required when using 'color' method")
                print("Example: --color 255,255,255 for white background")
                sys.exit(1)

            try:
                bg_color = tuple(map(int, args.color.split(",")))
                if len(bg_color) != 3:
                    raise ValueError
            except ValueError:
                print(
                    "Error: Invalid color format. Use R,G,B format (e.g., 255,255,255)"
                )
                sys.exit(1)

            remove_color_background(png_path, args.output, bg_color, args.tolerance)
        elif args.method == "smart":
            remove_background_smart(png_path, args.output, args.tolerance)

        if args.smooth:
            temp_output = args.output
            smooth_output = f"{os.path.splitext(args.output)[0]}_smooth.png"
            apply_edge_smoothing(temp_output, smooth_output)
            args.output = smooth_output

        print("Background removal completed successfully!")
        print(f"Output saved to: {args.output}")

        if png_path != args.input and os.path.exists(png_path):
            os.remove(png_path)

    except Exception as e:
        print(f"Error processing image: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
