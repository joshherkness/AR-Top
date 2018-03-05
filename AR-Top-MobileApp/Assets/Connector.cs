using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using SocketIO;
using UnityEngine.SceneManagement;

public class Connector : MonoBehaviour {

	SocketIOComponent socket;
	RoomManager room;
	string socketurlbase;
	private bool mainSceneLoaded = false;

	// Use this for initialization
	void Start () {
		DontDestroyOnLoad (this.gameObject);
		socket = GameObject.Find ("SocketIO").GetComponent <SocketIOComponent> ();
		room = FindObjectOfType<RoomManager> ();
		if (room != null)
			print (room);
		socketurlbase = socket.url;

		DontDestroyOnLoad (socket.gameObject);

		socket.On("connect", connected);
		socket.On ("update", UpdateJSON);
		socket.On ("RoomNotFound", roomNotFound);
		socket.On ("RoomFound", roomFound);
		socket.On ("error", handleError);

		//StartCoroutine (BoopTime ());
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
		//socket.url = socketurlbase;
		//socket.url += "&room=" + js ["roomNumber"];
		//print (socket.url); 
		socket.Emit ("joinRoom", js["roomNumber"]);
	}

	public void connected(SocketIOEvent e){
		Debug.Log ("connected to Socket server");
		if (e != null)
			Debug.LogWarning ("Message from Socket server: " + e);
		else
			Debug.Log ("No issues from Socket Server");
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
		Debug.Log ("Connection received");
		if (!mainSceneLoaded) {
			SceneManager.sceneLoaded += OnSceneLoaded;
			SceneManager.LoadScene ("main", LoadSceneMode.Additive);
			mainSceneLoaded = true;
		}
	}

	public void handleError (SocketIOEvent e){
		if (room != null)
			room.serverErrorReceived (e.data.ToString ());
	}

	public void OnSceneLoaded(Scene scene, LoadSceneMode mode){
		MapController jsonReader = FindObjectOfType<MapController> ();
		print (jsonReader);
		SceneManager.SetActiveScene (SceneManager.GetSceneByName ("main"));
		SceneManager.UnloadSceneAsync ("Login");
	}
}
