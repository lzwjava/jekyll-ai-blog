import sys
import re
from ruamel.yaml import YAML


def convert_markdown_table(file_path):
    yaml = YAML()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read()
            # Split the file content into front matter and content
            parts = data.split("---", 2)
            if len(parts) != 3:
                print(
                    "Error: Invalid markdown file format. Missing front matter or content."
                )
                return None
            front_matter_str = parts[1]
            content = parts[2].strip()

            try:
                post = yaml.load(front_matter_str)
            except Exception as e:
                print(f"Error parsing front matter: {e}")
                return None

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return None

    # Regex to find markdown table rows
    table_rows = re.findall(r"\|[^\n]+\|", content)
    if not table_rows:
        print("No markdown table found in the file.")
        return None

    converted_rows = []
    for row in table_rows[2:]:  # Skip header and separator
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        if len(cells) == 2:
            converted_rows.append(f"- {cells[0]}, {cells[1]}")

    if not converted_rows:
        print("No valid table rows found to convert.")
        return None

    new_content = "\n".join(converted_rows)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("---\n")
            yaml.dump(post, f)
            f.write("\n---\n")
            f.write(new_content)
        print(f"Successfully converted table in {file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <markdown_file_path>")
    else:
        file_path = sys.argv[1]
        convert_markdown_table(file_path)
