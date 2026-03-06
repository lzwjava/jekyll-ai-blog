import shutil
import os
import sys

# Determine direction based on --reverse flag
is_reverse = len(sys.argv) > 1 and sys.argv[1] == "--reverse"

if is_reverse:
    # Reverse: copy from repo to home
    source_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "config", "ghostty_config")
    )
    target_file = os.path.expanduser("~/.config/ghostty/config")
else:
    # Normal: copy from home to repo
    source_file = os.path.expanduser("~/.config/ghostty/config")
    target_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "config", "ghostty_config")
    )

# Ensure target directory exists
os.makedirs(os.path.dirname(target_file), exist_ok=True)

# Copy the file
shutil.copy2(source_file, target_file)

if is_reverse:
    print(f"Copied {source_file} to {target_file}")
else:
    print(f"Copied {source_file} to {target_file}")
