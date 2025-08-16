using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class SubmitBtn : MonoBehaviour
{
    public TextMeshProUGUI Text;
    public LipSync LipSync;
    public GameObject InputTextObject;
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void OnMouseDown()
    {
        string text = Text.text;
        LipSync.TriggerVoice(text);
        InputTextObject.SetActive(false);
    }
}
