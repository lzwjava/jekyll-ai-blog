import os
from datetime import datetime
import pytz
from feedgen.feed import FeedGenerator

# Configuration
audio_dir = "assets/conversations/"
base_url = "https://lzwjava.github.io/"
feed_file = "feeds/conversation-feed.xml"

# Initialize RSS feed
fg = FeedGenerator()
fg.id(base_url + "conversation_feed")
fg.title("My Conversation Podcast")
fg.author({"name": "Lzwjava", "email": "lzwjava@example.com"})
fg.link(href=base_url, rel="alternate")
fg.description("A podcast with conversation audio files.")
fg.language("en")

# List all MP3 files in the audio directory
audio_files = [f for f in os.listdir(audio_dir) if f.endswith(".mp3")]

# Add episodes to feed
for audio_file in audio_files:
    audio_path = os.path.join(audio_dir, audio_file)

    # Extract date from filename if present, otherwise use file modification time
    try:
        date_str = audio_file[:10]  # Assuming YYYY-MM-DD format at the beginning
        pub_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        mod_time = os.path.getmtime(audio_path)
        pub_date = datetime.fromtimestamp(mod_time)
        print(f"No valid date in {audio_file}, using modification time: {pub_date}")

    # Make datetime timezone-aware
    pub_date = pub_date.replace(tzinfo=pytz.UTC)

    episode_title = os.path.splitext(audio_file)[0].replace("-", " ").title()
    audio_url = base_url + audio_dir + audio_file
    audio_size = os.path.getsize(audio_path)

    fe = fg.add_entry()
    fe.id(audio_url)
    fe.title(episode_title)
    fe.link(href=audio_url)
    fe.description(f"Conversation: {episode_title}")
    fe.enclosure(url=audio_url, length=str(audio_size), type="audio/mpeg")
    fe.published(pub_date)

# Generate RSS feed
fg.rss_file(feed_file, pretty=True)
print(f"RSS feed generated successfully at {feed_file}")
