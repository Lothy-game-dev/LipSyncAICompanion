# LipSyncAICompanion

LipSyncAICompanion is an AI-powered text-to-speech (TTS) and lip sync system designed for integration with applications that require realistic voice synthesis and viseme (lip movement) data. It consists of a Python backend (REST API) and a Unity frontend for real-time lip sync animation.

## Frontend (Unity)

### Overview

The Unity frontend provides real-time lip sync animation and character voice playback by communicating with the Python backend API. It is implemented as a Unity project with C# scripts, using Unity's UI and audio systems.

### Features

- **Real-Time Lip Sync**: Animates character mouth shapes (visemes) in sync with generated speech audio.
- **Multiple Characters**: Switch between different TTS voices and character avatars (Windows, eSpeak, SpeechT5).
- **Text Input**: Enter text in Unity to generate speech and lip sync.
- **Backend Integration**: Connects to the Python REST API for TTS and viseme data.

### How It Works

1. **User Input**: Enter text in the Unity UI or trigger speech via script.
2. **API Request**: The `LipSync` C# script sends the text to the backend API.
3. **Receive Data**: The backend responds with viseme data, character mapping, and a generated audio file.
4. **Audio Playback**: Unity downloads and plays the audio file.
5. **Lip Sync Animation**: The script animates the character's mouth using viseme sprites in sync with the audio.

### Key Scripts

- `LipSync.cs`: Handles API communication, audio playback, and viseme animation.
- `VisemeResponse`: Data structure for parsing backend responses.

### Setup Instructions

1. **Clone the Repository**: Add the `Assets/Scripts/` folder to your Unity project.
2. **Assign References**: In the Unity Editor, assign the required SpriteRenderer, AudioSource, and character GameObjects to the `LipSync` script component.
3. **Import Viseme Sprites**: Add your viseme mouth shape sprites to the project and assign them in the inspector.
4. **Configure Backend URL**: Ensure the backend API is running and accessible at the URL specified in `LipSync.cs`.
5. **Run the Scene**: Enter play mode, input text, and see the character speak with synchronized lip movements.

### Requirements

- Unity 2021.3 or newer (recommended)
- TextMeshPro package (for text display)
- Internet access to communicate with the backend API

### Example Usage

1. Select a character (Windows, eSpeak, or SpeechT5) in the UI.
2. Enter text and trigger speech.
3. The character will speak the text with accurate lip sync.

For more details, see the comments in `Assets/Scripts/LipSync.cs`.

## Backend (Python REST API)

### Features

- **Multiple TTS Engines**: Supports Windows default TTS, eSpeak, and Microsoft SpeechT5.
- **Language Detection**: Automatically detects the language of the input text.
- **Phoneme-to-Viseme Mapping**: Converts phonemes to viseme indices for lip sync animation.
- **REST API**: FastAPI-based backend for easy integration.
- **Background Processing**: Uses process pools for efficient TTS generation.

### Requirements

- Python 3.8+
- [FastAPI](https://fastapi.tiangolo.com/)
- [Transformers](https://huggingface.co/docs/transformers/index)
- [Torch](https://pytorch.org/)
- [Torchaudio](https://pytorch.org/audio/stable/index.html)
- [langdetect](https://pypi.org/project/langdetect/)
- [soundfile](https://pypi.org/project/SoundFile/)
- [Datasets](https://huggingface.co/docs/datasets/index)
- Windows (for Windows TTS support)

### Installation

Install dependencies:
```
pip install -r requirements.txt
```

### How to Run This Project

1. **Start the Backend API**  
   In your terminal, navigate to the backend directory (where `api.py` is located) and run:
   ```
   python api.py
   ```
   Wait until the API has finished launching and is ready to accept requests.

2. **Run the Unity Project**  
   - Open the Unity project in the Unity Editor.
   - Press the **Play** button to enter Play mode.
   - Interact with the UI: select a character, enter text, and trigger speech.

The Unity project will communicate with the backend API to generate speech and viseme data for lip sync animation.
