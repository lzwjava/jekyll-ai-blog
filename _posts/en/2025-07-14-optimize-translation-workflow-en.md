---
audio: false
generated: true
lang: en
layout: post
title: Optimize Translation with Paragraph Hashing
translated: false
type: note
---

### Thoughts on Optimizing Your Translation Workflow

Your goal is clear: minimize AI token usage for translating Jekyll blog posts (written in Markdown) into 8 languages by only re-translating changed or new paragraphs, while caching unchanged ones. You want to stick with Markdown for editing, avoid databases/JSON/YAML for core content, and handle special elements like code blocks (which shouldn't be translated). A paragraph-based approach makes sense because it aligns with how you write and edit—translations can be more contextually accurate at that level than sentences.

Key challenges:
- **Identifying changes**: Without version control diffs, you need a way to detect what's new/changed/unchanged. Hashing paragraphs (e.g., using SHA-256 on normalized English text) is efficient and stateless—no need for storing full old versions.
- **Handling Markdown structure**: You can't just split on `\n\n` because code blocks, headers, lists, or other syntax could break things. A simple regex-based splitter might work for basic posts, but a lightweight Markdown parser is better to preserve structure and skip non-translatable parts.
- **Caching**: Keep it file-based and simple (e.g., a JSON file or directory of files) to avoid databases. Cache per-paragraph-hash, per-language.
- **Token savings**: For long posts, this could cut usage by 80-90% on minor edits, as only affected paragraphs hit the AI API.
- **Edge cases**: Added/deleted paragraphs (handle by hashing anew); minor tweaks (e.g., typo fixes) will trigger re-translation unless you normalize whitespace/punctuation; code blocks or inline code must be excluded; if paragraphs reorder, hashes won't match, but that's fine if you treat them as "new."
- **Integration**: Run this as a pre-build script in your Jekyll workflow (e.g., via a bash script or Git hook). No need for Jekyll plugins if you generate translated Markdown files separately.

This is preferable over sentence-level (less accurate context for AI) or full-post (no savings). YAML/JSON would indeed be cumbersome for writing ideas—stick to Markdown.

### Proposed Best Way: Paragraph-Hashing with Caching and Markdown-Aware Parsing

Use a Python script to:
1. Parse the English Markdown into "translatable units" (paragraphs, excluding code blocks, headers if desired, etc.).
2. Hash each unit's English text (normalized, e.g., strip extra whitespace).
3. Check a file-based cache for existing translations by hash/language.
4. Translate missing ones via your AI tool (e.g., DeepSeek/Mistral API).
5. Cache new translations.
6. Reassemble translated Markdown files, preserving non-translatable parts.

**Why this is best**:
- **Simple and low-overhead**: No DB, just files. Runs locally/offline except for AI calls.
- **Flexible**: Handles code blocks by skipping them. Extendable to other Markdown elements (e.g., don't translate headers if they're short).
- **Cost-effective**: Only pays for new/changed paragraphs. For a 10-paragraph post, editing one saves ~90% tokens.
- **Maintainable**: Edit English Markdown naturally; script handles the rest.
- **Tools needed**: Python (you likely have it). Libraries: `hashlib` (built-in for hashing), `markdown` or `mistune` for parsing (if needed; start simple with regex for your "no special syntax" case).

#### Step-by-Step Implementation

1. **Setup**:
   - Create a `translations_cache.json` file (or a directory like `cache/` with hash.json files for scalability).
   - Structure: `{ "hash1": { "fr": "translated text", "es": "...", ... }, "hash2": { ... } }`
   - Store this in your blog repo (git-ignore if sensitive) or a separate dir.
   - List your 8 languages in the script (e.g., ['fr', 'es', 'de', ...]).

2. **Parsing Markdown**:
   - For simple cases (paragraphs + code blocks): Use line-by-line processing to detect fenced code blocks (``````` or `~~~`) and indented code (>3 spaces).
   - Collect "paragraphs" as blocks of consecutive non-code, non-blank lines.
   - Better: Use Python's `markdown` library to convert to HTML, then extract text, but that's lossy for reassembly. Instead, use `mistune` (a fast Markdown parser) to get an AST (abstract syntax tree), which lets you traverse and modify translatable nodes (e.g., 'paragraph' nodes).
   - Install `mistune` if needed (but your env has basics; assume you can pip it locally).

3. **Hashing**:
   - Normalize: `text.strip().lower()` or just `.strip()` to ignore whitespace changes if desired (but that might miss intentional edits).
   - Hash: `hashlib.sha256(normalized.encode()).hexdigest()`

4. **Translation**:
   - Use your AI API wrapper (e.g., for DeepSeek: send prompt like "Translate this paragraph to French: {text}").
   - Batch if possible, but since paragraphs are small, sequential is fine.

5. **Reassembly**:
   - Rebuild the Markdown by replacing translatable blocks with cached/new translations, keeping code/headers intact.

6. **Script Execution**:
   - Run: `python translate_blog.py path/to/english.md`
   - Outputs: `path/to/fr.md`, `path/to/es.md`, etc.
   - For Jekyll: Place these in `_posts/` with lang prefixes, or use a multilingual plugin like `jekyll-polyglot` to handle.

#### Sample Python Script

Here's a basic version using line-by-line parsing (no external libs beyond built-ins). It assumes simple Markdown: paragraphs separated by blank lines, fenced code blocks. Upgrade to `mistune` for complex syntax.

```python
import hashlib
import json
import os
import sys
# Assume you have an AI translate function; replace with your DeepSeek/Mistral API call
def ai_translate(text, lang):
    # Placeholder: return API call result
    return f"Translated to {lang}: {text}"  # Replace with real API

CACHE_FILE = 'translations_cache.json'
LANGUAGES = ['fr', 'es', 'de', 'it', 'pt', 'zh', 'ja', 'ko']  # Your 8 languages

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=4)

def compute_hash(text):
    normalized = text.strip()  # Customize normalization
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

def parse_markdown(md_text):
    lines = md_text.splitlines()
    blocks = []
    current_block = []
    in_code = False
    for line in lines:
        if line.strip().startswith('```') or line.strip().startswith('~~~'):
            in_code = not in_code
            if current_block:
                blocks.append(('text', '\n'.join(current_block)))
                current_block = []
            blocks.append(('code', line))
            continue
        if in_code:
            blocks.append(('code', line))
        else:
            if line.strip():  # Non-blank
                current_block.append(line)
            else:
                if current_block:
                    blocks.append(('text', '\n'.join(current_block)))
                    current_block = []
    if current_block:
        blocks.append(('text', '\n'.join(current_block)))
    return blocks

def translate_post(english_md_path):
    with open(english_md_path, 'r') as f:
        md_text = f.read()

    blocks = parse_markdown(md_text)
    cache = load_cache()

    for lang in LANGUAGES:
        translated_blocks = []
        for block_type, content in blocks:
            if block_type == 'code':
                translated_blocks.append(content)
            else:  # text
                h = compute_hash(content)
                if h not in cache:
                    cache[h] = {}
                if lang not in cache[h]:
                    translation = ai_translate(content, lang)
                    cache[h][lang] = translation
                translated_blocks.append(cache[h][lang])

        # Reassemble with newlines
        translated_md = '\n\n'.join(translated_blocks)  # Adjust for Markdown formatting
        output_path = english_md_path.replace('.md', f'_{lang}.md')
        with open(output_path, 'w') as f:
            f.write(translated_md)

    save_cache(cache)
    print("Translations updated.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script.py path/to/english.md")
    else:
        translate_post(sys.argv[1])
```

**How to use**:
- Replace `ai_translate` with your API logic.
- Run on your post file after edits.
- For headers/lists: Extend `parse_markdown` to detect (e.g., lines starting with `#` or `-` as separate blocks).
- If posts have images/links: They stay unchanged since they're in text blocks.
- Normalization tip: If you want to ignore minor punctuation changes, use regex to strip them before hashing.

#### Enhancements
- **Git integration**: Use `git diff` to pre-identify changed lines, but hashing is simpler.
- **Batch translation**: If API supports, send multiple new paragraphs at once.
- **Error handling**: Retry failed API calls; validate translations.
- **Advanced parsing**: Pip `mistune` and use its renderer to customize (e.g., skip 'code_block' nodes).
- **Testing**: Hash collisions are rare with SHA-256; test on sample posts.

This should save you tokens without complicating your workflow. If your Markdown is more complex, start with this and iterate. Let me know if you need tweaks or help with the API integration!
