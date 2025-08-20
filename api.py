from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
import soundfile as sf
import os
import uvicorn
from datetime import datetime
import subprocess
from langdetect import detect, detect_langs
import random
from enum import Enum
from windows_tts import windows_default_tts
from espeak_tts import espeak_tts
from speecht5_tts import speecht5_tts
from concurrent.futures import ProcessPoolExecutor
import concurrent.futures

from fastapi.responses import FileResponse

executor = ProcessPoolExecutor()

# --- Init ---
app = FastAPI(docs_url="/docs", redoc_url=None)
os.makedirs("Assets\\StreamingAssets\\static", exist_ok=True)

class Voice(Enum):
    WINDOWS_DEFAULT = "windows_default"
    ESPEAK = "espeak"
    SPEECHT5 = "speecht5"

current_chosen_voice = Voice.ESPEAK
processes = {}

# Example mapping from phonemes (strip stress numbers) to visemes
ipa_to_viseme = {
    # 1: A, E, I
    "ɑ": 1, "æ": 1, "a": 1, "aɪ": 1, "ɛ": 1, "ɪ": 1, "eɪ": 1,

    # 2: U
    "u": 2, "ʊ": 2, "ʌ": 2, "oʊ": 2,

    # 3: O
    "ɔ": 3, "o": 3, "oʊ": 3,

    # 4: R
    "r": 4, "ɝ": 4, "ɚ": 4,

    # 5: L
    "l": 5,

    # 6: CH, SH, J
    "ʧ": 6, "ʃ": 6, "ʤ": 6,

    # 7: Q, W
    "w": 7,  # Q mapped to W sound

    # 8: B, M, P
    "b": 8, "m": 8, "p": 8,

    # 9: EE
    "i": 9, "iː": 9, "ɪi": 9,

    # 10: F, V
    "f": 10, "v": 10,

    # 11: C, D, G, K, N, S, T, X, Y, Z
    "k": 11, "g": 11, "ŋ": 11, "s": 11, "z": 11, "t": 11,
    "d": 11, "j": 11, "h": 11, "ʒ": 11,

    # 12: TH
    "θ": 12, "ð": 12,
}


def phonemes_to_visemes(phoneme_list):
    visemes = []
    for ph in phoneme_list:
        ph = ph.strip("012")
        viseme_id = ipa_to_viseme.get(ph, 8)
        visemes.append(viseme_id)
    return visemes


def text_to_visemes_func(text, lang):
    phonemes = []
    char_mapping = []
    all_chars = []

    def get_pronunciation(word):
        espeak_voices = subprocess.run(
            r'"espeak-ng" --ipa -q --pho "' + word + '"',
            capture_output=True,
            text=True,
            shell=True,
            encoding="utf-8"
        )
        pronunciations = [c for c in espeak_voices.stdout if c != " " and c != "\n"]
        return word, pronunciations

    words = text.split()
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_word = {executor.submit(get_pronunciation, word): word for word in words}
        for future in concurrent.futures.as_completed(future_to_word):
            word, pronunciations = future.result()
            results.append((word, pronunciations))

    # Preserve original word order
    word_to_pronunciations = {word: pronunciations for word, pronunciations in results}
    for word in words:
        pronunciations = word_to_pronunciations[word]
        print("pronunciations: ", pronunciations)
        if pronunciations:
            phoneme_list = [p.rstrip('012') for p in pronunciations]
            letters = list(word)
            char_index = 0

            for i, ph in enumerate(phoneme_list):
                # Assign at least one letter to each phoneme
                if char_index < len(letters):
                    # If last phoneme, take all remaining letters
                    if i == len(phoneme_list) - 1:
                        chars_for_ph = ''.join(letters[char_index:])
                        char_index = len(letters)
                    else:
                        chars_for_ph = letters[char_index]
                        char_index += 1
                else:
                    chars_for_ph = ""  # no characters left

                phonemes.append(ph)
                char_mapping.append(chars_for_ph)
                all_chars.extend(list(chars_for_ph))
        else:
            phonemes.append("8")
            char_mapping.append(word)
            all_chars.extend(list(word))

    visemes = phonemes_to_visemes(phonemes)
    return phonemes, visemes, char_mapping, all_chars
    
@app.get("/list_voices")
def list_voices():
    return {"voices": [v.value for v in Voice], "current_chosen_voice": current_chosen_voice.value}

@app.get("/select_voice")
def select_voice(voice: str):
    if voice in [v.value for v in Voice]:
        global current_chosen_voice
        current_chosen_voice = Voice(voice)
    else:
        return {"message": "Voice not found"}
    return {"message": "Voice selected successfully", "current_chosen_voice": current_chosen_voice.value}

@app.get("/stop-task/{task_name}")
def stop_task(task_name: str):
    p = processes.get(task_name)
    if not p:
        return {"status": f"Task {task_name} not found."}
    
    processes[task_name].cancel()
    return {"status": f"Task {task_name} was already finished."}

@app.get("/text_to_speech")
def text_to_speech(text: str, input_file_name: str):
    lang = detect(text)
    text = text.replace("\n", ". ").replace(r"\s+", " ")
    print("Language: ", lang)
    static_dir = os.path.join("Assets", "StreamingAssets", "static")
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    save_path = os.path.join(static_dir, f"{input_file_name}")
    print("Current chosen voice: ", current_chosen_voice)
    if current_chosen_voice == Voice.WINDOWS_DEFAULT:
        future = executor.submit(windows_default_tts, text, lang, save_path)
    elif current_chosen_voice == Voice.SPEECHT5:
        future = executor.submit(speecht5_tts, text, lang, save_path)
    else:
        future = executor.submit(espeak_tts, text, lang, save_path)
    
    future.result()
    # Return the file as a downloadable attachment
    return FileResponse(
        save_path,
        filename=input_file_name,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{input_file_name}"'}
    )


@app.get("/text_to_visemes")
def text_to_visemes(text: str, input_file_name:str):
    lang = detect(text)
    phonemes, visemes, char_mapping, all_chars = text_to_visemes_func(text, lang)
    return {
        "phonemes": phonemes,
        "visemes": visemes,
        "char_mapping": char_mapping,
        "all_chars": all_chars,
    }

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000)
