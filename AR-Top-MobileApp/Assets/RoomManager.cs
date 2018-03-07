using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class RoomManager : MonoBehaviour {

	public RectTransform panel; //The panel that contains the input field for the room code
	public InputField roomcode; //The input field for the room code
	public Button submitButton; //The button to submit the room code to the socket
	public TextMeshProUGUI errorLabel; //The label to print out user error
	public TextMeshProUGUI serverErrorLabel; //The label to display a server error e.g. "Room code doesn't exist!"

	private Connector con;

	private string code;
	private const int ROOMCODELENGTH = 5; //The alphanumeric length of the room code

	// Use this for initialization
	void Start () {
		con = FindObjectOfType<Connector> ();
		roomcode.contentType = InputField.ContentType.Alphanumeric;
		roomcode.characterLimit = 5;
	}
	
	// Update is called once per frame
	void Update () {
		if (roomcode.text.Length == ROOMCODELENGTH) {
			submitButton.interactable = true;
		} else {
			submitButton.interactable = false;
		}

	}

	public void SubmitRoomCode(){
		code = null;
		errorLabel.text = "";
		if (roomcode.text.Length == ROOMCODELENGTH) {
			code = roomcode.text;
			Dictionary<string, string> r = new Dictionary<string, string> ();
			r ["roomNumber"] = code;
			con.connection (new JSONObject (r));
			//panel.gameObject.SetActive (false);
		} else {
			errorLabel.text = "Room code must be " + ROOMCODELENGTH + " characters long.";
		}
	}

	public string GetRoomCode(){
		return code;
	}

	public void roomNotFound(){
		serverErrorLabel.text = "Error\nRoom not found with given code.";
	}

	public void serverErrorReceived(string message){
		serverErrorLabel.text = message;
	}
}
