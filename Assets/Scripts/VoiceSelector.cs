using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class VoiceSelector : MonoBehaviour
{
    public string VoiceName;
    public GameObject SelectedObject;
    public List<GameObject> OtherSelectors;
    public VoiceSelectSection VoiceSelectSection;
    /// <summary>
    /// Start is called on the frame when a script is enabled just before
    /// any of the Update methods is called the first time.
    /// </summary>

    public void Unselect()
    {
        SelectedObject.SetActive(false);
    }

    public void Select()
    {
        SelectedObject.SetActive(true);
    }

    private void OnMouseDown()
    {
        StartCoroutine(SelectVoice());
        Select();
        foreach (GameObject otherSelector in OtherSelectors)
        {
            otherSelector.GetComponent<VoiceSelector>().Unselect();
        }
        VoiceSelectSection.SelectVoice(VoiceName);
    }

    IEnumerator SelectVoice()
    {
        string url = "https://c6d7b0744907.ngrok-free.app/select_voice?voice=" + VoiceName;
        UnityWebRequest request = UnityWebRequest.Get(url);
        yield return request.SendWebRequest();
        if (request.result != UnityWebRequest.Result.Success)
        {
            Debug.LogError(request.error);
        }
    }
}
