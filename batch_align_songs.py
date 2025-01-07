import os
import re
from lsync import LyricsSync

SONGS_DIR = "songs"
LYRICS_DIR = "lyrics"
OUTPUT_DIR = "output"
YOUR_MODEL_ID = "en-finetuned-base"
YOUR_MODEL_BLANK_ID = 29


os.makedirs(OUTPUT_DIR, exist_ok=True)

lsync = LyricsSync(lang=YOUR_MODEL_ID, blank_id=YOUR_MODEL_BLANK_ID)

def clean_lrc_content(lrc_content):

    lines = lrc_content.splitlines()
    cleaned_lines = []
    for line in lines:
        # Remove the first timestamp [mm:ss.xx] and capture the rest
        match = re.match(r"^\[\d{2}:\d{2}\.\d{2}\](.*)$", line)
        if match:
            line = match.group(1)  # Keep the rest of the line

            # Remove spaces before "<"
            line = re.sub(r" <", "<", line)

            # Find the first timestamp in <> and convert it to []
            line = re.sub(r"^<(\d{2}:\d{2}\.\d{2})>", r"[\1]", line)

            # Remove trailing underscores if they exist
            line = line.rstrip("_")

            # Remove trailing spaces
            line = line.rstrip()

            cleaned_lines.append(line)
        else:
            # Remove trailing spaces for lines without timestamps as well
            cleaned_lines.append(line.rstrip() + "\n")

    return "\n".join(cleaned_lines)


def get_lrc_filename(audio_filename):
    base_name = os.path.splitext(audio_filename)[0]
    return os.path.join(OUTPUT_DIR, base_name + ".lrc")


def get_lyrics_filename(audio_filename):
    base_name = os.path.splitext(audio_filename)[0]
    return os.path.join(LYRICS_DIR, base_name + ".txt")


for filename in os.listdir(SONGS_DIR):
    if filename.endswith((".mp3", ".wav", ".flac")):
        audio_path = os.path.join(SONGS_DIR, filename)
        lyrics_path = get_lyrics_filename(filename)
        lrc_path = get_lrc_filename(filename)

# Check if the corresponding lyrics file exists
    if os.path.exists(lyrics_path):
        try:
            print(f"Processing: {filename}")
            words, lrc = lsync.sync(audio_path, lyrics_path)

            # Clean the generated LRC content
            cleaned_lrc = clean_lrc_content(lrc)

            # Save the cleaned LRC content to a file with UTF-16 encoding
            with open(lrc_path, "w", encoding="utf-16") as f:
                f.write(cleaned_lrc)

            print(f"LRC file saved to: {lrc_path}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")
    else:
        print(f"Lyrics file not found for {filename}. Skipping.")