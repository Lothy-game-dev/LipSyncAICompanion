class VoiceType:
    id: str
    lang: str
    gender: str

    def __init__(self, id, lang, gender):
        self.id = id
        self.lang = lang
        self.gender = gender