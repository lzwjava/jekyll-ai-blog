import os
import requests
import datetime
import pytz
from supabase import create_client
import argparse
import subprocess
import shutil
from pathlib import Path

# Load environment variables
TELEGRAM_PUNCH_BOT_API_KEY = os.environ.get("TELEGRAM_PUNCH_BOT_API_KEY")
TELEGRAM_CHAT_ID = "610574272"  # Your chat ID


def send_telegram_message(bot_token, chat_id, message):
    """Sends a message to a Telegram chat using the Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    response = requests.post(url, params=params)
    if response.status_code != 200:
        print(
            f"Error sending Telegram message: {response.status_code} - {response.text}"
        )


def send_reminder(action):
    """Sends a punch reminder message."""
    # Updated message to specify punch_in or punch_out command
    command = action  # e.g., 'punch_in' or 'punch_out'
    message = f"⏰ *Reminder:* Please {action.replace('_', ' ')} by sending '{command}' to this bot."
    send_telegram_message(TELEGRAM_PUNCH_BOT_API_KEY, TELEGRAM_CHAT_ID, message)


def send_confirmation(action):
    """Sends a confirmation message for completed punch."""
    message = f"✅ You have already {action.replace('_', ' ')} today. No further reminders will be sent."
    send_telegram_message(TELEGRAM_PUNCH_BOT_API_KEY, TELEGRAM_CHAT_ID, message)


def parse_time(hour_str):
    """Parses HH string into datetime.time object with zero minutes."""
    try:
        hour = int(hour_str)
        if not 0 <= hour <= 23:
            raise ValueError
        return datetime.time(hour, 0)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Hour '{hour_str}' must be an integer between 00 and 23"
        )


# Telegram image handling functions
def handle_telegram_photo(update, supabase=None):
    """Handle photo messages from Telegram and save images."""
    message = update.get("message", {})
    photo = message.get("photo")
    document = message.get("document")

    dir_name = "telegram-bot"  # Default directory for telegram images
    source = "telegram"

    if photo:
        # Get the largest photo size
        file_id = photo[-1]["file_id"]
    elif document and document.get("mime_type", "").startswith("image/"):
        # Handle image documents
        file_id = document["file_id"]
    else:
        return None

    # Download the image
    temp_path = download_telegram_file(TELEGRAM_PUNCH_BOT_API_KEY, file_id)
    if not temp_path:
        return None

    try:
        # Use the image saving logic
        markdown_content, relative_path, target_path = process_and_save_image(
            str(temp_path), dir_name, source
        )

        # Send confirmation back to Telegram
        confirmation_msg = f"✅ Image saved successfully!\\n📁 {relative_path}\\n📋 Markdown copied to clipboard."
        send_telegram_message(
            TELEGRAM_PUNCH_BOT_API_KEY, TELEGRAM_CHAT_ID, confirmation_msg
        )

        return markdown_content

    finally:
        # Clean up temp file
        if temp_path.exists():
            temp_path.unlink()


def download_telegram_file(bot_token, file_id):
    """Download a file from Telegram and return the temp file path."""
    try:
        # Get file info
        get_file_url = f"https://api.telegram.org/bot{bot_token}/getFile"
        params = {"file_id": file_id}
        response = requests.get(get_file_url, params=params)
        if response.status_code != 200:
            print(f"Error getting file info: {response.status_code}")
            return None

        file_path = response.json()["result"]["file_path"]

        # Download the file
        download_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
        response = requests.get(download_url)
        if response.status_code != 200:
            print(f"Error downloading file: {response.status_code}")
            return None

        # Save to temp file
        temp_path = Path(f"/tmp/telegram_image_{file_id}.jpg")
        temp_path.write_bytes(response.content)
        return temp_path

    except Exception as e:
        print(f"Error downloading Telegram file: {e}")
        return None


def process_and_save_image(image_path, dir_name, source):
    """Process and save image using the logic from add_image_from_telegram.py"""
    # Validate source image
    source_path, image_ext = validate_source_image(image_path)

    # Set up target directory (adjust path for bot location)
    script_dir = Path(__file__).parent.parent  # Go up to scripts/
    assets_dir = script_dir.parent / "assets" / "images" / dir_name
    assets_dir.mkdir(parents=True, exist_ok=True)

    # Get next available number and create target filename
    next_number = get_next_number(assets_dir, dir_name, image_ext)
    target_filename = f"{dir_name}{next_number}.{image_ext}"
    target_path = assets_dir / target_filename

    # Copy the image file
    shutil.copy2(source_path, target_path)
    print(f"Image saved: {target_path}")

    # Generate markdown content
    relative_path = f"assets/images/{dir_name}/{target_filename}"
    source_mapping = get_source_mapping()
    full_source_name = source_mapping.get(source, source)
    markdown_content = generate_markdown_content_func(relative_path, full_source_name)

    # Copy to clipboard
    copy_to_clipboard_func(markdown_content)

    return markdown_content, relative_path, target_path


# Helper functions copied from add_image_from_telegram.py
def validate_source_image(image_path):
    """Validate that the source image exists and is a valid file."""
    source_path = Path(image_path)

    if not source_path.exists():
        raise FileNotFoundError(f"Source image '{image_path}' does not exist.")

    if not source_path.is_file():
        raise ValueError(f"'{image_path}' is not a file.")

    # Get image extension
    image_ext = source_path.suffix.lstrip(".")
    if not image_ext:
        raise ValueError("Source file has no extension.")

    return source_path, image_ext


def get_next_number(target_dir, dir_name, image_ext):
    """Get the next available number for the image filename."""
    if not target_dir.exists():
        return 1

    existing_files = list(target_dir.glob(f"{dir_name}*.{image_ext}"))
    if not existing_files:
        return 1

    # Extract numbers from existing files
    numbers = []
    for file in existing_files:
        stem = file.stem
        if stem.startswith(dir_name):
            try:
                # Extract number after dir_name
                number_part = stem[len(dir_name) :]
                if number_part.isdigit():
                    numbers.append(int(number_part))
                elif number_part == "":
                    numbers.append(1)  # Handle case where file is just dir_name
            except ValueError:
                continue

    return max(numbers) + 1 if numbers else 1


def get_source_mapping():
    """Get the mapping from simplified names to full names."""
    return {
        "self-screenshot": "Self-screenshot",
        "self-captured": "Self-captured",
        "walmart": "walmart.com",
        "pinduoduo": "pinduoduo.com",
        "amazon": "amazon.com",
        "chatgpt": "chatgpt.com",
        "telegram": "Telegram Bot",
    }


def generate_markdown_content_func(relative_path, source):
    """Generate the formatted markdown content."""
    return f"""{{: .centered }}
![]({relative_path}){{: .responsive }}
*Source: {source}*{{: .caption }}"""


def copy_to_clipboard_func(text):
    """Copy text to clipboard using pbcopy (macOS)."""
    try:
        subprocess.run(["pbcopy"], input=text.encode(), check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def main():
    parser = argparse.ArgumentParser(description="Telegram Punch Reminder Bot")
    parser.add_argument(
        "--job",
        choices=["punch_reminder", "send_message"],
        required=True,
        help="Job to perform",
    )
    parser.add_argument(
        "--message", type=str, help="Message to send for 'send_message' job"
    )
    parser.add_argument(
        "--punch_in_start",
        type=parse_time,
        default="12",
        help="Punch in start hour (HH, default 12)",
    )
    parser.add_argument(
        "--punch_in_end",
        type=parse_time,
        default="15",
        help="Punch in end hour (HH, default 15)",
    )
    parser.add_argument(
        "--punch_out_start",
        type=parse_time,
        default="18",
        help="Punch out start hour (HH, default 18)",
    )
    parser.add_argument(
        "--punch_out_end",
        type=parse_time,
        default="21",
        help="Punch out end hour (HH, default 21)",
    )
    args = parser.parse_args()

    if args.job == "send_message":
        if TELEGRAM_PUNCH_BOT_API_KEY and TELEGRAM_CHAT_ID:
            message = (
                args.message if args.message else "Default test message from your bot!"
            )
            send_telegram_message(TELEGRAM_PUNCH_BOT_API_KEY, TELEGRAM_CHAT_ID, message)
            print(f"Message sent: {message}")
        else:
            print("TELEGRAM_PUNCH_BOT_API_KEY and TELEGRAM_CHAT_ID are not set.")
        return

    elif args.job == "punch_reminder":
        # Initialize Supabase
        supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

        # Get current time in SGT (UTC+8)
        sgt = pytz.timezone("Asia/Singapore")
        now_utc = datetime.datetime.utcnow()
        now_sgt = now_utc.replace(tzinfo=pytz.utc).astimezone(sgt)
        today_sgt = now_sgt.date()

        # Define time windows from arguments
        punch_in_start = args.punch_in_start
        punch_in_end = args.punch_in_end
        punch_out_start = args.punch_out_start
        punch_out_end = args.punch_out_end

        current_time = now_sgt.time()

        # Determine current window
        if punch_in_start <= current_time <= punch_in_end:
            window = "punch_in"
        elif punch_out_start <= current_time <= punch_out_end:
            window = "punch_out"
        else:
            window = None

        if not window:
            print("Outside punch reminder windows.")
            return

        # Fetch today's punch record
        response = (
            supabase.table("punch_records")
            .select("*")
            .eq("date", str(today_sgt))
            .execute()
        )
        punch_record = response.data[0] if response.data else None

        # Check if punch is already done
        if window == "punch_in" and punch_record and punch_record["punch_in_time"]:
            print("Already punched in today.")
            send_confirmation("punch_in")
            return
        if window == "punch_out" and punch_record and punch_record["punch_out_time"]:
            print("Already punched out today.")
            send_confirmation("punch_out")
            return

        # Fetch last processed Telegram update ID
        state_response = (
            supabase.table("telegram_state")
            .select("last_update_id")
            .eq("id", 1)
            .execute()
        )
        last_update_id = (
            state_response.data[0]["last_update_id"] if state_response.data else 0
        )

        # Get new Telegram updates
        url = f"https://api.telegram.org/bot{TELEGRAM_PUNCH_BOT_API_KEY}/getUpdates"
        params = {"offset": last_update_id + 1, "timeout": 0}
        response = requests.get(url, params=params)
        updates = response.json().get("result", [])

        max_update_id = last_update_id
        for update in updates:
            if update["update_id"] > max_update_id:
                max_update_id = update["update_id"]
            if (
                "message" in update
                and str(update["message"]["chat"]["id"]) == TELEGRAM_CHAT_ID
            ):
                message_text = update["message"].get("text", "").lower()
                # Check for specific commands based on the current window
                if window == "punch_in" and message_text == "punch_in":
                    if not punch_record:
                        supabase.table("punch_records").insert(
                            {
                                "date": str(today_sgt),
                                "punch_in_time": now_utc.isoformat(),
                            }
                        ).execute()
                    else:
                        supabase.table("punch_records").update(
                            {"punch_in_time": now_utc.isoformat()}
                        ).eq("date", str(today_sgt)).execute()
                elif window == "punch_out" and message_text == "punch_out":
                    if not punch_record:
                        supabase.table("punch_records").insert(
                            {
                                "date": str(today_sgt),
                                "punch_out_time": now_utc.isoformat(),
                            }
                        ).execute()
                    else:
                        supabase.table("punch_records").update(
                            {"punch_out_time": now_utc.isoformat()}
                        ).eq("date", str(today_sgt)).execute()

                # Handle photo/document messages regardless of punch window
                handle_telegram_photo(update, supabase)

        # Update last_update_id
        if max_update_id > last_update_id:
            supabase.table("telegram_state").update(
                {"last_update_id": max_update_id}
            ).eq("id", 1).execute()

        # Refetch punch record to check latest state
        response = (
            supabase.table("punch_records")
            .select("*")
            .eq("date", str(today_sgt))
            .execute()
        )
        punch_record = response.data[0] if response.data else None

        # Send reminder if punch not recorded
        if window == "punch_in" and (
            not punch_record or not punch_record["punch_in_time"]
        ):
            send_reminder("punch_in")
        elif window == "punch_out" and (
            not punch_record or not punch_record["punch_out_time"]
        ):
            send_reminder("punch_out")


if __name__ == "__main__":
    main()
