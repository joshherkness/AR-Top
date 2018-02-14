using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using SocketIO;
using UnityEngine.SceneManagement;

public class Connector : MonoBehaviour {

	SocketIOComponent socket;
	RoomManager room;

	// Use this for initialization
	void Start () {
		DontDestroyOnLoad (this.gameObject);
		socket = GameObject.Find ("SocketIO").GetComponent <SocketIOComponent> ();
		room = FindObjectOfType<RoomManager> ();

		DontDestroyOnLoad (socket.gameObject);

		//socket.On("connect", connection);
		socket.On ("update", UpdateJSON);
		socket.On ("RoomNotFound", roomNotFound);
		socket.On ("RoomFound", roomFound);

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
		data ["first"] = "Ronald";
		data ["last"] = "Pimsley";
		socket.Emit ("update", new JSONObject (data));
		//socket.Emit ("RoomNotFound", new JSONObject (data));
	}

	public void connection(JSONObject js){
		socket.Emit ("FindRoom", js);
	}

	public void UpdateJSON(SocketIOEvent e){
		Debug.Log ("Update Called"); 
		Debug.Log(string.Format ("[name: {0}, data: {1}]", e.name, e.data));
	}

	public void roomNotFound(SocketIOEvent e){
		Debug.Log ("Signal of 'Room Not Found' received."); 
		room.roomNotFound ();
	}

	public void roomFound (SocketIOEvent e){
		SceneManager.LoadScene ("main");
	}
}
