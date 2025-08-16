from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan, set_seed
from datasets import load_dataset
import torch
import torchaudio
from voice_type import VoiceType

dataset = load_dataset(
    "hf-internal-testing/librispeech_asr_demo", "clean", split="validation"
)  # doctest: +IGNORE_RESULT
dataset = dataset.sort("id")
sampling_rate = dataset.features["audio"].sampling_rate

processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

# audio file is decoded on the fly
inputs = processor(text="prelaunch", return_tensors="pt")
speaker_embeddings = torch.zeros((1, 512))  # or load xvectors from a file

set_seed(555)  # make deterministic

# generate speech and save to WAV
with torch.no_grad():
    speech = model.generate(inputs["input_ids"], speaker_embeddings=speaker_embeddings, vocoder=vocoder)
    # speech shape: (batch, samples) or (samples,) if batch size is 1
    speech_np = speech.cpu().numpy()
    # Ensure speech_np is 2D: (channels, samples)
    if speech_np.ndim == 1:
        speech_np = speech_np[None, :]  # Add batch/channel dimension
    torchaudio.save("test.wav", torch.from_numpy(speech_np), 16000)
    print("Saved speech to test.wav")
    
def speecht5_tts(text, lang, filename):
    inputs = processor(text=text, return_tensors="pt")
    # generate speech and save to WAV
    with torch.no_grad():
        speech = model.generate(inputs["input_ids"], speaker_embeddings=speaker_embeddings, vocoder=vocoder)
        # speech shape: (batch, samples) or (samples,) if batch size is 1
        speech_np = speech.cpu().numpy()
        # Ensure speech_np is 2D: (channels, samples)
        if speech_np.ndim == 1:
            speech_np = speech_np[None, :]  # Add batch/channel dimension
        torchaudio.save(filename, torch.from_numpy(speech_np), 16000)