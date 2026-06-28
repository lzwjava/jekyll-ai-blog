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

    restart_editor()


def _editor_available(name):
    """Check if an editor command exists on PATH."""
    return shutil.which(name) is not None


def restart_editor():
    """Restart the project in the best available editor: Zed first, then VSCode."""
    editor = None
    if _editor_available("zed"):
        editor = "zed"
    elif _editor_available("code"):
        editor = "code"
    else:
        print("No supported editor found (Zed or VSCode). Skipping editor restart.")
        return

    label = "Zed" if editor == "zed" else "VSCode"
    print(
        f"Restarting {label} gracefully to prevent accidental re-creation of draft files..."
    )
    try:
        if sys.platform == "win32":
            proc_name = "Zed.exe" if editor == "zed" else "Code.exe"
            os.system(f"taskkill /im {proc_name} /t")
            time.sleep(3)
            subprocess.Popen([editor, "."])
        elif sys.platform == "darwin":
            app_name = "Zed" if editor == "zed" else "Visual Studio Code"
            os.system(f"osascript -e 'quit app \"{app_name}\"'")
            time.sleep(3)
            subprocess.call(["open", "-a", app_name, "."])
        elif sys.platform.startswith("linux"):
            os.system(f"killall {editor}")
            time.sleep(3)
            subprocess.Popen([editor, "."])
        else:
            print(f"Unsupported platform for restarting {label}.")
    except Exception as e:
        print(f"Error during restart: {e}. Please manually restart {label}.")


if __name__ == "__main__":
    publish_drafts_to_posts()
