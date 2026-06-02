---
audio: false
generated: true
lang: en
layout: post
title: Create Educational Videos with Python
translated: false
type: note
---

To create educational short videos with a black background and captions synchronized with audio generated from text using the DeepSeek API and Google Cloud Text-to-Speech API, you can use Python to orchestrate the process. Below is a step-by-step guide and a Python script that accomplishes this. The script will:

1. Use DeepSeek API to generate or refine a script (assuming you provide the educational content).
2. Use Google Cloud Text-to-Speech API to convert the script into audio.
3. Use a library like `moviepy` to create a video with a black background and captions synchronized with the audio.

### Prerequisites

- **DeepSeek API Key**: Sign up at [DeepSeek](https://api-docs.deepseek.com/) and obtain an API key.
- **Google Cloud Text-to-Speech API**:
  - Set up a Google Cloud project and enable the Text-to-Speech API.
  - Create a service account and download the JSON credentials file.
  - Install the Google Cloud Text-to-Speech client library: `pip install google-cloud-texttospeech`.
- **Python Libraries**:
  - Install required libraries: `pip install openai moviepy requests`.
- **FFmpeg**: Ensure FFmpeg is installed for `moviepy` to handle video rendering (download from [FFmpeg website](https://ffmpeg.org/) or install via package manager).

### Steps

1. **Generate or Refine Script with DeepSeek API**: Use DeepSeek to create or polish the educational script, ensuring it’s concise and suitable for a 1-minute video.
2. **Convert Text to Audio with Google Cloud Text-to-Speech**: Split the script into paragraphs, generate audio for each, and save as separate audio files.
3. **Create Video with MoviePy**: Generate a video with a black background, display captions for each paragraph synchronized with the audio, and combine them into a final 1-minute video.

### Python Script

The following script assumes you have a text file with the educational content (paragraphs) and generates a video with a black background and captions.

```python
import os
from openai import OpenAI
from google.cloud import texttospeech
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip, concatenate_videoclips
import requests

# Set up environment variables
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/google-credentials.json"  # Update with your credentials file path
DEEPSEEK_API_KEY = "your_deepseek_api_key"  # Update with your DeepSeek API key

# Initialize DeepSeek client
deepseek_client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

# Function to refine script with DeepSeek
def refine_script_with_deepseek(script):
    prompt = f"""
    You are an expert scriptwriter for educational videos. Refine the following script to be concise, clear, and engaging for a 1-minute educational video. Ensure it is suitable for spoken narration and fits within 60 seconds when spoken at a natural pace. Split the script into 2-3 short paragraphs for caption display. Return the refined script as a list of paragraphs.

    Original script:
    {script}

    Output format:
    ["paragraph 1", "paragraph 2", "paragraph 3"]
    """
    response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    refined_script = eval(response.choices[0].message.content)  # Convert string to list
    return refined_script

# Function to generate audio for each paragraph using Google Cloud Text-to-Speech
def generate_audio(paragraphs, output_dir="audio"):
    client = texttospeech.TextToSpeechClient()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_files = []
    for i, paragraph in enumerate(paragraphs):
        synthesis_input = texttospeech.SynthesisInput(text=paragraph)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Wavenet-D"  # A natural-sounding English voice
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        audio_file = os.path.join(output_dir, f"paragraph_{i+1}.mp3")
        with open(audio_file, "wb") as out:
            out.write(response.audio_content)
        audio_files.append(audio_file)
    return audio_files

# Function to create video with captions and black background
def create_video(paragraphs, audio_files, output_file="educational_video.mp4"):
    clips = []
    for i, (paragraph, audio_file) in enumerate(zip(paragraphs, audio_files)):
        # Create text clip for captions
        text_clip = TextClip(
            paragraph,
            fontsize=40,
            color="white",
            font="Arial",
            size=(1280, 720),  # Standard HD resolution
            method="caption",
            align="center"
        )
        # Load audio and get its duration
        audio_clip = AudioFileClip(audio_file)
        duration = audio_clip.duration
        # Set text clip duration to match audio
        text_clip = text_clip.set_duration(duration)
        # Create black background clip
        bg_clip = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=duration)
        # Combine text and background
        video_clip = CompositeVideoClip([bg_clip, text_clip.set_position("center")])
        # Add audio to video clip
        video_clip = video_clip.set_audio(audio_clip)
        clips.append(video_clip)

    # Concatinate all clips
    final_clip = concatenate_videoclips(clips)
    # Write final video
    final_clip.write_videofile(output_file, fps=24, codec="libx264", audio_codec="aac")
    final_clip.close()
    for clip in clips:
        clip.close()

# Main function
def main():
    # Example input script (replace with your educational content)
    input_script = """
    Machine learning is a field of artificial intelligence that allows computers to learn from data without being explicitly programmed. It involves algorithms that identify patterns and make predictions. Applications include image recognition, natural language processing, and more. This technology is transforming industries like healthcare and finance.
    """

    # Step 1: Refine script with DeepSeek
    refined_paragraphs = refine_script_with_deepseek(input_script)
    print("Refined Script:", refined_paragraphs)

    # Step 2: Generate audio for each paragraph
    audio_files = generate_audio(refined_paragraphs)
    print("Audio files generated:", audio_files)

    # Step 3: Create video with captions and black background
    create_video(refined_paragraphs, audio_files)
    print("Video created: educational_video.mp4")

if __name__ == "__main__":
    main()

```

### How to Use

1. **Set Up Credentials**:
   - Replace `"path/to/your/google-credentials.json"` with the path to your Google Cloud service account JSON file.
   - Replace `"your_deepseek_api_key"` with your DeepSeek API key.
2. **Prepare Input Script**:
   - Modify the `input_script` variable in the `main()` function with your educational content. The script should be a single string with the full text you want to convert into a video.
3. **Run the Script**:
   - Save the script as `create_educational_video.py` and run it with `python create_educational_video.py`.
   - The script will:
     - Refine the script using DeepSeek API to ensure it’s concise and split into 2-3 paragraphs.
     - Generate MP3 audio files for each paragraph using Google Cloud Text-to-Speech.
     - Create a video with a black background, displaying each paragraph as captions synchronized with its corresponding audio.
4. **Output**:
   - The final video will be saved as `educational_video.mp4` in the same directory as the script.
   - Audio files for each paragraph will be saved in the `audio` directory.

### Notes

- **DeepSeek API**: The script uses the `deepseek-chat` model to refine the script. Ensure your API key is valid and you have sufficient credits. The DeepSeek API is used here to structure the script for video narration, as it excels in text generation and optimization.[](https://www.datacamp.com/tutorial/deepseek-api)
- **Google Cloud Text-to-Speech**: The script uses the `en-US-Wavenet-D` voice for natural-sounding English narration. You can change the voice by modifying the `name` parameter in `VoiceSelectionParams` (see Google Cloud Text-to-Speech documentation for other voice options).
- **MoviePy**: The video is created in 1280x720 resolution (HD). You can adjust the `size` parameter in `TextClip` and `ColorClip` for different resolutions.
- **Timing**: The script ensures captions are synchronized with audio by setting the text clip duration to match the audio duration. For a 1-minute video, the DeepSeek prompt enforces a concise script.
- **Dependencies**: Ensure FFmpeg is installed and accessible in your system’s PATH for `moviepy` to work correctly.

### Example Output

If your input script is about machine learning, the refined script might look like:

```
["Machine learning, a branch of AI, enables computers to learn from data.",
 "It uses algorithms to find patterns and predict outcomes.",
 "Applications include image recognition and healthcare innovations."]
```

- Each paragraph generates an audio file (e.g., `paragraph_1.mp3`, `paragraph_2.mp3`, etc.).
- The final video shows a black background with white captions appearing sequentially, synchronized with the audio narration.

This approach is simple, cost-effective, and produces professional-looking educational videos suitable for platforms like YouTube or educational websites. If you need further customization (e.g., different fonts, caption styles, or additional effects), let me know!
