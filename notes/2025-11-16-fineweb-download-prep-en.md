---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: FineWeb Data Download and Preparation
translated: false
type: note
---

### Downloading the Parquet File

The URL you provided points to a specific Parquet file from the FineWeb dataset (a cleaned subset of CommonCrawl data). This file (`000_00000.parquet` from the `CC-MAIN-2013-20` dump) contains ~1 million rows of English web text, with each row including a `text` column that's already preprocessed for language model training (HTML stripped, deduplicated, quality-filtered via tools like Trafilatura).

To download it:

- Use the Hugging Face CLI: `huggingface-cli download HuggingFaceFW/fineweb data/CC-MAIN-2013-20/000_00000.parquet --local-dir ./fineweb_data`
- Or via Python with `huggingface_hub`:

  ```python
  from huggingface_hub import hf_hub_download

  file_path = hf_hub_download(
      repo_id="HuggingFaceFW/fineweb",
      filename="data/CC-MAIN-2013-20/000_00000.parquet",
      local_dir="./fineweb_data"
  )
  print(f"Downloaded to: {file_path}")
  ```

This saves the ~500MB file locally (e.g., `./fineweb_data/data/CC-MAIN-2013-20/000_00000.parquet`).

For the full dump (hundreds of files), use `snapshot_download` as shown in the dataset docs, but start with this single file for testing.

### Extracting Text

FineWeb's `text` column is plain text ready for training—no need to parse HTML or raw HTML. Use `pandas` or `pyarrow` to load it efficiently. Here's how:

1. **Install Dependencies** (if needed): `pip install pandas pyarrow datasets` (assuming you have them for NanoGPT setup).

2. **Load the Parquet File and Extract Text**:

   ```python
   import pandas as pd
   import os

   # Path to your downloaded file
   parquet_path = "./fineweb_data/data/CC-MAIN-2013-20/000_00000.parquet"

   # Load the Parquet file (efficient for large files)
   df = pd.read_parquet(parquet_path, columns=['text'])  # Only load the text column to save memory

   # Extract all text into a list (or iterate if memory-constrained)
   texts = df['text'].tolist()  # List of ~1M strings

   # Optional: Basic cleaning (FineWeb is already clean, but normalize whitespace)
   import re
   def clean_text(text):
       if pd.isna(text):  # Skip nulls (rare in FineWeb)
           return ''
       text = re.sub(r'\s+', ' ', text.strip())  # Collapse whitespace
       return text if len(text) > 10 else ''  # Filter very short texts

   cleaned_texts = [clean_text(t) for t in texts if t]  # Apply filter

   print(f"Extracted {len(cleaned_texts)} text samples")
   print("Sample:", cleaned_texts[0][:200] + "...")  # Preview first text
   ```

   - **Memory Tip**: This file has ~1M rows, each text ~1-5k characters. On a machine with 16GB RAM, it loads fine. For larger dumps, use `pyarrow` for chunked reading:

     ```python
     import pyarrow.parquet as pq

     table = pq.read_table(parquet_path, columns=['text'])
     texts = table['text'].to_pylist()
     ```

   - **Streaming Alternative** (no full download needed): Use the `datasets` library to iterate without loading everything:

     ```python
     from datasets import load_dataset

     # Load specific dump in streaming mode
     dataset = load_dataset("HuggingFaceFW/fineweb", name="CC-MAIN-2013-20", split="train", streaming=True)

     texts = []
     for i, sample in enumerate(dataset):
         if i >= 100000:  # Limit for testing
             break
         texts.append(sample['text'])

     # Clean as above
     ```

### Preparing for NanoGPT Training

NanoGPT expects a single text file (e.g., `input.txt`) with concatenated documents separated by a special token (like `"<|endoftext|>"`). Here's how to format the extracted text:

```python
# After extracting cleaned_texts from above
with open('input.txt', 'w', encoding='utf-8') as f:
    for text in cleaned_texts:
        f.write(text + "\n<|endoftext|>\n")  # NanoGPT's default separator

print("Saved to input.txt – ready for NanoGPT!")
```

- **Why This Format?** NanoGPT's `data.py` script will read `input.txt`, encode it with your tokenizer (e.g., GPT-2), and create train/val splits. Each document ends with `"<|endoftext|>"` to avoid cross-document context bleed.
- **Customization**:
  - Filter by length: Add `if 100 < len(text.split()) < 10000:` before writing to keep mid-sized docs.
  - Subset for Testing: Use `cleaned_texts[:10000]` for a quick 10k-sample run.
  - Train Command: Once `input.txt` is ready, run `python train.py` in NanoGPT (adjust `--dataset=input.txt` if needed).

This single file gives ~5-10B tokens—great for fine-tuning. For more, download additional Parquet files and concatenate. If you hit memory issues or need help with NanoGPT config, share details!

**Reference**: [FineWeb Dataset Card](https://huggingface.co/datasets/HuggingFaceFW/fineweb)
