LANGUAGES = ["en", "zh", "ja", "es", "hi", "fr", "de", "ar", "hant"]

import os  # noqa: E402
import shutil  # noqa: E402

OUTPUT_DIRECTORY = "assets/pdfs"


def move_pdfs():
    for lang in LANGUAGES:
        lang_dir = os.path.join(OUTPUT_DIRECTORY, lang)
        os.makedirs(lang_dir, exist_ok=True)

    for filename in os.listdir(OUTPUT_DIRECTORY):
        if filename.endswith(".pdf"):
            for lang in LANGUAGES:
                if filename.endswith(f"-{lang}.pdf"):
                    source_path = os.path.join(OUTPUT_DIRECTORY, filename)
                    dest_path = os.path.join(OUTPUT_DIRECTORY, lang, filename)
                    shutil.move(source_path, dest_path)
                    print(f"Moved {filename} to {lang_dir}")
                    break


if __name__ == "__main__":
    move_pdfs()
