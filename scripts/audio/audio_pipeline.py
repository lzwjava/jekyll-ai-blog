import os
import markdown
from google.cloud import texttospeech
from html import unescape
from bs4 import BeautifulSoup
import re
import random
from pydub import AudioSegment
import tempfile
import argparse
import yaml

# Fixed output directory
OUTPUT_DIRECTORY = "assets/audios"


def split_into_sentences(text):
    """
    Splits text into sentences using regex.
    Handles common sentence endings.
    """
    sentence_endings = re.compile(r"(?<=[.!?。！？]) +")
    sentences = sentence_endings.split(text)
    return sentences


def split_text(text, max_bytes=3000):
    """
    Splits text into chunks not exceeding max_bytes.
    First splits text into sentences to ensure sentences are not split across chunks.
    If a single sentence exceeds max_bytes, it further splits the sentence.
    """
    sentences = split_into_sentences(text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        # Check if the sentence itself exceeds max_bytes
        if len(sentence.encode("utf-8")) > max_bytes:
            # Further split the sentence by commas or other delimiters
            sub_sentences = re.split(r", |; |: |，|；|：|。", sentence)
            for sub_sentence in sub_sentences:
                sub_sentence = sub_sentence.strip()
                if not sub_sentence:
                    continue
                tentative_chunk = f"{current_chunk} {sub_sentence}".strip()
                if len(tentative_chunk.encode("utf-8")) > max_bytes:
                    if current_chunk:
                        chunks.append(current_chunk)
                    current_chunk = sub_sentence
                else:
                    current_chunk = tentative_chunk
        else:
            tentative_chunk = f"{current_chunk} {sentence}".strip()
            if len(tentative_chunk.encode("utf-8")) > max_bytes:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence
            else:
                current_chunk = tentative_chunk

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def text_to_speech(text, output_filename, task, language_code="en-US", dry_run=False):
    if dry_run:
        print(f"Dry run: Would generate audio for file: {output_filename}")
        return True
    print(f"Generating audio for: {output_filename}")
    try:
        client = texttospeech.TextToSpeechClient()
        text_chunks = split_text(text)
        if not text_chunks:
            print("No text chunks to process.")
            return False

        audio_segments = []
        for idx, chunk in enumerate(text_chunks):
            synthesis_input = texttospeech.SynthesisInput(text=chunk)
            if language_code == "en-US":
                voice_name = random.choice(
                    ["en-US-Journey-D", "en-US-Journey-F", "en-US-Journey-O"]
                )
            elif language_code == "cmn-CN":
                voice_name = random.choice(
                    [
                        "cmn-CN-Wavenet-A",
                        "cmn-CN-Wavenet-B",
                        "cmn-CN-Wavenet-C",
                        "cmn-CN-Wavenet-D",
                    ]
                )
            elif language_code == "es-ES":
                voice_name = random.choice(
                    ["es-ES-Journey-D", "es-ES-Journey-F", "es-ES-Journey-O"]
                )
            elif language_code == "fr-FR":
                voice_name = random.choice(
                    ["fr-FR-Journey-D", "fr-FR-Journey-F", "fr-FR-Journey-O"]
                )
            elif language_code == "yue-HK":
                voice_name = random.choice(
                    [
                        "yue-HK-Standard-A",
                        "yue-HK-Standard-B",
                        "yue-HK-Standard-C",
                        "yue-HK-Standard-D",
                    ]
                )
            elif language_code == "ja-JP":
                voice_name = random.choice(
                    ["ja-JP-Neural2-B", "ja-JP-Neural2-C", "ja-JP-Neural2-D"]
                )
            elif language_code == "hi-IN":
                voice_name = random.choice(
                    [
                        "hi-IN-Wavenet-A",
                        "hi-IN-Wavenet-B",
                        "hi-IN-Wavenet-C",
                        "hi-IN-Wavenet-D",
                        "hi-IN-Wavenet-E",
                        "hi-IN-Wavenet-F",
                    ]
                )
            elif language_code == "de-DE":
                voice_name = random.choice(
                    ["de-DE-Journey-D", "de-DE-Journey-F", "de-DE-Journey-O"]
                )
            elif language_code == "ar-XA":
                voice_name = random.choice(
                    [
                        "ar-XA-Wavenet-A",
                        "ar-XA-Wavenet-B",
                        "ar-XA-Wavenet-C",
                        "ar-XA-Wavenet-D",
                    ]
                )

            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code, name=voice_name
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                effects_profile_id=["small-bluetooth-speaker-class-device"],
            )

            try:
                response = client.synthesize_speech(
                    input=synthesis_input, voice=voice, audio_config=audio_config
                )
            except Exception as e:
                # Check if the error is due to sentences being too long
                error_message = str(e).lower()
                if (
                    "sentences that are too long" in error_message
                    or "text too long" in error_message
                ):
                    print(
                        f"Chunk {idx + 1} has sentences that are too long. Attempting to split further."
                    )
                    # Split the chunk into smaller parts and process each
                    sub_sentences = split_into_sentences(chunk)
                    for sub_idx, sub_sentence in enumerate(sub_sentences):
                        sub_sentence = sub_sentence.strip()
                        if not sub_sentence:
                            continue
                        sub_synthesis_input = texttospeech.SynthesisInput(
                            text=sub_sentence
                        )
                        try:
                            sub_response = client.synthesize_speech(
                                input=sub_synthesis_input,
                                voice=voice,
                                audio_config=audio_config,
                            )
                            with tempfile.NamedTemporaryFile(
                                delete=False, suffix=".mp3"
                            ) as tmp_sub_file:
                                tmp_sub_file.write(sub_response.audio_content)
                                sub_temp_filename = tmp_sub_file.name
                            sub_audio_segment = AudioSegment.from_mp3(sub_temp_filename)
                            audio_segments.append(sub_audio_segment)
                            os.remove(sub_temp_filename)
                            print(
                                f"Sub-chunk {sub_idx + 1}/{len(sub_sentences)} of chunk {idx + 1} processed."
                            )
                        except Exception as sub_e:
                            print(
                                f"Failed to process sub-chunk {sub_idx + 1} of chunk {idx + 1}: {sub_e}"
                            )
                            continue
                    continue  # Move to the next chunk
                else:
                    print(f"Error on chunk {idx + 1}: {e}")
                    return False

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tmp_file.write(response.audio_content)
                temp_filename = tmp_file.name
            audio_segment = AudioSegment.from_mp3(temp_filename)
            audio_segments.append(audio_segment)
            os.remove(temp_filename)
            print(f"Chunk {idx + 1}/{len(text_chunks)} processed.")

        if audio_segments:
            combined = audio_segments[0]
            for segment in audio_segments[1:]:
                combined += segment
            combined.export(output_filename, format="mp3")
            print(f"Audio content written to {output_filename}")
            return True
        else:
            print("No audio segments to combine.")
            return False
    except Exception as e:
        print(f"An error occurred while generating audio for {output_filename}: {e}")
        return False


def md_to_text(md_file):
    print(f"Reading file: {md_file}")
    try:
        with open(md_file, "r", encoding="utf-8") as file:
            md_content = file.read()
        # Extract front matter
        front_matter = {}
        if md_content.startswith("---"):
            _, front_matter_str, md_content = md_content.split("---", 2)
            try:
                front_matter = yaml.safe_load(front_matter_str)
            except yaml.YAMLError as e:
                print(f"Error parsing front matter: {e}")

        html = markdown.markdown(md_content)
        text = unescape(BeautifulSoup(html, "html.parser").get_text())
        return text, front_matter
    except Exception as e:
        print(f"Error reading or parsing {md_file}: {e}")
        return "", {}


def get_last_n_files(input_dir, n=10):
    """
    Retrieve the last n Markdown files from the input directory based on filename (descending order).
    """
    try:
        # Get all markdown files
        md_files = []
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.endswith(".md"):
                    md_files.append(os.path.join(root, file))
        # Sort by filename descending
        md_files_sorted = sorted(
            md_files, key=lambda x: os.path.basename(x), reverse=True
        )
        # Get the top n files
        last_n_files = md_files_sorted[:n]
        return last_n_files
    except Exception as e:
        print(f"Error retrieving files from {input_dir}: {e}")
        return []


def process_markdown_files(
    task, input_dir, output_dir, n=10, max_files=100, dry_run=False
):
    os.makedirs(output_dir, exist_ok=True)

    if task == "posts":
        total_files = 0
        last_md_files = []
        for lang_dir in os.listdir(input_dir):
            lang_path = os.path.join(input_dir, lang_dir)
            if os.path.isdir(lang_path):
                files = get_last_n_files(lang_path, n)
                last_md_files.extend(files)
                total_files += len(files)

        print(
            f"Total Markdown files to process in '_posts' (last {n} from each language dir): {total_files}"
        )
    elif task == "notes":
        last_md_files = get_last_n_files(input_dir, n)
        total_files = len(last_md_files)
        print(f"Total Markdown files to process in 'notes' (last {n}): {total_files}")
    else:
        print("Invalid task specified.")
        return

    if total_files == 0:
        print(f"No Markdown files found in '{input_dir}' directory.")
        return

    files_processed = 0

    for md_file_path in last_md_files:
        filename = os.path.basename(md_file_path)
        output_filename = os.path.join(
            output_dir, f"{os.path.splitext(filename)[0]}.mp3"
        )
        if os.path.exists(output_filename):
            print(f"Skipping {filename}: {output_filename} already exists.")
            continue
        article_text, front_matter = md_to_text(md_file_path)
        if not article_text.strip():
            print(f"Skipping {filename}: No content to convert.")
            continue
        print(f"\nProcessing {files_processed + 1}/{total_files}: {filename}")
        try:
            # Determine language based on filename suffix

            language_code = "en-US"

            if filename.endswith("-zh.md"):
                language_code = "cmn-CN"
            elif filename.endswith("-es.md"):
                language_code = "es-ES"
            elif filename.endswith("-fr.md"):
                language_code = "fr-FR"
            elif filename.endswith("-de.md"):
                language_code = "de-DE"
            elif filename.endswith("-ja.md"):
                language_code = "ja-JP"
            elif filename.endswith("-hi.md"):
                language_code = "hi-IN"
            elif filename.endswith("-ar.md"):
                language_code = "ar-XA"
            elif filename.endswith("-hant.md"):
                language_code = "yue-HK"
            elif filename.endswith("-en.md"):
                language_code = "en-US"

            success = text_to_speech(
                text=article_text,
                output_filename=output_filename,
                task=task,
                language_code=language_code,
                dry_run=dry_run,
            )
            if success:
                files_processed += 1
                print(f"File {files_processed}/{total_files} processed.\n")
                if task == "posts" and "audio" not in front_matter:
                    # Update front matter with audio: true
                    with open(md_file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) == 3:
                            front_matter_str = parts[1]
                            try:
                                front_matter = yaml.safe_load(front_matter_str)
                            except yaml.YAMLError as e:
                                print(f"Error parsing front matter: {e}")
                                continue
                            front_matter["audio"] = True
                            updated_front_matter_str = yaml.dump(
                                front_matter, sort_keys=False
                            )
                            updated_content = (
                                f"---\n{updated_front_matter_str}---\n{parts[2]}"
                            )
                            with open(md_file_path, "w", encoding="utf-8") as f:
                                f.write(updated_content)
                            print(
                                f"Updated front matter in {filename} with audio: true"
                            )
                        else:
                            print(
                                f"Unexpected format in {filename}, cannot update front matter"
                            )
                    else:
                        print(
                            f"No front matter found in {filename}, cannot update front matter"
                        )
            else:
                print(f"Failed to generate audio for {filename}")
            if task in ["posts", "notes"] and files_processed >= max_files:
                print("Processed the maximum allowed files.")
                break
        except Exception as e:
            print(f"Failed to process {filename}: {e}")
            continue

    print(f"Processing complete! {files_processed}/{total_files} files processed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process Markdown files to generate audio."
    )
    parser.add_argument(
        "--task",
        choices=["posts", "notes"],
        required=True,
        help="Task to perform: 'posts', or 'notes'",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=10,
        help="Number of last files to process (only for 'posts' and 'notes').",
    )
    parser.add_argument(
        "--max_files",
        type=int,
        default=100,
        help="Maximum number of files to process (only for 'pages').",
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Perform a dry run without generating audio.",
    )

    args = parser.parse_args()

    # Determine input_dir based on task
    if args.task == "posts":
        input_directory = "_posts"
        n = args.n
        max_files = args.max_files  # Typically 10 for 'posts', but keeping flexibility
    elif args.task == "notes":
        input_directory = "notes"
        n = args.n
        max_files = args.max_files  # Typically 10 for 'notes', but keeping flexibility
    else:
        print("Invalid task specified. Choose either 'posts', or 'notes'.")
        exit(1)

    # Handle 'n' and 'max_files' based on task
    if args.task in ["posts", "notes"]:
        process_markdown_files(
            task=args.task,
            input_dir=input_directory,
            output_dir=OUTPUT_DIRECTORY,
            n=args.n,
            max_files=args.max_files,  # Typically 10
            dry_run=args.dry_run,
        )
