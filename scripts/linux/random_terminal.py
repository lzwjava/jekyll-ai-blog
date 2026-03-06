#!/usr/bin/env python3
"""
Fullscreen Terminal Script
Opens a terminal in fullscreen mode for better multitasking
"""

import subprocess
import random
import os


def get_screen_resolution():
    """Get screen resolution using xrandr"""
    try:
        result = subprocess.run(["xrandr"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "*" in line:
                # Parse resolution like "1920x1080 60.00*+"
                res_part = line.split()[0]
                width, height = map(int, res_part.split("x"))
                return width, height
    except Exception as e:
        print(f"Error getting screen resolution: {e}")
    return 1920, 1080  # Default fallback


def generate_fullscreen_size(screen_width, screen_height):
    """Generate full screen terminal dimensions"""
    # Terminal character dimensions (rough estimates)
    char_width_px = 8  # pixels per character
    char_height_px = 16  # pixels per line

    # Calculate terminal dimensions to fill most of the screen
    # Reserve some space for window decorations
    effective_height = screen_height - 50
    effective_width = screen_width - 20

    # Convert to character dimensions
    term_width = int(effective_width / char_width_px)
    term_height = int(effective_height / char_height_px)

    # Use position 0,0 for full screen
    x = 0
    y = 0

    return x, y, term_width, term_height


def open_terminal_at_position(x, y, term_width=80, term_height=24):
    """Open gnome-terminal at specified position with specified dimensions"""
    try:
        # Use gnome-terminal with geometry (geometry is in characters: WxH+X+Y)
        cmd = [
            "gnome-terminal",
            "--geometry",
            f"{term_width}x{term_height}+{x}+{y}",
            "--working-directory",
            os.getcwd(),
        ]

        subprocess.Popen(cmd)
        print(
            f"Opened terminal at position ({x}, {y}) with size {term_width}x{term_height}"
        )

    except subprocess.CalledProcessError as e:
        print(f"Error opening terminal: {e}")
        # Fallback to xterm if gnome-terminal not available
        try:
            cmd = ["xterm", "-geometry", f"{term_width}x{term_height}+{x}+{y}"]
            subprocess.Popen(cmd)
            print(
                f"Opened xterm at position ({x}, {y}) with size {term_width}x{term_height}"
            )
        except Exception as ex:
            print(f"Error opening xterm: {ex}")


def main():
    screen_width, screen_height = get_screen_resolution()
    x, y, term_width, term_height = generate_fullscreen_size(
        screen_width, screen_height
    )
    open_terminal_at_position(x, y, term_width, term_height)


if __name__ == "__main__":
    main()
