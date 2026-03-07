import os
import datetime
import glob
import shutil
import sys
import subprocess
import time
import re
import yaml


def validate_image_frontmatter(file_path):
    """Check if image frontmatter matches content. Returns (is_valid, error_message)."""
    try:
        with open(file_path, "r", encoding="utf-8") as infile:
            content = infile.read()

        front_matter_match = re.match(r"---\n(.*?)\n---", content, re.DOTALL)
        if front_matter_match:
            front_matter = front_matter_match.group(1)
            front_matter_dict = yaml.safe_load(front_matter) if front_matter else {}
        else:
            front_matter_dict = {}

        # Check if content contains image path
        has_image_in_content = "assets/images/" in content
        has_image_in_frontmatter = front_matter_dict.get("image", False)

        if has_image_in_content and not has_image_in_frontmatter:
            return False, "Content contains images but image: false in frontmatter"
        elif not has_image_in_content and has_image_in_frontmatter:
            return False, "Frontmatter has image: true but no images in content"
        else:
            return True, None

    except Exception as e:
        return False, f"Error validating file: {e}"


def publish_drafts_to_posts():
    """Checks for draft files created today and moves them to the _posts/en directory."""
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")

    drafts_dir = "_drafts"
    posts_en_dir = "original"

    if not os.path.exists(drafts_dir):
        print(f"Drafts directory '{drafts_dir}' does not exist. No files to publish.")
        return

    if not os.path.exists(posts_en_dir):
        os.makedirs(posts_en_dir)

    # Pattern to find files in drafts directory starting with today's date and ending with -en.md
    pattern = os.path.join(drafts_dir, f"{date_str}-*-*.md")

    found_files = glob.glob(pattern)

    if not found_files:
        print(
            f"No draft files found in '{drafts_dir}' starting with '{date_str}' to publish."
        )
        return

    for file_path in found_files:
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(posts_en_dir, file_name)

        # Validate image frontmatter before publishing
        is_valid, error_message = validate_image_frontmatter(file_path)
        if not is_valid:
            print(f"❌ Cannot publish '{file_name}': {error_message}")
            print("   Please fix the image frontmatter before publishing.")
            continue

        try:
            shutil.move(file_path, destination_path)
            print(f"✅ Moved '{file_name}' from '{drafts_dir}' to '{posts_en_dir}'.")
        except Exception as e:
            print(f"Error moving '{file_name}': {e}")

    restart_vscode()


def restart_vscode():
    print(
        "Restarting VSCode gracefully to prevent accidental re-creation of draft files..."
    )
    try:
        if sys.platform == "win32":
            # Graceful close without /f
            os.system("taskkill /im Code.exe /t")
            time.sleep(3)  # Delay for cleanup
            subprocess.Popen(["code", "."])  # Reopen
        elif sys.platform == "darwin":
            # Use AppleScript for graceful quit
            os.system("osascript -e 'quit app \"Visual Studio Code\"'")
            time.sleep(3)
            subprocess.call(["open", "-a", "Visual Studio Code", "."])
        elif sys.platform.startswith("linux"):
            # SIGTERM for graceful termination
            os.system("killall code")
            time.sleep(3)
            subprocess.Popen(["code", "."])
        else:
            print("Unsupported platform for restarting VSCode.")
    except Exception as e:
        print(f"Error during restart: {e}. Please manually restart VSCode.")


if __name__ == "__main__":
    publish_drafts_to_posts()
