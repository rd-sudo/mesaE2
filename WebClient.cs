using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class WebClient : MonoBehaviour
{

    public float timeToUpdate;
    public float dt;

    IEnumerator UpdateStep()
    {
        WWWForm form = new WWWForm();
        string url = "http://127.0.0.1:3000/";
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");
            yield return www.SendWebRequest();
            if (www.result == UnityWebRequest.Result.ConnectionError)
            {
                Debug.Log(www.error);
            }
            else
            {
                string txt = www.downloadHandler.text;
                Debug.Log(txt);
            }
        }
    }

    IEnumerator GetCars()
    {
        WWWForm form = new WWWForm();
        string url = "http://127.0.0.1:3000/cars";
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");
            yield return www.SendWebRequest();
            if (www.result == UnityWebRequest.Result.ConnectionError)
            {
                Debug.Log(www.error);
            }
            else
            {
                string txt = www.downloadHandler.text;
                Debug.Log(txt);
            }
        }
    }


    IEnumerator GetTrafficLights()
    {
        WWWForm form = new WWWForm();
        string url = "http://127.0.0.1:3000/trafficLights";
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");
            yield return www.SendWebRequest();
            if (www.result == UnityWebRequest.Result.ConnectionError)
            {
                Debug.Log(www.error);
            }
            else
            {
                string txt = www.downloadHandler.text;
                Debug.Log(txt);
            }
        }
    }

    IEnumerator CallFunctionsSequentially()
    {
        yield return StartCoroutine(UpdateStep());
        yield return StartCoroutine(GetCars());
        yield return StartCoroutine(GetTrafficLights());

        Debug.Log("Funciones ejecutadas después de 480 frames.");
    }

    void Start()
    {

    }


    private int frameCounter = 0;

    void Update()
    {
        frameCounter++;

        if (frameCounter >= 480)
        {
            StartCoroutine(CallFunctionsSequentially());
            frameCounter = 0; 
        }
    }



}
