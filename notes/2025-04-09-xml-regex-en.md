---
audio: false
generated: true
lang: en
layout: post
title: An XML Regex Script
translated: false
type: note
---

I'll modify the script to use `argparse` for handling command-line arguments. This will allow you to pass the file path directly when running the script:

```python
import xml.etree.ElementTree as ET
import re
import argparse

def extract_look_tags(xml_file):
    # Read the XML file content
    with open(xml_file, 'r') as file:
        xml_content = file.read()

    # Find all <c:look> tags using regex
    pattern = r'<c:look>(\d+)</c:look>'
    matches = re.findall(pattern, xml_content)

    # Print the numbers
    for number in matches:
        print(number)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Extract numbers from <c:look> tags in an XML file')
    parser.add_argument('file_path', help='Path to the XML file')

    # Parse arguments
    args = parser.parse_args()

    # Process the file
    extract_look_tags(args.file_path)

if __name__ == "__main__":
    main()

```

Now you can run the script from the command line like this:

```
python script_name.py path/to/your/xml_file.xml
```

The script will:
1. Use `argparse` to handle the command-line argument for the file path
2. Parse the XML file to find all `<c:look>` tags
3. Extract and print the numbers inside these tags

This approach makes the script more user-friendly and suitable for scripting or batch processing.
