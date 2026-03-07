import os
import re

source_file = os.path.expanduser("~/.zprofile")

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Create the path to the config directory within the parent directory
target_file = os.path.join(parent_dir, "config", ".zprofile")

with open(source_file, "r") as f_source:
    content = f_source.read()

# Remove lines containing API key exports
content = re.sub(r'export \w+_API_KEY=".*"\n?', "", content)
content = re.sub(r'export TIGER_\w+=".*"\n?', "", content)
content = re.sub(r'export CLASH_\w+=".*"\n?', "", content)

# Ensure target directory exists
os.makedirs(os.path.dirname(target_file), exist_ok=True)

with open(target_file, "w") as f_target:
    f_target.write(content)

print(f"Copied and sanitized {source_file} to {target_file}")
