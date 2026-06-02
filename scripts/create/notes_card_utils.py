#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import qrcode
import os


def center_crop_to_fit(img, target_width, target_height):
    """Center crop an image to fit target dimensions while preserving aspect ratio"""
    img_width, img_height = img.size
    target_ratio = target_width / target_height
    img_ratio = img_width / img_height

    if img_ratio > target_ratio:
        # Image is wider than target ratio, crop width
        new_width = int(img_height * target_ratio)
        offset = (img_width - new_width) // 2
        cropped_img = img.crop((offset, 0, offset + new_width, img_height))
    elif img_ratio < target_ratio:
        # Image is taller than target ratio, crop height
        new_height = int(img_width / target_ratio)
        offset = (img_height - new_height) // 2
        cropped_img = img.crop((0, offset, img_width, offset + new_height))
    else:
        # Same aspect ratio, no cropping needed
        cropped_img = img

    # Resize to exact target dimensions
    resized_img = cropped_img.resize(
        (target_width, target_height), Image.Resampling.LANCZOS
    )
    return resized_img


def generate_share_card(
    titles, output_path, invitation=None, background_image_path=None
):
    """Generate a share card image with note titles and QR code"""
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Image dimensions - iPhone 14 Pro Max aspect ratio (2.16:1)
    WIDTH = 1080
    HEIGHT = 1600

    # Create full-area background image
    if background_image_path and os.path.exists(background_image_path):
        # Load background image and center crop to match aspect ratio
        bg_img = Image.open(background_image_path)
        bg_img = center_crop_to_fit(bg_img, WIDTH, HEIGHT)
        img = bg_img.convert("RGBA")
    else:
        # Create new image with white background if no background image
        img = Image.new("RGBA", (WIDTH, HEIGHT), color="white")

    # Add semi-transparent blur effect to bottom area for better text readability
    HALF_HEIGHT = HEIGHT // 2
    blur_overlay = Image.new(
        "RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0)
    )  # Transparent overlay
    draw_overlay = ImageDraw.Draw(blur_overlay)

    # Create a semi-transparent dark rectangle over the bottom half
    draw_overlay.rectangle(
        [0, HALF_HEIGHT, WIDTH, HEIGHT], fill=(0, 0, 0, 120)
    )  # Semi-transparent black

    # Composite the blur overlay onto the background
    img = Image.alpha_composite(img, blur_overlay)

    draw = ImageDraw.Draw(img)

    try:
        # Try to use a nice font, fallback to default
        font_title = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 72)
        font_invitation = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 48)
        font_notes = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", 36)
    except Exception:
        # Fallback to default font
        font_title = ImageFont.load_default()
        font_invitation = ImageFont.load_default()
        font_notes = ImageFont.load_default()

    # All text content is now in the bottom half (bottom area starts at HALF_HEIGHT)
    # Title
    if invitation:
        title = invitation
        title_font = font_invitation
    else:
        title = "Latest Notes"
        title_font = font_title

    base_y_offset = HALF_HEIGHT + 20  # Start text in bottom half
    draw.text((20, base_y_offset), title, fill="white", font=title_font)

    # List notes - adjust offset based on title height
    title_bbox = draw.textbbox((20, base_y_offset), title, font=title_font)
    y_offset = title_bbox[3] + 40  # Add some padding after title
    for title in titles:
        text = f"• {title}"
        draw.text((20, y_offset), text, fill="white", font=font_notes)
        y_offset += 50

    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=15, border=5)
    qr.add_data("https://lzwjava.github.io/notes-en")
    qr.make(fit=True)

    # Create QR code image
    qr_img = qr.make_image(fill="black", back_color="white")

    # Make QR code smaller and place in center
    qr_size = 200  # Smaller size
    qr_img = qr_img.resize((qr_size, qr_size))

    # Paste QR code on the image - positioned near bottom edge with 20px margin
    qr_x = (WIDTH - qr_size) // 2
    qr_y = HEIGHT - qr_size - 20  # Position 20px above bottom edge
    img.paste(qr_img, (qr_x, qr_y))

    # Add QR code label - centered above QR code
    draw.textbbox((0, 0), "Scan for more notes", font=font_notes)[3]
    label_y = qr_y - 40
    label_x = (
        WIDTH - draw.textbbox((0, 0), "Scan for more notes", font=font_notes)[2]
    ) // 2
    draw.text((label_x, label_y), "Scan for more notes", fill="white", font=font_notes)

    # Save the image - convert back to RGB for compatibility
    if img.mode == "RGBA":
        # Create a new RGB image
        rgb_img = Image.new("RGB", img.size, "white")
        rgb_img.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
        rgb_img.save(output_path)
    else:
        img.save(output_path)
    return output_path
