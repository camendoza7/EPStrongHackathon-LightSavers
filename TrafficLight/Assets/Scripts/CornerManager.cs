using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CornerManager : MonoBehaviour
{
    [SerializeField] GameObject Stop1;
    [SerializeField] GameObject Stop2;
    [SerializeField] GameObject Stop3;
    [SerializeField] GameObject Stop4;

    public void TurnOnStop(string number)
    {
        Debug.Log(number);
        if(number.Equals("False"))
        {
            Stop1.GetComponent<BoxCollider2D>().enabled = false;
            Stop1.GetComponent<SpriteRenderer>().color = Color.green;
            Stop2.GetComponent<BoxCollider2D>().enabled = false;
            Stop2.GetComponent<SpriteRenderer>().color = Color.green;
            Stop3.GetComponent<BoxCollider2D>().enabled = true;
            Stop3.GetComponent<SpriteRenderer>().color = Color.red;
            Stop4.GetComponent<BoxCollider2D>().enabled = true;
            Stop4.GetComponent<SpriteRenderer>().color = Color.red;

        }
        else if(number.Equals("True"))
        {
            Stop1.GetComponent<BoxCollider2D>().enabled = true;
            Stop1.GetComponent<SpriteRenderer>().color = Color.red;
            Stop2.GetComponent<BoxCollider2D>().enabled = true;
            Stop2.GetComponent<SpriteRenderer>().color = Color.red;
            Stop3.GetComponent<BoxCollider2D>().enabled = false;
            Stop3.GetComponent<SpriteRenderer>().color = Color.green;
            Stop4.GetComponent<BoxCollider2D>().enabled = false;
            Stop4.GetComponent<SpriteRenderer>().color = Color.green;

        }
    }
}
