from dataclasses import dataclass
from typing import List, Optional
import unicodedata
from .util import read_text, convert_to_utf16le
from .lrc_formatter import Word
import os

SEPARATOR = '|'

@dataclass
class Segment:
    label: str
    start: int
    end: int

class LyricsProcessor:
    def __init__(self, lang: str = "en-US") -> None:
        """
        Initialize lyrics processor with specified language.
        
        Args:
            lang (str): Language code for processing (e.g., "en-US", "zh-CN")
        """
        self.lang = lang

    def process(self, text_path: str) -> Optional[str]:
        """
        Process lyrics text file with improved Unicode and error handling.
        
        Args:
            text_path: Path to the lyrics text file
            
        Returns:
            Optional[str]: Processed text or None if processing fails
        """
        try:
            # 1. Read text (detect encoding if necessary)
            text = read_text(text_path)
            if text is None:
                print(f"Error processing {text_path}: Could not read or decode text.")
                return None

            # Create UTF-16LE file in same directory as original
            dir_path = os.path.dirname(text_path)
            base_name = os.path.basename(text_path)
            utf16le_text_path = os.path.join(dir_path, f"{base_name}.utf16le")

            # 2. Convert to UTF-16LE
            if not convert_to_utf16le(text_path, utf16le_text_path):
                print(f"Error processing {text_path}: Could not convert to UTF-16LE")
                return None
            
            # 3. Read the UTF-16LE text
            text = read_text(utf16le_text_path, encoding="utf-16le")
            if text is None:
                print(f"Error processing {utf16le_text_path}: Could not read UTF-16LE text.")
                return None

            # 4. Process based on language
            if self.lang.startswith("en"):
                return self.__process_en(text, is_upper=not self.lang.endswith("-base"))
            elif self.lang == 'zh-CN':
                return self.__process_cn(text)
            else:
                print(f"Unsupported language: {self.lang}")
                return None

        except Exception as e:
            print(f"Error processing lyrics: {str(e)}")
            return None

    def __process_en(self, text: str, is_upper: bool = True) -> str:
        """
        Process English text with improved character handling.
        """
        try:
            # Normalize Unicode characters
            text = unicodedata.normalize('NFKC', text)

            # Apply case transformation if needed
            if is_upper:
                text = text.upper()
            else:
                text = text.lower()

            # Replace various Unicode characters with their ASCII equivalents
            replacements = {
                ''': "'",  # Right single quote
                ''': "'",  # Left single quote
                '"': '"',  # Right double quote
                '"': '"',  # Left double quote
                '–': '-',  # En dash
                '—': '-',  # Em dash
                '…': '...', # Ellipsis
                '\u2005': ' ',  # Four-per-em space
                '\u00A0': ' ',  # Non-breaking space
                '\u202F': ' ',  # Narrow no-break space
                '\u2028': '\n', # Line separator
                '\u2029': '\n', # Paragraph separator
            }
            
            for old, new in replacements.items():
                text = text.replace(old, new)

            # Replace spaces and newlines with separator
            text = text.replace(' ', SEPARATOR)
            text = text.replace('\n', SEPARATOR)
            text = text.replace('_', "'")  # Preserve apostrophes

            # Remove multiple consecutive separators
            while SEPARATOR + SEPARATOR in text:
                text = text.replace(SEPARATOR + SEPARATOR, SEPARATOR)

            return text.strip(SEPARATOR)

        except Exception as e:
            print(f"Error processing English text: {str(e)}")
            return None

    def __process_cn(self, text: str) -> str:
        """
        Process Chinese text with improved character handling.
        """
        try:
            # Normalize Unicode characters
            text = unicodedata.normalize('NFKC', text)
            
            # Remove whitespace and normalize newlines
            text = ''.join(text.split())
            
            return text

        except Exception as e:
            print(f"Error processing Chinese text: {str(e)}")
            return None

    def get_words_from_path(self, text: Optional[str], path: list, frame_duration: float) -> Optional[List[Word]]:
        """
        Extract words from alignment path with error handling.
        """
        try:
            if text is None or not path:
                return None

            # Skip repeating char
            i1, i2 = 0, 0
            segments = []
            
            while i1 < len(path):
                while i2 < len(path) and path[i1].token_index == path[i2].token_index:
                    i2 += 1
                segments.append(
                    Segment(
                        text[path[i1].token_index],
                        path[i1].time_index,
                        path[i2 - 1].time_index + 1
                    )
                )
                i1 = i2

            if self.lang.startswith("en"):
                return self.__merge_en(segments, frame_duration)
            elif self.lang == 'zh-CN':
                return [Word(s.label, s.start * frame_duration, s.end * frame_duration) 
                       for s in segments]
            else:
                print(f"Unsupported language for word extraction: {self.lang}")
                return None

        except Exception as e:
            print(f"Error extracting words from path: {str(e)}")
            return None

    def __merge_en(self, segments: List[Segment], frame_duration: float, separator: str = SEPARATOR) -> List[Word]:
        """
        Merge characters into words for English text.
        """
        try:
            words = []
            i1, i2 = 0, 0
            
            while i1 < len(segments):
                if i2 >= len(segments) or segments[i2].label == separator:
                    if i1 != i2:
                        segs = segments[i1:i2]
                        word = "".join([seg.label for seg in segs])
                        words.append(Word(
                            word,
                            segments[i1].start * frame_duration,
                            segments[i2 - 1].end * frame_duration
                        ))
                    i1 = i2 + 1
                    i2 = i1
                else:
                    i2 += 1
                    
            return words

        except Exception as e:
            print(f"Error merging English segments: {str(e)}")
            return None