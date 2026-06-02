---
audio: false
generated: true
image: false
lang: en
layout: post
model: google/gemini-2.5-flash
title: Diagnosing System Hang Causes
translated: false
type: note
---

It's frustrating when your system hangs during a long-running script\! The Python code you provided appears to process the files sequentially and row-by-row, which is good for memory management, but the issue you're describing—the system hanging and the mouse becoming unresponsive—strongly suggests a **system-wide resource exhaustion** or a **disk I/O bottleneck**, rather than a memory leak within the script itself.

Here's an assessment of the most likely causes and solutions:

## 💾 Potential Causes for System Hang

The hang is likely happening because the script is consuming a critical resource, causing the entire Ubuntu desktop environment (**GNOME/Wayland/Xorg**) to become unresponsive.

-----

### 1\. **High Disk I/O Saturation (Most Likely)**

Reading and writing large amounts of data to disk, especially with a loop that processes many files, can saturate the disk's capacity.

* **Parquet Reading:** Although Parquet is efficient, reading 20 large files involves a massive amount of sequential and potentially random disk reads.
* **Text Writing:** Repeatedly appending (writing) to the output file `fineweb_extracted_all.txt` causes continuous disk writes.
* **The Problem:** When the disk (especially a **SATA HDD** or a low-end **SATA SSD**) is completely saturated with the application's I/O operations, the system's ability to handle other I/O, including reading/writing data for the desktop environment, mouse movements, and kernel processes, severely degrades, leading to a system-wide freeze.

### 2\. **Memory/Swap Thrashing (A possibility, but less likely given your code)**

While your code doesn't *store* all the data in memory, the operating system and pandas still need **working memory** and **page caches**.

* **DataFrame Overhead:** Even if you process row-by-row, loading the *entire* DataFrame for a single Parquet file (`df = pd.read_parquet(parquet_file)`) still requires memory proportional to the size of that file. If your system has limited **RAM** and the DataFrames are large, the OS might start heavily using the **swap partition** on the disk.
* **The Problem:** Swap is much slower than RAM. If the system is constantly swapping data between RAM and the disk (**thrashing**), it exacerbates the I/O bottleneck (Cause 1) and effectively stalls the entire system.

### 3\. **CPU Load Spikes (Less likely to cause a permanent hang)**

While your script isn't heavily CPU-bound, **pandas I/O operations** can occasionally utilize multiple cores or cause brief CPU spikes, but this usually results in slowdowns, not a complete system hang.

-----

## 🛠️ Solutions and Troubleshooting Steps

To fix this, you need to either reduce the load or monitor what's actually happening when the hang occurs.

### 1\. Monitor System Resources

The next time you run the script, open a terminal *before* the script starts and run a system monitoring tool:

* **`htop`** (for CPU and Memory usage)
* **`iotop`** (for Disk I/O usage - *This is the most critical tool for your issue*)
* **`nmon`** (for a comprehensive view of all resources)

Watch **`iotop`** as the script runs. If the **IO** column for your Python process (or the overall disk utilization at the top) is consistently at or near **100%**, then Disk I/O Saturation is the cause.

### 2\. Implement I/O Throttling (Best Coding Solution)

You can introduce a small, strategic delay to allow the disk to "catch up" and free up resources for the OS.

* **Add a small delay:** After processing a large batch of rows, add a `time.sleep()`.

<!-- end list -->

```python
# ... inside the inner loop:
                    if text_content and text_content.strip():
                        f.write(text_content.strip() + "\n\n<|endoftext|><|endoftext|><|endoftext|>\n\n")

                    total_rows_processed += 1

                    # Progress reporting
                    if i % 10000 == 0:
                        print(f"File {file_idx + 1} - Processed {i} rows, Total: {total_rows_processed}")

                        # ✨ ADD THIS LINE to allow the system to breathe
                        # The value (e.g., 0.1 seconds) may need tuning.
                        import time
                        time.sleep(0.1)
```

### 3\. Optimize Text Extraction (Better I/O Efficiency)

Instead of iterating row-by-row in Python, which is generally slow and I/O-intensive, let **pandas** handle the extraction efficiently and only write once per file.

```python
# Instead of:
# for i, row in df.iterrows(): ...
# and writing row by row...

# Use this vectorised approach:
text_col = None
for col in ['text', 'content', 'article', 'text_content', 'body']:
    if col in df.columns:
        text_col = col
        break

if text_col:
    # 1. Select the text column
    texts = df[text_col].astype(str).tolist()

    # 2. Join all texts from this file into one string
    # Apply the separator '<|endoftext|><|endoftext|><|endoftext|>'
    file_output = "\n\n<|endoftext|><|endoftext|><|endoftext|>\n\n".join(texts)

    # 3. Write the entire file's content in one large block
    f.write(file_output.strip() + "\n\n<|endoftext|><|endoftext|><|endoftext|>\n\n")

    total_rows_processed += len(df) # Update count for the entire DataFrame
```

This vectorised method drastically reduces the number of small, slow disk **write** calls, converting them into one large, fast write per Parquet file. This should significantly alleviate the I/O bottleneck.
