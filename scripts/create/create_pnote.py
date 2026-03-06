from gpa import gpa
from create_note_from_clipboard import create_note_from_content

if __name__ == "__main__":
    from create_note_utils import get_clipboard_content

    content = get_clipboard_content()
    file_path = create_note_from_content(content, directory="pnotes")
    # Call gpa function
    gpa()
