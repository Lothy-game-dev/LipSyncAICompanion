import pyttsx3
import random
from voice_type import VoiceType

engine = pyttsx3.init()
list_all_voices_windows_default = []
list_female_voices_windows_default = []
for idx, voice in enumerate(engine.getProperty('voices')):
    list_all_voices_windows_default.append(VoiceType(id=voice.id, lang="".join(voice.languages), gender=getattr(voice, 'gender', 'Unknown')))
    if getattr(voice, 'gender', 'Unknown') == 'Female':
        list_female_voices_windows_default.append(VoiceType(id=voice.id, lang="".join(voice.languages), gender=getattr(voice, 'gender', 'Unknown')))

def windows_default_tts(text, lang, filename):
    list_suitable_voices = []
    list_suitable_voices_female = []
    for idx, voice in enumerate(list_all_voices_windows_default):
        if lang in voice.lang:
            if voice.gender == 'F':
                list_suitable_voices_female.append(voice.id)
            list_suitable_voices.append(voice)
    if len(list_suitable_voices_female) == 0:
        if len(list_suitable_voices) == 0:
            engine.setProperty('voice', list_all_voices_windows_default[random.randint(0, len(list_all_voices_windows_default) - 1)].id)
        else:
            engine.setProperty('voice', list_suitable_voices[random.randint(0, len(list_suitable_voices) - 1)].id)
    else:
        engine.setProperty('voice', list_suitable_voices_female[random.randint(0, len(list_suitable_voices_female) - 1)].id)
    engine.save_to_file(text, filename)
    engine.runAndWait()