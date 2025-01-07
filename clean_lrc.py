import os
import re
import argparse

def clean_lrc_files(folder_path):
    """
    Cleans LRC files in a folder:
        - Removes the first timestamp.
        - Converts the second timestamp from <> to [].
        - Removes extra spaces before "<".
        - Removes trailing underscores.

    Args:
        folder_path: The path to the folder containing LRC files.
    """
    if not os.path.isdir(folder_path):
        print(f"Error: Invalid folder path: {folder_path}")
        return

    for filename in os.listdir(folder_path):
        if filename.endswith(".lrc"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r") as f:
                lines = f.readlines()

            cleaned_lines = []
            for line in lines:
                # Remove the first timestamp [mm:ss.xx]
                line = re.sub(r"^\[\d{2}:\d{2}\.\d{2}\] ", "", line)

                # Convert the second timestamp from <> to []
                line = re.sub(r"<(\d{2}:\d{2}\.\d{2})>", r"[\1]", line)

                # Remove spaces before "<"
                line = re.sub(r" <", "<", line)

                # Remove trailing underscores if they exist
                line = line.rstrip("_\n") + "\n"

                cleaned_lines.append(line)

            with open(filepath, "w") as f:
                f.writelines(cleaned_lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean LRC files in a specified folder.")
    parser.add_argument("folder_path", help="The path to the folder containing LRC files.")
    args = parser.parse_args()

    clean_lrc_files(args.folder_path)