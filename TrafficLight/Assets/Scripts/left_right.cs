using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class left_right : MonoBehaviour
{
    [SerializeField] bool MovementMove;
    [SerializeField] float Speed;
    [SerializeField] bool Straigth;
    bool turn;
    public int check;
    // Start is called before the first frame update
    void Start()
    {
        Destroy(gameObject, 110);
        System.Random rnd = new System.Random();
        MovementMove = true;
        turn = false;
        check = 1;
        if(rnd.NextDouble() >= 0.5)
        {
            Straigth = true;
        }
        else
        {
            Straigth = false;
        }
    }
    // Update is called once per frame
    void Update()
    {
        if(MovementMove && !(turn))
        {
            transform.Translate(Vector2.up * Speed * Time.deltaTime);
        }
        else if(MovementMove && turn)
        {
            if(Straigth)
            {
                transform.Translate(Vector2.up * Speed * Time.deltaTime);
            }
            else
            {
                transform.Translate(Vector2.left * Speed * Time.deltaTime);
            }
        }
    }
    private void OnTriggerEnter2D(Collider2D collision)
    {
        if(collision.tag == "Stop" || collision.tag == "Car")
        {
            MovementMove = false;
        }

        if(collision.tag == "Turn")
        {
            if(check == 0)
            {
                turn = true;
            }
            else
            {
                check = check -1;
            }
        }
        if(collision.tag == "KILL")
        {
            Destroy(gameObject);
        }
    }
    private void OnTriggerExit2D(Collider2D other)
    {
        if (other.tag == "Stop" || other.tag == "Car")
        {
            MovementMove = true;
        }
    }
}
