using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using TMPro;
using System.IO;

public class LipSync : MonoBehaviour
{
    private List<int> Visemes;
    public List<Sprite> VisemeSprites;
    public SpriteRenderer VisemeImage;
    public TextMeshPro TextMesh;
    public AudioSource AudioSource;
    public GameObject WindowsCharacter;
    public GameObject EspeakCharacter;
    public GameObject Speecht5Character;

    private float DelayTimer;
    private int CurrentVisemeIndex;
    private List<string> CharMapping;
    private List<string> AllChars;
    private string FinalText;
    // Start is called before the first frame update
    void Start()
    {
        Visemes = new List<int>();
        CurrentVisemeIndex = 0;
    }

    // Update is called once per frame
    void Update()
    {
    }

    public void TriggerVoice(string text) 
    {
        StopAllCoroutines();
        StartCoroutine(GetVisemes(text));
    }

    public IEnumerator GetVisemes(string text)
    {
        string fileName = "speech_" + System.DateTime.Now.ToString("yyyyMMddHHmmss") + ".wav";
        string url = "http://localhost:8000/text_to_visemes?text=" + UnityWebRequest.EscapeURL(text) + "&input_file_name=" + fileName;

        // 1. Call API
        UnityWebRequest request = UnityWebRequest.Get(url);
        yield return request.SendWebRequest();
        if (request.result != UnityWebRequest.Result.Success)
        {
            Debug.LogError(request.error);
            yield break;
        }

        var wrapper = JsonUtility.FromJson<VisemeResponse>(request.downloadHandler.text);
        Visemes = wrapper.visemes;
        CharMapping = wrapper.char_mapping;
        
        CurrentVisemeIndex = 0;
        FinalText = "";

        // 2. Wait until audio file is written
        string filePath = Path.Combine(Application.streamingAssetsPath, "static/" + fileName).Replace("\\", "/");
        Debug.Log(filePath);
        while (!File.Exists(filePath))
        {
            yield return null; // wait one frame
        }

        // 3. Load audio from file (not Resources.Load!)
        string fileUri = new System.Uri(filePath).AbsoluteUri;
        float audioLength = 0;
        Debug.Log(fileUri);
        using (UnityWebRequest www = UnityWebRequestMultimedia.GetAudioClip(fileUri, AudioType.WAV))
        {
            yield return www.SendWebRequest();
            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError(www.error);
                yield break;
            }

            AudioClip clip = DownloadHandlerAudioClip.GetContent(www);
            string url2 = "http://localhost:8000/stop-task/" + wrapper.task_name;

            // 1. Call API
            UnityWebRequest request2 = UnityWebRequest.Get(url2);
            yield return request2.SendWebRequest();
            if (request2.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError(request2.error);
                yield break;
            }
            AudioSource.clip = clip;
            audioLength = clip.length;
            AudioSource.Play();
        }

        // 4. Drive viseme timeline
        string fullText = text;
        float delay = audioLength / Visemes.Count;
        while (CurrentVisemeIndex < Visemes.Count)
        {
            VisemeImage.sprite = VisemeSprites[Visemes[CurrentVisemeIndex] - 1];

            FinalText += CharMapping[CurrentVisemeIndex];
            int index = fullText.IndexOf(CharMapping[CurrentVisemeIndex]);
            if (index >= 0) fullText = fullText.Remove(index, CharMapping[CurrentVisemeIndex].Length);

            if (fullText.Length > 0 && fullText[0] == ' ')
            {
                fullText = fullText.Substring(1);
                FinalText += " ";
            }

            TextMesh.text = FinalText;
            CurrentVisemeIndex++;
            
            if (CurrentVisemeIndex >= Visemes.Count)
            {
                VisemeImage.sprite = VisemeSprites[7]; // rest mouth
            }
            yield return new WaitForSeconds(delay);
        }
    }

    public void SelectCharacter(string character)
    {
        WindowsCharacter.SetActive(false);
        EspeakCharacter.SetActive(false);
        Speecht5Character.SetActive(false);
        if (character == "espeak")
        {
            EspeakCharacter.SetActive(true);
            TriggerVoice("Hello I am your AI companion. My name is ESpeak!");
        }
        else if (character == "speecht5")
        {
            Speecht5Character.SetActive(true);
            TriggerVoice("Hello I am your AI companion. My name is SpeechT5!");
        }
        else
        {
            WindowsCharacter.SetActive(true);
            TriggerVoice("Hello I am your AI companion. My name is Windows!");
        }
    }


    [System.Serializable]
    public class VisemeResponse
    {
        public List<int> phonemes;
        public List<int> visemes;
        public List<string> char_mapping;
        public List<string> all_chars;
        public string audio_file;
        public string task_name;
    }
}

