---
audio: false
generated: true
lang: en
layout: post
title: 'qBittorrent File Verification: SHA-1 Hashing'
translated: false
type: note
---

When you move file locations in qBittorrent and it checks the files again before seeding, it’s ensuring that the files in the new location are the same as the ones it was originally working with. This verification is critical in torrenting to prevent sharing incorrect or corrupted data. Here’s how the process works and what algorithm it uses:

### How qBittorrent Verifies Files

qBittorrent doesn’t simply trust that the moved files are correct—it checks their integrity by comparing them to information stored in the torrent file. In torrenting, data is split into smaller chunks called **pieces**, and each piece has a unique hash value. These hashes are included in the torrent file and act as a fingerprint for each piece of data. When you move files to a new location, qBittorrent uses these piece hashes to confirm that the files haven’t changed.

The process can be broken down into these steps:

1. **Specify the New Location**: You tell qBittorrent where the files are now located by setting the new file path.
2. **Map Files to the Torrent**: qBittorrent matches the files in the new location to the files listed in the torrent, typically using file names and sizes (since this info is in the torrent file).
3. **Verify Piece Hashes**: qBittorrent reads the data from the new files piece by piece, calculates a hash for each piece, and compares it to the corresponding hash stored in the torrent file.
4. **Confirm Integrity**: If all the calculated hashes match the torrent’s hashes, the files are confirmed to be identical, and qBittorrent can resume seeding. If any piece’s hash doesn’t match, that piece is flagged as incomplete or missing, and qBittorrent may need to redownload it.

### What Algorithm Does It Use?

qBittorrent doesn’t use a full-file checksum (like MD5 or SHA-256 for the entire file), as that would be slow and inefficient, especially for large files. Instead, it relies on the **piece hashes** defined by the BitTorrent protocol. The algorithm used for these piece hashes is **SHA-1**, a widely used cryptographic hash function. Each piece of data (which could be a few kilobytes to a few megabytes, depending on the torrent) is hashed with SHA-1, and those hashes are what qBittorrent checks against.

Using piece hashes instead of a full-file checksum has two big advantages:

- **Efficiency**: Checking smaller pieces is faster than hashing an entire file.
- **Granularity**: If something’s wrong, qBittorrent can pinpoint exactly which pieces need fixing, rather than rejecting the whole file.

### Why This Matters

This hash-based verification ensures that the data you’re seeding from the new location matches what other peers expect, maintaining the integrity of the torrent swarm. Without this check, moving files could lead to sharing corrupted or mismatched data, which would disrupt the torrenting process.

In short, when you move file locations in qBittorrent, it rechecks the files by computing **SHA-1 hashes** of each piece and comparing them to the hashes in the torrent file. That’s how it confirms everything’s correct before seeding resumes.

---

To demonstrate how qBittorrent verifies file integrity using piece hashes (specifically SHA-1 hashes) when moving file locations, here’s a simple Python script. qBittorrent, following the BitTorrent protocol, splits files into pieces, computes SHA-1 hashes for each piece, and uses these hashes to ensure the file’s content remains unchanged, regardless of its location. This script simulates that process by creating a sample file, computing its piece hashes, verifying an identical copy, and then showing how modification causes verification to fail.

### Explanation

- **Piece Hashes**: The script splits a file into fixed-size pieces (e.g., 10 bytes) and computes SHA-1 hashes for each piece, mimicking how a torrent file stores these hashes.
- **Verification**: It checks if a file’s computed hashes match the expected hashes, ensuring integrity.
- **Simulation**: It creates a file, copies it (simulating a move), verifies it, then modifies the copy and verifies again to show how changes are detected.

Here’s the script with comments for clarity:

```python
import hashlib
import shutil
import os

def compute_piece_hashes(file_path, piece_size):
    """Compute SHA-1 hashes for each piece of the file."""
    hashes = []
    with open(file_path, 'rb') as f:
        while True:
            piece = f.read(piece_size)
            if not piece:
                break
            hash_obj = hashlib.sha1(piece)
            hashes.append(hash_obj.hexdigest())
    return hashes

def verify_file_integrity(file_path, piece_size, expected_hashes):
    """Verify the file's integrity by comparing piece hashes."""
    current_hashes = compute_piece_hashes(file_path, piece_size)
    if len(current_hashes) != len(expected_hashes):
        return False
    for current, expected in zip(current_hashes, expected_hashes):
        if current != expected:
            return False
    return True

# Create a sample file with known content
with open('file1.txt', 'w') as f:
    f.write("Hello, this is a test file.")

piece_size = 10  # bytes, small for demonstration

# Compute expected hashes from file1.txt (simulates torrent hashes)
expected_hashes = compute_piece_hashes('file1.txt', piece_size)
print("Expected hashes:", [h[:8] for h in expected_hashes])  # Show first 8 chars for readability

# Copy file1.txt to file2.txt to simulate moving the file
shutil.copyfile('file1.txt', 'file2.txt')

# Verify file2.txt against expected hashes (should pass)
is_valid = verify_file_integrity('file2.txt', piece_size, expected_hashes)
print("Verification of file2.txt (unchanged):", "Valid" if is_valid else "Invalid")

# Modify file2.txt to simulate corruption or change
with open('file2.txt', 'a') as f:
    f.write(" Modified")

# Verify again (should fail due to changed content)
is_valid = verify_file_integrity('file2.txt', piece_size, expected_hashes)
print("Verification of file2.txt (modified):", "Valid" if is_valid else "Invalid")

# Clean up the created files
os.remove('file1.txt')
os.remove('file2.txt')
```

### How It Works

1. **File Creation**: Writes "Hello, this is a test file." (25 bytes) to `file1.txt`.
2. **Hash Computation**: Splits `file1.txt` into pieces of 10 bytes each (e.g., "Hello, thi", "s is a tes", "t file."), computes SHA-1 hashes, and stores them as `expected_hashes`.
3. **Simulate Move**: Copies `file1.txt` to `file2.txt`, representing a file moved to a new location.
4. **Initial Verification**: Checks `file2.txt` against `expected_hashes`. Since the content is identical, it prints "Valid".
5. **Modification**: Appends " Modified" to `file2.txt`, altering its content and size (now 34 bytes, split into 4 pieces).
6. **Second Verification**: Checks the modified `file2.txt`. The number of pieces or their hashes differ, so it prints "Invalid".
7. **Cleanup**: Deletes the temporary files.

### Output Example

```
Expected hashes: ['dffd6021', 'a2b3c4d5', 'e6f789ab']  # Example hash prefixes
Verification of file2.txt (unchanged): Valid
Verification of file2.txt (modified): Invalid
```

(Actual hash values will vary but follow this pattern.)

This script illustrates how qBittorrent ensures file integrity by comparing piece hashes, detecting any changes even after a file is moved, making it a simple yet effective demonstration of the process.
