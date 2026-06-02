---
audio: true
generated: false
image: false
lang: en
layout: post
title: Getting Started with Google Text-to-Speech API
type: post
---

I plan to convert some of Yin Wang's articles into audio using the Google Text-to-Speech API. Below is a step-by-step guide, along with some helpful tutorials provided by ChatGPT. Once everything is ready, I will upload the audio here for you to listen to.

---

### Step 1: Set Up Google Cloud Account

1. Create a Google Cloud Account
   If you don’t have one, sign up at the [Google Cloud Console](https://console.cloud.google.com/).

2. Create a New Project
   - In the Cloud Console, click on the project dropdown menu (top left).
   - Choose New Project, give it a name, and create the project.

3. Enable the Text-to-Speech API
   - Visit the [Google Cloud Text-to-Speech API page](https://cloud.google.com/text-to-speech).
   - Click Enable to activate the API for your project.

4. Create API Credentials
   - Navigate to APIs & Services > Credentials in the Cloud Console.
   - Click Create Credentials, then select Service Account.
   - Follow the prompts to create the service account and download the private key file in JSON format.
   - Keep this JSON file secure as it’s used to authenticate your API requests.

---

### Step 2: Install Google Cloud SDK and Client Library

1. Install Google Cloud SDK
   If you haven't yet, follow the instructions to install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) for your operating system.

2. Install the Python Client Library
   If you're using Python, install the `google-cloud-texttospeech` library with:

   ```bash
   pip install google-cloud-texttospeech
   ```

---

### Step 3: Set Up Authentication

Before using the API, you need to authenticate with your credentials. Set the environment variable to the path of your credentials file:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
```

Replace the path with the actual location of your downloaded JSON file.

---

### Step 4: Implement Text-to-Speech Conversion

Here’s a Python example to convert text into speech using the Google Cloud Text-to-Speech API:

```python
from google.cloud import texttospeech

def text_to_speech(text, output_filename):
    # Initialize the Text-to-Speech client
    client = texttospeech.TextToSpeechClient()

    # Set up the synthesis input
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Set voice parameters (using 'en-US-Journey-D')
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",  # English (United States)
        name="en-US-Journey-D"  # Specific voice model (Journey)
    )

    # Set audio configuration
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,  # MP3 format
        effects_profile_id=["small-bluetooth-speaker-class-device"],  # Optimized for Bluetooth speakers
        pitch=0.0,  # No pitch modification
        speaking_rate=0.9,  # Adjusted speech rate (can modify as needed)
        volume_gain_db=5.0  # Louder volume
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the audio content to a file
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)

    print(f"Audio content written to {output_filename}")

# Example usage
article_text = "Movies, oh my gosh, I just absolutely love them. They're like time machines taking you to different worlds and landscapes, and I just can't get enough of it."
output_file = "output_audio.mp3"  # Output in MP3 format

# Convert text to speech
text_to_speech(article_text, output_file)
```

---

### Step 5: Run the Script

1. Save the script as `text_to_speech.py`.
2. Run the script with:

   ```bash
   python text_to_speech.py
   ```

This will generate an audio file (`output_audio.mp3`) from the provided text.

---

### Step 6: Service Account Key

The JSON key for your service account should look similar to this:

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "your-private-key",
  "client_email": "your-service-account-email@your-project-id.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "your-client-cert-url"
}
```

---

### Why Choose Journey?

Google Cloud Text-to-Speech offers several voices, but Journey stands out for its natural, human-like sound. Unlike other models that often sound robotic, Journey excels in expressiveness and lifelike delivery. It is particularly suited for long-form content such as podcasts, audiobooks, or any application requiring a more conversational tone.

Key Features of Journey:

- Natural Speech: Sounds closer to a human voice.
- Expressiveness: Adjusts tone and inflection based on context.
- Ideal for Long-Form Content: Perfect for podcasts and narrations.

For more details on the benefits of Google Cloud Text-to-Speech, check out the [Google Cloud overview](https://cloud.google.com/text-to-speech#benefits).

---

### Step 7: Generate a New Service Account Key (if needed)

If your service account key doesn’t match the example above, you can generate a new one from the Google Cloud Console.

To generate a new key:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Navigate to IAM & Admin > Service Accounts.
3. Create a new service account:
   - Click Create Service Account and assign appropriate roles.
   - Click Create.
4. Generate a key:
   - After creating the service account, click it.
   - Go to the Keys tab, click Add Key, and choose JSON. Then download the key.

---

### Example Audio Output

Once everything is set up, you can generate an audio file, which will be available here:
[Download the audio file](assets/audios/output-audio.mp3).

---

### Conclusion

The Google Cloud Text-to-Speech API makes it easy to convert text into natural-sounding speech. Whether you're building an app that needs voice output or just experimenting with text-to-speech, this API offers powerful features and customization options. Explore the full documentation for additional voice selections, languages, and advanced features.
