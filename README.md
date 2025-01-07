# Lyrics Sync (lsync) compatible with Windows OS

This project aims to build a lyrics-to-audio alignment system that can synchronize the audio of a polyphonic song with its lyrics and produce time-aligned lyrics with word-level onset and offset as a `.lrc` file. A deep-learning-based system is developed to approach the problem in three steps, which include separating the vocals, recognizing the singing vocals, and performing forced alignment. For singing vocals recognition, transfer learning is utilized to apply knowledge obtained from the speech domain to the singing domain.

### Flow

![](.github/fig.png)


### Installation
clone repo 
cd to repo
conda create -n lsync-windows python=3.9
conda activate lsync-windows 

pip install -r requirements.txt

### Usage

1. Place lyrics in lyrics/ directory
2. Place song files in songs/ directory (make sure they are the same filename as lyric files)
3. python batch_align_songs.py

#### Demo

Please refer to [demo.ipynb](./demo.ipynb).

If you want to visualize `.lrc` for evaluation, you can use [Lrc Player](https://github.com/mikezzb/lrc-player).

### Experiments

If you want to fine-tune a Wav2Vec2 model for better accuracy in singing domain, please refer to the experiments section below.

#### Fine-tune Wav2Vec2 model for lyrics transcription

1. Make a `dataset` folder in root folder
2. Download [DALI](https://github.com/gabolsgabs/DALI) dataset and put it it inside `dataset/DALI/v1`
   * Similarly, you can download jamendolyrics dataset for evaluation and put it in `dataset/jamendolyrics`
3. Download all DALI songs using `python get_dataset.py`
4. Run `dataset.ipynb` to prepare the DALI for fine-tune tasks
   * Procedures including vocal extraction, line-level segmentation, and making tokenizer
5. Run `train.ipynb` to fine-tune the `facebook/wav2vec2-base` for singing voice recognition
6. Run `run.ipynb` to see how to use the `lsync` library for lyrics-to-audio alignment based on the fine-tuned model
   * Remember to update model path to your model's path inside `lsync/phoneme_recognizer.py`

