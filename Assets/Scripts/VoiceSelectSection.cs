using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System;

public class VoiceSelectSection : MonoBehaviour
{
    public List<VoiceSelector> VoiceSelectors;
    public LipSync LipSync;
    void Start()
    {
        StartCoroutine(InitVoice());
    }

    public void SelectVoice(string voice)
    {
        foreach (VoiceSelector voiceSelector in VoiceSelectors)
        {
            if (voiceSelector.VoiceName == voice)
            {
                voiceSelector.Select();
            } else {
                voiceSelector.Unselect();
            }
        }
        LipSync.SelectCharacter(voice.ToLower());
    }

    IEnumerator InitVoice()
    {
        string url = "https://c6d7b0744907.ngrok-free.app/list_voices";
        UnityWebRequest request = UnityWebRequest.Get(url);
        yield return request.SendWebRequest();
        if (request.result != UnityWebRequest.Result.Success)
        {
            Debug.LogError(request.error);
        }
        var wrapper = JsonUtility.FromJson<VoiceResponse>(request.downloadHandler.text);
        string current_chosen_voice = wrapper.current_chosen_voice;
        SelectVoice(current_chosen_voice);
    }

    [System.Serializable]
    public class VoiceResponse
    {
        public List<string> voices;
        public string current_chosen_voice;
    }
}