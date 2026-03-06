import subprocess
import datetime
import os
import time
from PIL import Image

# Create screenshots directory if it doesn't exist
screenshot_dir = "assets/screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

# Prompt user to prepare for screenshot
print("🖼️  Screenshot will be taken in 5 seconds...")
print("📋 Please switch to the window you want to capture")
print("⏳ Countdown: 5...", end="", flush=True)

time.sleep(1)
print(" 4...", end="", flush=True)
time.sleep(1)
print(" 3...", end="", flush=True)
time.sleep(1)
print(" 2...", end="", flush=True)
time.sleep(1)
print(" 1...")
time.sleep(1)
print("📸 Taking screenshot now!")

# Generate filename with format: yearmmdd_hhmm.png
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")
path = os.path.join(screenshot_dir, f"{ts}.png")

# Method 1: Use scrot (if available)
try:
    subprocess.run(["scrot", path], check=True)
    print(f"Saved screenshot to {path} using scrot")
except (subprocess.CalledProcessError, FileNotFoundError):
    # Method 2: Use ImageMagick's import command
    try:
        subprocess.run(["import", "-window", "root", path], check=True)
        print(f"Saved screenshot to {path} using ImageMagick")
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Method 3: Use gnome-screenshot (GNOME environments)
        try:
            subprocess.run(["gnome-screenshot", "-f", path], check=True)
            print(f"Saved screenshot to {path} using gnome-screenshot")
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Method 4: Use spectacle (KDE environments)
            try:
                subprocess.run(["spectacle", "-b", "-n", "-o", path], check=True)
                print(f"Saved screenshot to {path} using spectacle")
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Method 5: Use xwd (X11 fallback)
                try:
                    # Take screenshot with xwd
                    xwd_path = os.path.join(screenshot_dir, f"{ts}.xwd")
                    subprocess.run(["xwd", "-root", "-out", xwd_path], check=True)

                    # Convert xwd to png using ImageMagick
                    subprocess.run(["convert", xwd_path, path], check=True)

                    # Clean up xwd file
                    if os.path.exists(xwd_path):
                        os.remove(xwd_path)

                    print(f"Saved screenshot to {path} using xwd + convert")
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # Method 6: Use ffmpeg (last resort)
                    try:
                        subprocess.run(
                            [
                                "ffmpeg",
                                "-f",
                                "x11grab",
                                "-s",
                                "1920x1080",
                                "-i",
                                ":0.0",
                                "-frames:v",
                                "1",
                                path,
                            ],
                            check=True,
                            capture_output=True,
                        )
                        print(f"Saved screenshot to {path} using ffmpeg")
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        print(
                            "No suitable screenshot tool found. Please install one of: scrot, ImageMagick, gnome-screenshot, spectacle, or ffmpeg."
                        )

# If screenshot was taken, show basic info and compress
if os.path.exists(path):
    try:
        with Image.open(path) as img:
            original_size = os.path.getsize(path)
            print(f"Screenshot saved successfully: {path}")
            print(
                f"Original size: {img.size[0]}x{img.size[1]} ({original_size / 1024:.1f} KB)"
            )

            # Resize to 50% of original size for better compression
            new_width = int(img.size[0] * 0.5)
            new_height = int(img.size[1] * 0.5)
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)

            # Compress with quality 85 and save - use JPEG for better compression
            compressed_path = path.replace(".png", "_compressed.jpg")
            resized_img.save(compressed_path, "JPEG", quality=85, optimize=True)

            # Show compressed size
            compressed_size = os.path.getsize(compressed_path)
            print(
                f"Compressed size: {new_width}x{new_height} ({compressed_size / 1024:.1f} KB)"
            )
            print(f"Compression ratio: {(original_size / compressed_size):.1f}x")
            print(f"Compressed saved as: {compressed_path}")

            # Optionally replace original with compressed version
            os.replace(compressed_path, path)
            print(f"✅ Compressed screenshot saved: {path}")

    except Exception as e:
        print(f"Could not process image: {e}")
