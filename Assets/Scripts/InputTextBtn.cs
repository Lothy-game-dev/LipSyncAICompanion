using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InputTextBtn : MonoBehaviour
{
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
        InputTextObject.SetActive(true);
    }
}
