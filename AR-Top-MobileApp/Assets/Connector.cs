using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using SocketIO;

public class Connector : MonoBehaviour {

	SocketIOComponent socket;
	RoomManager room;

	// Use this for initialization
	void Start () {
		socket = GameObject.Find ("SocketIO").GetComponent <SocketIOComponent> ();
		room = FindObjectOfType<RoomManager> ();

		//socket.On("connect", connection);
		socket.On ("update", TestBoop);
		//socket.Emit ("RoomNotFound");
		socket.On ("RoomNotFound", roomNotFound);

		StartCoroutine (BoopTime ());
	}

	// Update is called once per frame
	void Update () {
		
	}

	private IEnumerator BoopTime(){
		yield return new WaitForSeconds (1);

		Dictionary<string, string> data = new Dictionary<string, string>();
		data["email"] = "some@email.com";
		data["pass"] = "1234";
		socket.Emit ("update", new JSONObject (data));
		//socket.Emit ("RoomNotFound", new JSONObject (data));
	}

	public void connection(SocketIOEvent e){
		socket.Emit ("RoomNotFound", new JSONObject (e.data));
	}

	public void TestBoop(SocketIOEvent e){
		Debug.Log ("Update Called"); 
		Debug.Log(string.Format ("[name: {0}, data: {1}]", e.name, e.data));
	}

	public void roomNotFound(SocketIOEvent e){
		Debug.Log ("Signal of 'Room Not Found' received."); 
		room.roomNotFound ();
	}
}
