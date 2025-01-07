ORIGINAL_SR = 44100
TARGET_SR = 16000
SEG_HOP_LENGTH = 1

MODELS = {
    'en-US': 'facebook/wav2vec2-large-960h-lv60-self',
    'en-US-base': 'facebook/wav2vec2-base',
    'en-finetuned-base': 'mikezzb/wav2vec2-base-singing',
    'zh-CN': 'jonatasgrosman/wav2vec2-large-xlsr-53-chinese-zh-cn'
}
