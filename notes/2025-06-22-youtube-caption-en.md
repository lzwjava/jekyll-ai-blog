---
audio: false
generated: true
lang: en
layout: post
title: YouTube Video Caption Extraction Methods
translated: false
type: note
---

To get all captions of a YouTube video, follow these steps, depending on your needs and whether you want a manual or automated approach. Note that captions must be available for the video (either auto-generated or uploaded by the creator).

### Manual Method (Using YouTube's Built-in Transcript Feature)
1. **Open the Video**: Go to YouTube in a web browser and navigate to the desired video.
2. **Check for Captions**: Click the video to pause it. Look for a "CC" (Closed Captions) icon near the bottom-right corner of the player. If visible, captions are available.
3. **Access the Transcript**:
   - Scroll down to the video description and click "Show more."
   - Find and click "Show transcript" (if available). This opens a transcript panel on the right side of the video with timestamps and text.
4. **Toggle Timestamps**: Click the three vertical dots at the top-right of the transcript panel and select "Toggle timestamps" to show or hide timestamps, depending on your preference.
5. **Copy the Transcript**:
   - Scroll to the bottom of the transcript, click and hold after the last word, then drag to the top to highlight all text.
   - Press `Ctrl + C` (Windows) or `Command + C` (Mac) to copy.
6. **Paste and Save**: Open a text editor (e.g., Notepad, TextEdit, or Word), paste the text with `Ctrl + V` or `Command + V`, and save as a `.txt` file or your preferred format.

**Note**: This method only works on the YouTube website, not the mobile app.[](https://www.wikihow.com/Download-YouTube-Video-Subtitles)

### For Content Creators (Downloading Captions from Your Own Video)
If you own the video, you can download captions directly from YouTube Studio:
1. **Log in to YouTube Studio**: Go to [studio.youtube.com](https://studio.youtube.com).
2. **Select Video**: Click "Content" in the left menu, then choose the video.
3. **Access Subtitles**: Click "Subtitles" in the left menu, then select the language.
4. **Download Captions**: Click the three-dot menu next to the subtitle track and select "Download." Choose a format like `.srt`, `.vtt`, or `.sbv`.
5. **Edit or Use**: Open the downloaded file in a text editor or subtitle editor (e.g., Aegisub) for further use.

**Note**: You can only download caption files for videos on channels you manage.[](https://ito-engineering.screenstepslive.com/s/ito_fase/a/1639680-how-do-i-download-a-caption-file-from-youtube)

### Automated Method (Using Third-Party Tools)
If you need captions in a specific format (e.g., `.srt`) or for videos you don’t own, use a reputable third-party tool:
1. **Choose a Tool**: Popular options include:
   - **DownSub**: A free online tool for downloading subtitles.
   - **Notta**: Offers transcription and subtitle downloads with high accuracy.[](https://www.notta.ai/en/blog/download-subtitles-from-youtube)
   - **4K Download**: A desktop app for subtitle extraction.[](https://verbit.ai/captioning/a-guide-to-downloading-subtitles-and-captions-from-youtube-enhancing-accessibility-and-user-experience/)
2. **Copy Video URL**: Open the YouTube video, click "Share" below the video, and copy the URL.
3. **Use the Tool**:
   - Paste the URL into the tool’s input field.
   - Select the desired language and format (e.g., `.srt`, `.txt`).
   - Click "Download" or "Extract" and save the file.
4. **Verify**: Open the file to ensure accuracy, as auto-generated captions may contain errors.

**Caution**: Use trusted tools to avoid security risks. Some tools may have ads or require payment for advanced features.[](https://gotranscript.com/blog/how-to-download-subtitles-from-youtube)

### Using the YouTube API (For Developers)
For bulk caption extraction or app integration, use the YouTube Data API:
1. **Set Up API Access**: Create a project in the [Google Cloud Console](https://console.cloud.google.com), enable the YouTube Data API v3, and obtain an API key.
2. **List Caption Tracks**: Use the `captions.list` endpoint to retrieve available caption tracks for a video. Example:
   ```
   GET https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId=VIDEO_ID&key=API_KEY
   ```
3. **Download Captions**: Use the `captions.download` endpoint to fetch a specific caption track. Example:
   ```
   GET https://www.googleapis.com/youtube/v3/captions/CAPTION_ID?tfmt=srt&key=API_KEY
   ```
4. **Limitations**:
   - You can only download captions for your own videos unless the video owner has made them publicly accessible.
   - API usage has quota limits (approximately 200 units per caption download).[](https://developers.google.com/youtube/v3/docs/captions)[](https://stackoverflow.com/questions/73863672/how-can-i-get-captions-of-a-youtube-video-and-display-it-separately)
5. **Alternative**: Some developers scrape the timed text URL (e.g., `https://www.youtube.com/api/timedtext?...`) from the video page source, but this is unreliable, may violate YouTube’s terms, and risks IP blocking.[](https://stackoverflow.com/questions/73863672/how-can-i-get-captions-of-a-youtube-video-and-display-it-separately)

### Additional Tips
- **Language Selection**: If captions are available in multiple languages, select your preferred language from the "Subtitles/CC" settings or the transcript’s dropdown menu.[](https://riverside.fm/blog/youtube-transcription)
- **Auto-Generated Captions**: These may have errors due to accents, background noise, or complex audio. Review and edit if accuracy is critical.[](https://support.google.com/youtube/answer/6373554?hl=en)
- **Accessibility**: Captions enhance accessibility for deaf or hard-of-hearing viewers and improve SEO by making content searchable.[](https://www.descript.com/blog/article/transcript-of-youtube-videos)
- **No Captions Available?**: If the video lacks captions, consider using transcription services like Rev or Notta to generate a transcript from the audio.[](https://www.rev.com/resources/how-to-download-youtube-subtitles-as-text-files)[](https://www.notta.ai/en/blog/download-subtitles-from-youtube)

### Limitations
- Not all videos have captions, especially if the creator disabled them or YouTube’s auto-captioning isn’t supported for the language or audio quality.[](https://support.google.com/youtube/answer/6373554?hl=en)
- The YouTube mobile app doesn’t support transcript viewing, but you can enable captions via the "CC" button.[](https://riverside.fm/blog/youtube-transcription)
- Some third-party tools or API methods may not work for auto-generated captions or restricted videos.[](https://stackoverflow.com/questions/9611397/how-to-extract-closed-caption-transcript-from-youtube-video)

If you need captions for a specific video or in a particular format, let me know, and I can guide you further!
