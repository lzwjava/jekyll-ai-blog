---
audio: true
generated: false
image: false
lang: en
layout: post
title: Conversation Audio Generation
type: post
---

Inspired by a YouTube video featuring a discussion about DeepSeek-V3, I've been experimenting with AI-generated conversations. My goal is to create realistic audio dialogues using Google Text-to-Speech and ffmpeg for audio generation and concatenation. The following code outlines my current approach to simulating a natural back-and-forth conversation.

## Prompt

> Create a natural and extended conversation between two experts, A and B, with at least 100 turns. The experts should discuss a specific topic in depth, with the conversation flowing back and forth. Both participants should ask questions, share insights, and explore the nuances of the subject matter. The format should be as follows:

```json
[
    {
      "speaker": "A",
      "line": "Hey, I’ve been hearing a lot about Machine Learning (ML), Deep Learning (DL), and GPT lately. Can you break it down for me?"
    },
    {
      "speaker": "B",
      "line": "Sure! Let’s start with the basics. Machine Learning is a field of computer science where systems learn from data to improve their performance without being explicitly programmed. Think of it as teaching a computer to recognize patterns."
    }
]
```

## Code

```python
import os
import json
import random
import subprocess
from google.cloud import texttospeech
import tempfile
import time
import argparse

# Fixed output directory for conversations
OUTPUT_DIRECTORY = "assets/conversations"
INPUT_DIRECTORY = "scripts/conversation"

def text_to_speech(text, output_filename, voice_name=None):
    print(f"Generating audio for: {output_filename}")
    try:
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code="en-US", name=voice_name)
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            effects_profile_id=["small-bluetooth-speaker-class-device"]
        )

        retries = 5
        for attempt in range(1, retries + 1):
            try:
                response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
                with open(output_filename, 'wb') as out:
                    out.write(response.audio_content)
                print(f"Audio content written to {output_filename}")
                return True
            except Exception as e:
                print(f"Error on attempt {attempt}: {e}")
                if attempt == retries:
                    print(f"Failed to generate audio after {retries} attempts.")
                    return False
                wait_time = 2 ** attempt
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
    except Exception as e:
        print(f"An error occurred while generating audio for {output_filename}: {e}")
        return False

def process_conversation(filename):
    filepath = os.path.join(INPUT_DIRECTORY, filename)
    output_filename = os.path.join(OUTPUT_DIRECTORY, os.path.splitext(filename)[0] + ".mp3")

    if os.path.exists(output_filename):
        print(f"Audio file already exists: {output_filename}")
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            conversation = json.load(f)
    except Exception as e:
        print(f"Error loading conversation file {filename}: {e}")
        return

    temp_files = []

    voice_options = ["en-US-Journey-D", "en-US-Journey-F", "en-US-Journey-O"]
    voice_name_A = random.choice(voice_options)
    voice_name_B = random.choice(voice_options)
    while voice_name_A == voice_name_B:
        voice_name_B = random.choice(voice_options)

    for idx, line_data in enumerate(conversation):
        speaker = line_data.get("speaker")
        line = line_data.get("line")
        if not line:
            continue
        temp_file = os.path.join(OUTPUT_DIRECTORY, f"temp_{idx}.mp3")
        temp_files.append(temp_file)

        voice_name = None
        if speaker == "A":
            voice_name = voice_name_A
        elif speaker == "B":
            voice_name = voice_name_B

        if not text_to_speech(line, temp_file, voice_name=voice_name):
            print(f"Failed to generate audio for line {idx+1} of {filename}")
            # Clean up temp files
            for temp_file_to_remove in temp_files:
                if os.path.exists(temp_file_to_remove):
                    os.remove(temp_file_to_remove)
            return

    if not temp_files:
        print(f"No audio generated for {filename}")
        return

    # Concatenate using ffmpeg
    concat_file = os.path.join(OUTPUT_DIRECTORY, "concat.txt")
    with open(concat_file, 'w') as f:
        for temp_file in temp_files:
            f.write(f"file '{os.path.abspath(temp_file)}'\n")

    try:
        subprocess.run(
            ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_file, '-c', 'copy', output_filename],
            check=True,
            capture_output=True
        )
        print(f"Successfully concatenated audio to {output_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error concatenating audio: {e.stderr.decode()}")
    finally:
        os.remove(concat_file)
        for temp_file in temp_files:
            os.remove(temp_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process conversation JSON files to generate audio.")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    for filename in os.listdir(INPUT_DIRECTORY):
        if filename.endswith(".json"):
            process_conversation(filename)
```

## Cover

```bash
ffmpeg -i deepseek.jpg -vf "crop=854:480" deepseek_480p_cropped.jpg
```

## Video

```bash
ffmpeg -loop 1 -i deepseek.jpg -i deepseek.mp3 -c:v libx264 -tune stillimage -c:a aac -b:a 192k -shortest output_video.mp4
```
