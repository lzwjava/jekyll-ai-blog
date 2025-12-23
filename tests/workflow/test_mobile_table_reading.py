import unittest
import re
import os

# Configuration: Maximum allowed columns in markdown tables for mobile readability
MAX_TABLE_COLUMNS = 7

def scan_markdown_files_for_table_columns():
    """Scan English markdown files for tables with more than MAX_TABLE_COLUMNS columns."""
    results = []

    # Only scan original directory for English markdown files
    original_dir = 'original'

    if not os.path.exists(original_dir):
        return results

    # Walk through all subdirectories in original
    for root, dirs, files in os.walk(original_dir):
        for filename in files:
            if not filename.endswith('-en.md'):
                continue

            file_path = os.path.join(root, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Find all markdown tables in the file
                table_pattern = r'^\|\s.*\|\s*$'
                lines = content.split('\n')

                tables_with_many_columns = []

                i = 0
                while i < len(lines):
                    # Look for table start (header row)
                    if re.match(table_pattern, lines[i]) and i + 1 < len(lines):
                        # Check if next line is separator row
                        if re.match(r'^\|\s*[-:]+[-| :]*(?:\s*\|\s*)*$', lines[i + 1]):
                            table_start = i
                            column_count = len(lines[i].split('|')) - 2  # Subtract 2 for empty columns at start/end

                            if column_count > MAX_TABLE_COLUMNS:
                                tables_with_many_columns.append({
                                    'line': table_start + 1,
                                    'column_count': column_count,
                                    'header': lines[i].strip()
                                })

                            # Skip to end of table
                            i += 2
                            while i < len(lines) and re.match(table_pattern, lines[i]):
                                i += 1
                            continue

                    i += 1

                if tables_with_many_columns:
                    results.append({
                        'file': file_path,
                        'tables': tables_with_many_columns
                    })

            except (UnicodeDecodeError, IOError) as e:
                # Skip files that can't be read
                continue

    return results

class TestMobileTableReading(unittest.TestCase):
    def test_mobile_table_column_count(self):
        """Test that English markdown files have tables with MAX_TABLE_COLUMNS or fewer columns for mobile readability."""
        table_results = scan_markdown_files_for_table_columns()

        failing_files = []
        for result in table_results:
            failing_files.append(result)

        if failing_files:
            details = []
            for result in failing_files:
                file_details = f"{result['file']}:"
                for table in result['tables']:
                    file_details += f"\n  Line {table['line']}: {table['column_count']} columns - {table['header']}"
                details.append(file_details)

            self.fail(f"Found {len(failing_files)} files with tables having more than {MAX_TABLE_COLUMNS} columns:\\n{'\\n'.join(details)}")

if __name__ == '__main__':
    unittest.main()