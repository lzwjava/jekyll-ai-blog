---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Python XML Parsing with xml.etree
translated: false
type: note
---

### Overview of xml.etree in Python

`xml.etree` is a built-in Python module (specifically `xml.etree.ElementTree`) for parsing and manipulating XML data. It provides a tree-like structure where you can read, write, modify, and navigate XML elements efficiently. It's lightweight and doesn't require external libraries, making it ideal for basic XML tasks. Import it with `import xml.etree.ElementTree as ET`.

### Parsing XML

To load XML into memory, use parsing methods:

- **From a string**: `ET.fromstring(xml_string)` returns an Element object representing the root.
- **From a file**: `ET.parse(filename)` returns an ElementTree object, which you can access via `.getroot()`.

```python
import xml.etree.ElementTree as ET

# Parse from string
xml_data = "<root><child>text</child></root>"
root = ET.fromstring(xml_data)

# Parse from file
tree = ET.parse('example.xml')
root = tree.getroot()
```

### Navigating Elements

Once parsed, you can traverse the XML tree:

- **Access children**: Use `root[0]` for indexed access or iterate with `for child in root:`.
- **Find elements**:
  - `root.find('tag')` gets the first matching child.
  - `root.findall('tag')` gets all matching children.
- **Access text and attributes**:
  - Text content: `element.text`
  - Attributes: `element.attrib` (a dict)

```python
# Example XML: <bookstore><book id="1"><title>Python</title></book></bookstore>
for book in root.findall('book'):
    title = book.find('title').text
    book_id = book.attrib['id']
    print(f"Book {book_id}: {title}")
```

### Modifying XML

Edit elements dynamically:

- **Add elements**: `ET.SubElement(parent, 'new_tag')` creates and attaches a new child.
- **Set text/attributes**: `element.text = 'new text'`; `element.set('attr', 'value')`.
- **Remove elements**: `root.remove(child)`.

```python
new_child = ET.SubElement(root, 'new_element')
new_child.text = 'Added content'
new_child.set('attr', 'value')
```

### Writing XML

To save modifications back to XML:

- **To a string**: `ET.tostring(root, encoding='unicode')`.
- **To a file**: `tree.write('output.xml')`.

```python
xml_output = ET.tostring(root, encoding='unicode')
with open('output.xml', 'w') as f:
    f.write(xml_output)

# Or directly
tree.write('output.xml')
```

### Complete Example

Here's a full script to parse, modify, and write XML:

```python
import xml.etree.ElementTree as ET

# Input XML string
xml_str = """<library>
  <book id="1"><title>1984</title><author>Orwell</author></book>
</library>"""

root = ET.fromstring(xml_str)

# Add a new book
new_book = ET.SubElement(root, 'book', id="2")
ET.SubElement(new_book, 'title').text = 'Brave New World'
ET.SubElement(new_book, 'author').text = 'Huxley'

# Print all books
for book in root:
    title = book.find('title').text
    author = book.find('author').text
    print(f"{title} by {author}")

# Write to file
ET.tostring(root, encoding='unicode')
# Or root.write('library.xml')
```

### Notes

- Handle namespaces with `xmlns='{namespace}'` in find queries, e.g., `root.find('{http://example.com}tag')`.
- For large files, consider iterative parsing with `ET.iterparse()`.
- Be cautious with user-input XML to avoid XML vulnerabilities like injection.
- For complex needs, libraries like lxml offer extended features.
