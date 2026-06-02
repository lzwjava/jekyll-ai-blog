---
audio: false
generated: true
lang: en
layout: post
title: Comparing Two Single-row CSV
translated: false
type: note
---

Below is a Python script that compares two single-row CSV files containing strings (e.g., "P0001") and identifies:
- Common items (present in both files)
- Items unique to the first file
- Items unique to the second file

The script uses `argparse` to accept two CSV file paths, reads the first row from each, performs a set-based comparison, and writes the results to `comparison.txt`.

```python
#!/usr/bin/env python3
import argparse
import csv
import os

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Compare two single-row CSV files for common and unique items')
    parser.add_argument('file1_path', help='Path to the first CSV file')
    parser.add_argument('file2_path', help='Path to the second CSV file')

    # Parse arguments
    args = parser.parse_args()

    try:
        # Read the first row of the first CSV file
        with open(args.file1_path, 'r') as file1:
            reader1 = csv.reader(file1)
            for row in reader1:
                values1 = row
                break

        # Read the first row of the second CSV file
        with open(args.file2_path, 'r') as file2:
            reader2 = csv.reader(file2)
            for row in reader2:
                values2 = row
                break

        # Convert to sets for comparison
        set1 = set(values1)
        set2 = set(values2)

        # Find common and unique items
        common_items = set1.intersection(set2)
        unique_to_file1 = set1.difference(set2)
        unique_to_file2 = set2.difference(set1)

        # Determine output directory (use directory of first file)
        output_dir = os.path.dirname(args.file1_path) or '.'
        output_file = os.path.join(output_dir, 'comparison.txt')

        # Write results to output file
        with open(output_file, 'w') as file:
            file.write("Comparison Results:\n\n")

            file.write("Common Items (in both files):\n")
            if common_items:
                for item in sorted(common_items):
                    file.write(f"{item}\n")
            else:
                file.write("None\n")

            file.write("\nItems only in first file:\n")
            if unique_to_file1:
                for item in sorted(unique_to_file1):
                    file.write(f"{item}\n")
            else:
                file.write("None\n")

            file.write("\nItems only in second file:\n")
            if unique_to_file2:
                for item in sorted(unique_to_file2):
                    file.write(f"{item}\n")
            else:
                file.write("None\n")

        print(f"Comparison complete. Results saved to {output_file}")

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

### How it works:
1. **Input**: Takes two CSV file paths via command-line arguments.
2. **Reading**: Reads only the first row from each CSV file.
3. **Comparison**:
   - Converts the rows to sets for efficient comparison.
   - Finds:
     - **Common items**: Items present in both rows (set intersection).
     - **Unique to first file**: Items only in the first row (set difference: file1 - file2).
     - **Unique to second file**: Items only in the second row (set difference: file2 - file1).
4. **Output**: Writes results to `comparison.txt` in the directory of the first file, listing:
   - Common items
   - Items only in the first file
   - Items only in the second file
   - Each section is sorted alphabetically; "None" is written if a section is empty.
5. **Error Handling**: Catches file-not-found errors and other exceptions.

### Example usage:
Save the script as `compare_csv.py`. Create two CSV files, e.g.:
- `file1.csv`: `P0001,P0002,P0003`
- `file2.csv`: `P0001,P0004,P0003`

Run the script:
```
python compare_csv.py file1.csv file2.csv
```

**Output** (`comparison.txt`):
```
Comparison Results:

Common Items (in both files):
P0001
P0003

Items only in first file:
P0002

Items only in second file:
P0004
```

### Notes:
- The script ignores the position of items and focuses only on presence/absence.
- Duplicate items in a row are automatically handled (sets remove duplicates).
- The output is written to `comparison.txt` in the directory of the first input file.
- If a file is empty or has no row, the script will treat it as an empty set.

Would you like me to modify the script (e.g., change the output format or add more details)?
