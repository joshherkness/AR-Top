using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class RoomManager : MonoBehaviour {

	public RectTransform panel; //The panel that contains the input field for the room code
	public InputField roomcode; //The input field for the room code
	public Button submitButton; //The button to submit the room code to the socket

	private string code;
	private const int ROOMCODELENGTH = 5; //The alphanumeric length of the room code

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		
	}

	public void SubmitRoomCode(){
		code = null;
		if (roomcode.text.Length == ROOMCODELENGTH) {
			code = roomcode.text;
			panel.gameObject.SetActive (false);
		}
	}

	public string GetRoomCode(){
		return code;
	}
}
