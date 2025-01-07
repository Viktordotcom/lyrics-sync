from dataclasses import dataclass
from typing import List, Optional
import unicodedata

def seconds_to_lrc(seconds: float, is_word: bool = True) -> str:
    """
    Convert seconds to LRC timestamp format.
    
    Args:
        seconds (float): Time in seconds
        is_word (bool): If True, uses <> brackets, otherwise uses [] brackets
        
    Returns:
        str: Formatted timestamp
    """
    try:
        minutes = int(seconds // 60)
        seconds = seconds % 60
        hundredths = int((seconds % 1) * 100)
        seconds = int(seconds)
        formatted = f"{minutes:02d}:{seconds:02d}.{hundredths:02d}"
        return f"<{formatted}>" if is_word else f"[{formatted}]"
    except Exception as e:
        print(f"Error formatting time {seconds}: {str(e)}")
        return "<00:00.00>" if is_word else "[00:00.00]"

@dataclass
class Word:
    label: str
    start: float
    end: float

    def __repr__(self) -> str:
        """
        Format word with timestamps.
        Now includes Unicode normalization and error handling.
        """
        try:
            # Normalize Unicode characters
            normalized_label = unicodedata.normalize('NFKC', self.label)
            return f"{seconds_to_lrc(self.start)} {normalized_label} {seconds_to_lrc(self.end)}"
        except Exception as e:
            print(f"Error formatting word {self.label}: {str(e)}")
            return f"{seconds_to_lrc(self.start)} ERROR {seconds_to_lrc(self.end)}"

class LrcFormatter:
    @staticmethod
    def words2lrc(words: List[Word], original_lyrics: str, lang: str = "en-US") -> Optional[str]:
        """
        Convert word timings to LRC format.
        
        Args:
            words: List of Word objects with timing information
            original_lyrics: Original lyrics text
            lang: Language code for processing
            
        Returns:
            str: Formatted LRC content, or None if processing fails
        """
        try:
            if not words or not original_lyrics:
                print("Error: Empty words list or lyrics")
                return None

            lrc = ""
            counter = 0
            
            # Normalize Unicode in original lyrics
            original_lyrics = unicodedata.normalize('NFKC', original_lyrics)
            lines = original_lyrics.splitlines()

            for line_index, line in enumerate(lines):
                if not line.strip():
                    continue

                # Check if we have enough words left
                if counter >= len(words):
                    print(f"Warning: Not enough word timings for line {line_index + 1}")
                    break

                # Get line start time
                line_start_word = words[counter]
                line_start_time = seconds_to_lrc(line_start_word.start, False)
                lrc += line_start_time

                # Split line into words based on language
                if lang.startswith("en"):
                    splitted_words = [w for w in line.split(' ') if w.strip()]
                elif lang == "zh-CN":
                    splitted_words = list(line)  # Split into characters for Chinese
                else:
                    # Default to space-based splitting for unknown languages
                    splitted_words = [w for w in line.split(' ') if w.strip()]

                for original_word in splitted_words:
                    if not original_word.strip():
                        continue
                        
                    if counter >= len(words):
                        print(f"Warning: Not enough word timings for word '{original_word}'")
                        break

                    word = words[counter]
                    # Update label with original text while preserving timing
                    word.label = original_word
                    lrc += f" {word}"
                    counter += 1

                # Add newline if it's not the last line
                if line_index < len(lines) - 1:
                    lrc += "\n"

            return lrc

        except Exception as e:
            print(f"Error generating LRC format: {str(e)}")
            return None