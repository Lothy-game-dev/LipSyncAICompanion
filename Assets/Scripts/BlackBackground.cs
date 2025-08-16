using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BlackBackground : MonoBehaviour
{
    public GameObject InputTextObject;
    public GameObject Left;
    public GameObject Right;
    public GameObject Top;
    public GameObject Bottom;
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
        Vector3 mousePosition = Camera.main.ScreenToWorldPoint(Input.mousePosition);
        if (mousePosition.x > Left.transform.position.x && mousePosition.x < Right.transform.position.x && mousePosition.y > Bottom.transform.position.y && mousePosition.y < Top.transform.position.y)
        {
            return;
        }
        InputTextObject.SetActive(false);
    }
}
