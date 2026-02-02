import re
from datetime import datetime
import sys
from create_note_utils import (
    get_clipboard_content,
    clean_grok_tags,
    generate_title,
    generate_short_title,
    create_filename,
    format_front_matter,
    clean_content,
    write_note,
)
from check_duplicate_notes import check_duplicate_notes


def create_note_from_content(content, custom_title=None, directory="notes", date=None, note_model_key: str | None = None):
    """Create a note from provided content instead of clipboard"""
    if not content or not content.strip():
        print("Content is empty or invalid. Aborting.")
        sys.exit(1)
    if len(content.strip()) < 200:
        print("Content is less than 200 characters. Aborting.")
        sys.exit(1)
    if not note_model_key:
        raise ValueError("--note-model is required (no default). Choose a key from openrouter_client.MODEL_MAPPING.")
    
    # Use provided date, otherwise use current date
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Clean grok tags if present
    content = clean_grok_tags(content)

    if custom_title:
        full_title = custom_title
        short_title = custom_title.lower().replace(" ", "-")
        short_title = re.sub(r"[^a-z0-9-]", "", short_title)
    else:
        # Generate titles
        full_title_prompt = (
            lambda c: f"Generate a very short title in English (maximum six words, do not have single quote) for the following text and respond with only the title: {c}"
        )
        full_title = generate_title(content, 6, full_title_prompt)
        
        short_title_prompt = f"Generate a concise title for file naming (max 3 words, lowercase, letters/numbers/hyphens only, no spaces or special characters, no single quotes or underscores, use hyphens to join words) based on this title: {full_title}. Respond with just the title:"
        
        short_title = generate_short_title(short_title_prompt).lower()
        
        # Check if short_title contains underscore
        if '_' in short_title:
            raise ValueError("Short title contains underscore. Please try again with a different title.")

    # Create file path
    file_path = create_filename(short_title, directory, date)

    # Format front matter with date
    front_matter = format_front_matter(full_title, note_model_key, date)

    # Clean content
    content = clean_content(content)

    # Write to file
    write_note(file_path, front_matter, content)
    return file_path


def create_note(date=None, note_model_key: str | None = None):
    # Check for duplicate notes first
    if check_duplicate_notes():
        raise ValueError("Duplicate note found. Aborting note creation.")
    # Get and validate clipboard content
    content = get_clipboard_content()
    # Return the created file path so callers can post-process the file.
    return create_note_from_content(content, date=date, note_model_key=note_model_key)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a note from clipboard content.")
    parser.add_argument("--content", help="Content to create note from (if not provided, uses clipboard)")
    parser.add_argument("--note-model", required=True, help="Model key to annotate in frontmatter (must match scripts.llm.openrouter_client.MODEL_MAPPING)")
    parser.add_argument("--date", help="Override date (YYYY-MM-DD)")
    args = parser.parse_args()

    if args.content:
        file_path = create_note_from_content(args.content, date=args.date, note_model_key=args.note_model)
        print(file_path)
    else:
        file_path = create_note(date=args.date, note_model_key=args.note_model)
        print(file_path)
