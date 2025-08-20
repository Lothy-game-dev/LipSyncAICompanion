import subprocess
import random
import os
from voice_type import VoiceType

# Get list of voices
result = subprocess.run(
    r'"espeak-ng" --voices',
    capture_output=True,
    text=True,
    shell=True,
    encoding="utf-8"
)
list_female_voices_espeak = []
list_all_voices_espeak = []
for line in result.stdout.splitlines():
    parts = line.split()
    if len(parts) >= 4:
        if "F" in parts[2]:  # Gender column
            list_female_voices_espeak.append(VoiceType(id=parts[3], lang=parts[1], gender="F"))
        list_all_voices_espeak.append(VoiceType(id=parts[3], lang=parts[1], gender=""))
        

def espeak_tts(text, lang, filename, rate=150):
    """
    Generate speech with eSpeak NG and save to WAV file.
    
    :param text: The text to speak
    :param filename: Output WAV file path
    :param voice: Voice language code (e.g., 'en', 'en-us', 'ja')
    :param rate: Speaking speed (default 150 wpm)
    """
    list_suitable_voices_female = []
    for idx, voice in enumerate(list_female_voices_espeak):
        if lang in voice.lang:
            list_suitable_voices_female.append(voice)
    if len(list_suitable_voices_female) == 0:
        list_suitable_voices = []
        for idx, voice in enumerate(list_all_voices_espeak):
            if lang in voice.lang:
                list_suitable_voices.append(voice)
        if len(list_suitable_voices) == 0:
            voice = list_all_voices_espeak[random.randint(0, len(list_all_voices_espeak) - 1)]
        else:
            voice = list_suitable_voices[0]
    else:
        voice = list_suitable_voices_female[random.randint(0, len(list_suitable_voices_female) - 1)]
    # Build espeak-ng command
    command = (
        fr'"espeak-ng" '
        f'-v {voice.lang}+f{random.randint(1, 5)} '
        f'-s {rate} '
        f'-w "{filename}" '
        f'"{text}"'
    )
    subprocess.run(command, check=True, shell=True)
    
    if os.path.exists(filename):
        print(f"WAV file created: {filename}")
    else:
        print("Failed to generate speech.")