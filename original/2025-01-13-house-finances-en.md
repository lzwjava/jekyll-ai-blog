---
audio: true
generated: false
image: false
lang: en
layout: post
title: Tracking Our House Finances
type: post
---

Recently, I created a markdown document to keep track of our house's financial transactions.

The house belongs to my wife and me. My parents gave us money, and we borrowed money from my sister and my maternal uncle. Although my maternal uncle sent money to me, my father later repaid that amount.

We paid 50% of the total price of our house as a down payment, and we borrowed the other half from the Agricultural Bank of China. The contract lasts for 20 years, and the current interest rate is 3.65%.

When I was jobless, my wife and my father provided me with funds to cover the monthly mortgage payments. Consequently, there are many transactions involved.

I use China Merchants Bank as my primary bank. China Merchants Bank allows filtering of transactions by whether they are incoming or outgoing, and by a minimum amount. It also supports filtering by keywords, which is very helpful.

Another helpful aspect is the prevalence of AI. It can also assist with this task. Using AI-powered OCR, specifically Grok, I was able to extract text from transaction records with the Guangzhou Electric Power Bureau.

As the later table is based on previous numbers, it is better to check the numbers first to make sure everything is correct before moving forward.

The code below helps generate a PDF from the markdown. It has some special settings to support Chinese character rendering in PDF.


```python
import os
import subprocess

# Configuration
CJK_FONT = "Heiti SC"
GEOMETRY = "margin=1in"
input_markdown_path = "mortgage.md"  # Replace with your input Markdown file
output_pdf_path = "mortgage.pdf"    # Replace with your desired output PDF file

# Check if input file exists
if not os.path.exists(input_markdown_path):
    raise Exception(f"Input file does not exist: {input_markdown_path}")

# Construct the Pandoc command
command = [
    'pandoc',
    input_markdown_path,
    '-o', output_pdf_path,
    '-f', 'markdown',
    '--pdf-engine', 'xelatex',
    '-V', f'CJKmainfont={CJK_FONT}',
    '-V', f'CJKsansfont={CJK_FONT}',
    '-V', f'CJKmonofont={CJK_FONT}',
    '-V', f'geometry:{GEOMETRY}',
    '-V', 'classoption=16pt',
    '-V', 'CJKoptions=Scale=1.1',
    '-V', 'linestretch=1.5'
]

# Run the Pandoc command
try:
    subprocess.run(command, check=True)
    print(f"PDF successfully generated: {output_pdf_path}")
except subprocess.CalledProcessError as e:
    print(f"Error generating PDF: {e}")
```
