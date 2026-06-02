---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: OpenWebText Dataset Preprocessing Script
translated: false
type: note
---

### Overview

This Python script processes a large text file containing the OpenWebText dataset (a corpus of web-scraped text similar to what's used for training models like GPT-2). The goal is to:

- Split the raw text into manageable "documents" (chunks of text).
- Create a Hugging Face `Dataset` object for easy handling.
- Tokenize the text using the GPT-2 Byte Pair Encoding (BPE) tokenizer from TikToken (ignoring special tokens and appending an end-of-text marker).
- Split the dataset into training (99.95%) and validation (0.05%) sets.
- Save the tokenized data as compact binary files (`train.bin` and `val.bin`) using NumPy's memory-mapped arrays. These files store sequences of token IDs (as 16-bit integers) for efficient loading during machine learning training.

The script is designed for efficiency on multi-core systems, using multiprocessing for tokenization. It's inspired by a data loading module from the Flash Attention repository (linked in the code), which handles similar preprocessing for language model training. Note: OpenWebText is massive (~40GB uncompressed), but this script assumes a pre-downloaded, local `openwebtext.txt` file. The output files are much smaller: `train.bin` ~17GB (9B tokens) and `val.bin` ~8.5MB (4M tokens).

The script prints proxy settings at the start (likely for debugging network issues during any implicit downloads, though none are explicit here). It uses 8 worker processes for tokenization by default.

### Step-by-Step Breakdown

#### 1. Imports and Initial Setup

```python
import os
import tarfile
from tqdm import tqdm
import numpy as np
import tiktoken
from huggingface_hub import hf_hub_download
from datasets import load_dataset # huggingface datasets
import datasets

print("HTTP_PROXY:", os.getenv("HTTP_PROXY"))
print("HTTPS_PROXY:", os.getenv("HTTPS_PROXY"))

# number of workers in .map() call
# good number to use is ~order number of cpu cores // 2
num_proc = 8

# number of workers in load_dataset() call
# best number might be different from num_proc above as it also depends on NW speed.
# it is better than 1 usually though
num_proc_load_dataset = num_proc

enc = tiktoken.get_encoding("gpt2")

datasets.logging.set_verbosity_info()
```

- **Purpose**: Imports libraries for file handling (`os`, `tarfile`), progress bars (`tqdm`), numerical operations (`numpy`), tokenization (`tiktoken`), and Hugging Face utilities (`huggingface_hub`, `datasets`).
- **Proxy prints**: Logs environment variables for HTTP/HTTPS proxies, useful if the script encounters network restrictions (e.g., for downloading tokenizer models, though TikToken handles this internally).
- **Workers**: Sets `num_proc=8` for parallel processing in tokenization (roughly half the CPU cores for balance). `num_proc_load_dataset` matches it but isn't used here (leftover from the inspiration code, which loads from Hugging Face).
- **Encoder**: Loads the GPT-2 BPE tokenizer (`enc`). This converts text to integer token IDs (0–50,256 range).
- **Logging**: Sets Hugging Face datasets logging to "info" level for verbose output during processing.

The `if __name__ == '__main__':` guard ensures the main logic runs only when the script is executed directly (not imported).

#### 2. Reading and Splitting the Text File

```python
if __name__ == '__main__':
    # Read the local openwebtext.txt file
    txt_file = os.path.join(os.path.dirname(__file__), 'openwebtext.txt')
    print(f"Reading from local file: {txt_file}")

    # Read the text content
    texts = []
    with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
        # Read the entire file
        full_text = f.read().strip()

        # Try to split into documents by double newlines first
        documents = full_text.split('\n\n')

        # If we only got one document, split by single newlines
        if len(documents) <= 1:
            documents = full_text.split('\n')

        # If we still only have one document, split by period followed by space
        if len(documents) <= 1:
            # Split on period followed by space, then join back sentences
            sentences = full_text.split('. ')
            # Group sentences into chunks of ~100 sentences per document
            chunk_size = 100
            for i in range(0, len(sentences), chunk_size):
                chunk = '. '.join(sentences[i:i+chunk_size])
                if chunk.strip():
                    texts.append(chunk.strip() + '.')
        else:
            # Process documents from double/single newline splits
            for doc in documents:
                doc = doc.strip()
                if doc:  # Only add non-empty documents
                    texts.append(doc)

        print(f"Created {len(texts)} documents from the text file")
```

- **File reading**: Opens `openwebtext.txt` (assumed to be in the same directory as the script) in UTF-8 mode, ignoring encoding errors. Reads the entire content into `full_text` and strips whitespace.
- **Splitting logic**: Attempts to divide the text into "documents" (logical chunks like paragraphs or articles):
  - **Primary**: Split by double newlines (`\n\n`), common for separating documents in corpora.
  - **Fallback 1**: If that yields ≤1 chunk (e.g., no double newlines), split by single newlines (`\n`) for line-based text.
  - **Fallback 2**: If still ≤1 chunk (e.g., a single block of text), split into sentences by `.` (period + space), then group every 100 sentences into a "document" chunk. This prevents overly long single entries. Adds a period to the end of each chunk for completeness.
- **Output**: Stores non-empty, stripped documents in `texts` list. Prints the total number created (e.g., 10k examples for a subset).
- **Why this way?** OpenWebText is a concatenation of web pages, so splitting creates training examples that aren't just raw dumps. This mimics how datasets like BookCorpus are processed.

#### 3. Creating and Splitting the Dataset

```python
    # Create dataset from texts
    dataset = datasets.Dataset.from_dict({'text': texts})

    # create train/val split from the 10k examples
    split_dataset = dataset.train_test_split(test_size=0.0005, seed=2357, shuffle=True)
    split_dataset['val'] = split_dataset.pop('test') # rename the test split to val
```

- **Dataset creation**: Wraps the `texts` list into a Hugging Face `Dataset` with a single column `'text'`. This enables efficient parallel operations like mapping.
- **Splitting**: Uses `train_test_split` to divide into train (99.95%) and test (0.05%) sets. The small validation size is intentional for huge datasets—enough for evaluation without wasting compute.
  - `test_size=0.0005`: 0.05% for val (e.g., ~50 examples from 100k).
  - `seed=2357`: Fixed random seed for reproducibility.
  - `shuffle=True`: Randomizes before splitting.
- **Rename**: Pops `'test'` and renames to `'val'`. Now `split_dataset` is a dict with `'train'` and `'val'` keys, each a `Dataset` object.

#### 4. Tokenization Function

```python
    # we now want to tokenize the dataset. first define the encoding function (gpt2 bpe)
    def process(example):
        ids = enc.encode_ordinary(example['text']) # encode_ordinary ignores any special tokens
        ids.append(enc.eot_token) # add the end of text token, e.g. 50256 for gpt2 bpe
        # note: I think eot should be prepended not appended... hmm. it's called "eot" though...
        out = {'ids': ids, 'len': len(ids)}
        return out
```

- **Purpose**: Converts text to token IDs for model input.
- **`encode_ordinary`**: Tokenizes the text string into a list of integers (GPT-2 vocab). Ignores any non-standard tokens in the text.
- **Append EOT**: Adds the end-of-text token (ID 50256 for GPT-2) at the end. This signals the sequence boundary during training. (The comment notes a potential prepend vs. append debate, but appending is common in causal LM setups like GPT.)
- **Output**: Returns a dict with `'ids'` (list of token IDs) and `'len'` (sequence length, for later summing).

#### 5. Applying Tokenization

```python
    # tokenize the dataset
    tokenized = split_dataset.map(
        process,
        remove_columns=['text'],
        desc="tokenizing the splits",
        num_proc=num_proc,
    )
```

- **Mapping**: Applies `process` to every example in the train/val datasets using parallel workers (`num_proc=8`).
- **`remove_columns=['text']`**: Drops the original text to save memory (we only need tokens now).
- **Progress**: Shows a progress bar via `desc`. This step can take time for large datasets due to encoding.

#### 6. Saving Tokenized Data to Binary Files

```python
    # concatenate all the ids in each dataset into one large file we can use for training
    for split, dset in tokenized.items():
        arr_len = np.sum(dset['len'], dtype=np.uint64)
        filename = os.path.join(os.path.dirname(__file__), f'{split}.bin')
        dtype = np.uint16 # (can do since enc.max_token_value == 50256 is < 2**16)
        arr = np.memmap(filename, dtype=dtype, mode='w+', shape=(arr_len,))

        # Use adaptive batch size based on dataset size
        total_batches = min(1024, len(dset))
        if total_batches < 1024:
            print(f"Using {total_batches} batches for {split} dataset (size: {len(dset)})")

        idx = 0
        for batch_idx in tqdm(range(total_batches), desc=f'writing {filename}'):
            # Only process if this batch index is valid for the dataset size
            if batch_idx < len(dset):
                # Batch together samples for faster write
                batch = dset.shard(num_shards=total_batches, index=batch_idx, contiguous=True).with_format('numpy')
                arr_batch = np.concatenate(batch['ids'])
                # Write into mmap
                arr[idx : idx + len(arr_batch)] = arr_batch
                idx += len(arr_batch)
        arr.flush()
```

- **Loop over splits**: For `'train'` and `'val'`, compute total token count (`arr_len`) by summing `'len'` fields.
- **Memory-mapped array**: Creates a NumPy memmap file (`train.bin` or `val.bin`) as a writable array of uint16 integers (fits GPT-2's 50,256 max token value; saves ~50% space vs. int32). Shape is 1D: `(total_tokens,)`.
- **Batching for efficiency**: Divides the dataset into up to 1024 shards (`total_batches`) to avoid loading everything into RAM at once. For small datasets (<1024 examples), uses the exact number.
  - **`shard`**: Splits the dataset into contiguous batches (no shuffling here).
  - **`with_format('numpy')`**: Converts the batch to NumPy arrays for fast concatenation.
- **Writing**: Concatenates token IDs from each batch and copies them sequentially into the memmap array starting at `idx`. Tracks progress with `tqdm`.
- **`flush()`**: Ensures all data is written to disk.
- **Why binary/memmap?** These files are huge but streamable. During training, you can load them with `np.memmap('train.bin', dtype=np.uint16, mode='r')` without loading everything into memory.

#### 7. Comments on Output and Usage

```python
    # train.bin is ~17GB, val.bin ~8.5MB
    # train has ~9B tokens (9,035,582,198)
    # val has ~4M tokens (4,434,897)

    # to read the bin files later, e.g. with numpy:
    # m = np.memmap('train.bin', dtype=np.uint16, mode='r')
```

- These are example sizes for the full OpenWebText (your local file might differ).
- **Reading tip**: Use memmap for read-only access. In training loops, you can sample random starting indices and read fixed-length sequences (e.g., 1024 tokens) from the flat array.

### Potential Issues and Notes

- **Memory usage**: Reading the full `openwebtext.txt` into RAM could fail for very large files (40GB+). Consider streaming reads if needed.
- **EOT placement**: The comment questions appending vs. prepending EOT; in practice, appending works for autoregressive models (it marks the end after content).
- **Customization**: Assumes a local file; the inspiration code downloads from Hugging Face, but this version reads locally (faster, no auth needed).
- **Dependencies**: Requires `tiktoken`, `datasets`, `numpy`, `tqdm`. Install via pip if missing.
- **Scalability**: For the real OpenWebText, run on a machine with 64GB+ RAM and fast storage (SSD). The 10k-example split suggests this might be for a subset.

This script turns raw text into a training-ready format, optimized for language models like GPT. If you have questions on modifying it (e.g., different tokenizer or chunk size), let me know!
