import chardet
import librosa
import soundfile as sf
from .config import ORIGINAL_SR, TARGET_SR
from lsync.lrc_formatter import Word
from typing import List
import dataclasses
import pandas as pd
import numpy as np
import os 

# Audio processing constants
window_size = int(TARGET_SR * 15)
hop_length = window_size

def get_audio_segments(audio):
    """Split audio to segments.
    
    Args:
        audio (np.ndarray): Input audio signal
        
    Returns:
        np.ndarray: Framed audio segments
    """
    return librosa.util.frame(audio, frame_length=window_size, hop_length=hop_length, axis=0)

def get_audio_segments_by_onsets(audio):
    """Split audio into segments based on onset detection.
    
    Args:
        audio (np.ndarray): Input audio signal
        
    Returns:
        list: List of audio segments
    """
    onset_times = librosa.onset.onset_detect(
        y=audio, sr=TARGET_SR, backtrack=True)
    onset_boundaries = np.concatenate([onset_times, [len(audio)]])
    segments = []
    start_onset = 0
    for onset in onset_boundaries:
        segments.append(audio[start_onset:onset])
        start_onset = onset
    return segments

def ensure_directory_exists(path):
    """Ensure the directory exists, create if it doesn't."""
    os.makedirs(os.path.dirname(path), exist_ok=True)

def read_text(text_path, encoding=None):
    """Reads text from a file, with improved Unicode handling."""
    if encoding is None:
        with open(text_path, 'rb') as f:
            detected = chardet.detect(f.read())
            encoding = detected['encoding'] or 'utf-8'  # Fallback to utf-8 if detection fails

    try:
        with open(text_path, 'r', encoding=encoding, errors='replace') as file:
            data = file.read()
        return data
    except UnicodeDecodeError:
        # Try with utf-8 if the detected encoding fails
        try:
            with open(text_path, 'r', encoding='utf-8', errors='replace') as file:
                data = file.read()
            return data
        except Exception as e:
            print(f"Error: Failed to read file with both detected and UTF-8 encoding: {str(e)}")
            return None
    except FileNotFoundError:
        print(f"Error: File not found at {text_path}")
        return None

def save_lrc(lrc: str, name: str, output_dir='output/lrc'):
    """Save LRC file with proper Unicode handling."""
    try:
        # Ensure the output directory exists
        ensure_directory_exists(f'{output_dir}/{name}.lrc')
        
        # Save with UTF-8 encoding
        with open(f'{output_dir}/{name}.lrc', 'w', encoding='utf-8') as fp:
            fp.write(lrc)
    except Exception as e:
        print(f"Error saving LRC file: {str(e)}")

def save_words(words: List[Word], name: str, output_dir='output/words'):
    """Save words data with proper Unicode handling."""
    try:
        # Ensure the output directory exists
        ensure_directory_exists(f'{output_dir}/{name}.csv')
        
        df = pd.DataFrame([dataclasses.asdict(w) for w in words])
        df.to_csv(f"{output_dir}/{name}.csv", index=False, encoding='utf-8')
    except Exception as e:
        print(f"Error saving words file: {str(e)}")

def save_audio(audio, name, sr=ORIGINAL_SR, out_path="output/vocals"):
    """Save audio file with proper path handling."""
    try:
        # Ensure the output directory exists
        ensure_directory_exists(f'{out_path}/{name}.wav')
        
        sf.write(f'{out_path}/{name}.wav', audio, sr)
    except Exception as e:
        print(f"Error saving audio file: {str(e)}")

def convert_to_utf16le(input_path, output_path, original_encoding=None):
    """Converts a text file to UTF-16LE encoding with improved error handling."""
    try:
        if original_encoding is None:
            with open(input_path, 'rb') as f:
                detected = chardet.detect(f.read())
                original_encoding = detected['encoding'] or 'utf-8'

        # First read with original encoding
        with open(input_path, 'r', encoding=original_encoding, errors='replace') as infile:
            text = infile.read()

        # Ensure the output directory exists
        ensure_directory_exists(output_path)
        
        # Write with UTF-16LE encoding
        with open(output_path, 'w', encoding='utf-16le') as outfile:
            outfile.write(text)
        print(f"File converted to UTF-16LE: {output_path}")
        return True
    except Exception as e:
        print(f"Error converting file to UTF-16LE: {str(e)}")
        return False