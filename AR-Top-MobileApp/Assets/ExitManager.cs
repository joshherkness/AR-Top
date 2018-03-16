using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using Vuforia;
using UnityEngine.UI;

public class ExitManager : MonoBehaviour {

	private Connector connector;
	public RectTransform panel;

	public Button[] buttons;

	// Use this for initialization
	void Start () {
		connector = FindObjectOfType<Connector> ();
		panel.gameObject.SetActive (false);
	}
	
	// Update is called once per frame
	void Update () {
		
	}

	public void exit (){
		VuforiaBehaviour.Instance.enabled = false;
		Destroy (GameObject.FindGameObjectWithTag ("MainCamera"));
		SceneManager.LoadScene ("Login", LoadSceneMode.Additive);
		/*
		Destroy (GameObject.FindObjectOfType<RoomManager> ());
		Destroy (connector.gameObject);*/
	}

	public void openExitPanel (){
		panel.gameObject.SetActive (true);

		foreach (Button button in buttons) {
			button.gameObject.SetActive (false);
		}
	}

	public void closeExitPanel(){
		panel.gameObject.SetActive (false);

		foreach (Button button in buttons) {
			button.gameObject.SetActive (true);
		}
	}
}
