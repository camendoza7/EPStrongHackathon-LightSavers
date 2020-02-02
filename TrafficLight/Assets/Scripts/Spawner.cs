using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Spawner : MonoBehaviour
{
    [SerializeField] bool NewVersion;
    [SerializeField] GameObject Car1;
    [SerializeField] GameObject Car2;
    [SerializeField] GameObject Car3;
    [SerializeField] GameObject Car4;
    [SerializeField] GameObject Spawner1;
    [SerializeField] GameObject Spawner2;
    [SerializeField] GameObject Spawner3;
    [SerializeField] GameObject Spawner4;
    [SerializeField] CornerManager cornerManager;
    [System.NonSerializedAttribute] System.IO.StreamReader file;
    [System.NonSerializedAttribute] string line;
    Queue queue;
    [SerializeField] float timer;
    int[] rows;

    private void Start()
    {
        rows = new int[4];
        if(NewVersion)
        {
            file = new System.IO.StreamReader("Assets/MLsim.txt");
        }
        else
        {
            file = new System.IO.StreamReader("Assets/timersim.txt");
        }
        
        line = file.ReadLine();
        Debug.Log("Firstline " + line);
        string[] words = line.Split(' ');
        Debug.Log(words.ToString());
        for (int i = 0, j = 0; j < rows.Length; i = i+2, j++)
        {
            Debug.Log("i " + i );
            rows[j] = int.Parse(words[i]);
            Debug.Log("J " + j + "|" + rows[j]);
            
        }
        ReadLine(words);
        StartCoroutine("NextLine");

    }
    public void ReadLine(string[] words)
    {
        cornerManager.TurnOnStop(words[words.Length - 2]);
        for (int i = 0, j = 0; j < rows.Length; i = i + 2, j++)
        {
            Debug.Log(rows[j] + "|" + int.Parse(words[i]));
            if (rows[j] < int.Parse(words[i]))
            {
                rows[j] = int.Parse(words[i]);
                Spawn(j);
            }
            else
            {
                rows[j] = int.Parse(words[i]);
            }
        }
    }
    public void Spawn(int i)
    {
        float ran = Random.Range(0, 3);
        GameObject Car;
        if (ran == 0)
        {
             Car = Car1; 
        }
        else if(ran == 1)
        {
             Car = Car2;
        }
        else if (ran == 2)
        {
             Car = Car3;
        }
        else
        {
             Car = Car4;
        }

        if (i == 0)
        {
            GameObject newCar = Instantiate(Car, Spawner1.transform.position, Spawner1.transform.rotation);
        }
        else if(i == 1)
        {
            GameObject newCar = Instantiate(Car, Spawner2.transform.position, Spawner2.transform.rotation);
        }
        else if (i == 2)
        {
            GameObject newCar = Instantiate(Car, Spawner3.transform.position, Spawner3.transform.rotation);
        }
        else if (i == 3)
        {
            GameObject newCar = Instantiate(Car, Spawner4.transform.position, Spawner4.transform.rotation);
        }
    }
    IEnumerator NextLine()
    {
        Debug.Log("Called");
        yield return new WaitForSeconds(timer);
        Debug.Log("Timer Over");
        while ((line = file.ReadLine()) != null)
        {
            string[] words = line.Split(' ');
            ReadLine(words);
            Debug.Log(line);
            yield return new WaitForSeconds(timer);
            
            
        }
       
       
    }

}
