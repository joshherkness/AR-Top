using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using SocketIO;

public class Connector : MonoBehaviour {

	SocketIOComponent socket;

	// Use this for initialization
	void Start () {
		socket = GameObject.Find ("SocketIO").GetComponent <SocketIOComponent> ();
		//socket.On("connect", connection);
		socket.On ("update", TestBoop);

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
	}

	public void connection(SocketIOEvent e){
		socket.Emit ("connect", new JSONObject (e.data));
	}

	public void TestBoop(SocketIOEvent e){
		Debug.Log(string.Format ("[name: {0}, data: {1}]", e.name, e.data));
	}
}
