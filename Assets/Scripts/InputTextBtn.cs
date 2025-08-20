using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class InputTextBtn : MonoBehaviour
{
    public GameObject InputTextObject;
    public TextMeshProUGUI TextMesh;
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
        TextMesh.enableWordWrapping = true;
        InputTextObject.SetActive(true);
    }
}
