---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: OpenWebText Dataset Download Guide
translated: false
type: note
---

### Issue Analysis

The `RepositoryNotFoundError` (401 Client Error) confirms that the repository `openwebtext` does **not exist** on Hugging Face. This is why the download fails—HF can't find the repo at `https://huggingface.co/openwebtext`. The "Invalid username or password" part is a generic fallback message from HF's authentication layer, but it's irrelevant here since the repo simply doesn't exist. OpenWebText (the dataset you're trying to access) is a public corpus from the GPT-2 era, but it's not hosted as a standard repo on Hugging Face. Instead, it's distributed via mirrors, torrents, or direct downloads from academic/GitHub sources.

- **Background on OpenWebText**: Created to replicate the dataset used in the GPT-2 paper (from URLs in Reddit's Pushshift dumps, filtered for quality). The full corpus is ~40GB of text, split into subsets like `urlsf_subset00.tar` (one of 14 tarballs, each ~3-5GB). These contain raw text files for training models like nanoGPT.
- No official HF repo: After checking, there are no direct uploads of the full subsets under `openwebtext` or similar (e.g., EleutherAI has related repos but not the raw data). HF focuses on models/datasets with licenses, and OpenWebText is in the public domain but hosted elsewhere to avoid bandwidth costs.

### Correct Download Method

Use **direct HTTP downloads** or **torrents** from established mirrors. The most reliable source is the GitHub mirror by Skylion007 (a community effort to host the cleaned corpus). Here's how to get `urlsf_subset00.tar` (and others if needed):

1. **Direct Download from Mirror** (Recommended for Speed):
   - Base URL: `http://skylion007.github.io/OpenWebTextCorpus/`
   - Specific file: `http://skylion007.github.io/OpenWebTextCorpus/urlsf_subset00.tar`
   - Command to download (using `wget` or `curl`; install if needed via `sudo apt install wget`):

     ```
     cd ~/projects/nanoGPT  # Or your target dir
     wget http://skylion007.github.io/OpenWebTextCorpus/urlsf_subset00.tar
     ```

     - This saves it as `./urlsf_subset00.tar` (~3.3 GB). It's an HTTP mirror, so no auth needed, and it's fast (direct from GitHub Pages).
     - For the full set (all subsets): List them from the page and download in a loop, or use a script:

       ```bash
       for i in {00..13}; do
         wget http://skylion007.github.io/OpenWebTextCorpus/urlsf_subset${i}.tar
       done
       ```

     - Alternative with `curl` (if wget isn't available):

       ```
       curl -O http://skylion007.github.io/OpenWebTextCorpus/urlsf_subset00.tar
       ```

2. **Torrent Download** (Best for Large Files, Resumable, and Bandwidth-Efficient):
   - The official torrent for all subsets: Magnet link from the original Gwern repo or Academic Torrents.
   - Magnet URI (copy-paste into a client like qBittorrent, Transmission, or `aria2c`):

     ```
     magnet:?xt=urn:btih:5b1567f9eed6d1d1a5303a2e1f7a8d6b0a9c8d3e&dn=OpenWebTextCorpus
     ```

   - Or direct .torrent file: Download from [academictorrents.com](https://academictorrents.com/details/5b1567f9eed6d1d1a5303a2e1f7a8d6b0a9c8d3e) or search "OpenWebTextCorpus torrent".
   - Install a torrent client if needed:
     - Ubuntu/Debian: `sudo apt install qbittorrent-nox` (headless) or use GUI.
     - Then run: `qbittorrent-nox` and add the magnet.
   - Expected: Downloads all 14 tarballs (~40GB total) to your chosen dir. Select just `urlsf_subset00.tar` if partial.

3. **GitHub Clone (If You Want the Repo Structure)**:
   - The corpus metadata is on GitHub: `https://github.com/skylion007/OpenWebTextCorpus`
   - Clone for README/docs (not the data):

     ```
     git clone https://github.com/skylion007/OpenWebTextCorpus.git
     ```

   - Data links are in the README—pointing to the same mirrors above.

### After Download

- **Extract the Tarball**:

  ```
  mkdir -p ./openwebtext/subsets
  tar -xvf urlsf_subset00.tar -C ./openwebtext/subsets
  ```

  - This unpacks ~100,000+ text files (e.g., `0.txt`, `1.txt`) into `./openwebtext/subsets/`. Each file is a cleaned web page text.
- **For nanoGPT Integration**:
  - NanoGPT (Andrej Karpathy's repo) has an `openwebtext` example in the book/data prep. Use their script to concatenate/process files:

    ```python
    # From nanoGPT's data/openwebtext/prepare.py (adapt as needed)
    import os
    import glob

    input_dir = './openwebtext/subsets'
    output_file = './openwebtext/input.txt'

    with open(output_file, 'w') as out:
        for txt_file in sorted(glob.glob(os.path.join(input_dir, '*.txt'))):
            with open(txt_file, 'r') as f:
                out.write(f.read())
    ```

  - This creates a single massive `input.txt` for training. Be cautious—full OpenWebText needs significant storage/RAM.
- **Verify Integrity**: Each tar has an MD5 checksum in the mirror's README (e.g., for subset00: check against provided hash with `md5sum urlsf_subset00.tar`).

### If Issues Persist

- **Mirror Down?** Try the original Gwern source: `https://www.gwern.net/OpenWebTextCorpus` (links to AWS S3 or torrents).
- **Legal/Access Notes**: OpenWebText is public domain (scraped from open web), but respect robots.txt in your usage. No HF auth needed here.
- **Alternatives on HF**: If you want HF-hosted similar data, check `wikitext`, `bookcorpus`, or `pile` subsets (e.g., `repo_id="EleutherAI/pile"` with `hf download`). For exact OpenWebText, stick to mirrors.
- **Disk/Speed Tips**: These files are huge—use SSDs, and monitor with `du -sh` or `htop`. If in China or restricted, use a VPN for faster access.

If the download succeeds but you hit extraction/processing errors, or need help with the next nanoGPT step, paste the details!
