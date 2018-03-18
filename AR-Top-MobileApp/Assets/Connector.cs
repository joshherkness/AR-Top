using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using SocketIO;
using UnityEngine.SceneManagement;
using Vuforia;

public class Connector : MonoBehaviour {

	SocketIOComponent socket;
	RoomManager room;
	string socketurlbase;
	private bool mainSceneLoaded = false;
	private MapGameObject mapGameObject;

	JSONObject roomCode;

	// Use this for initialization
	void Start () {
		DontDestroyOnLoad (this.gameObject);
		//DontDestroyOnLoad (GameObject.FindGameObjectWithTag ("MainCamera"));
		mapGameObject = FindObjectOfType<MapGameObject> ();

		VuforiaBehaviour.Instance.enabled = false;
		socket = GameObject.Find ("SocketIO").GetComponent <SocketIOComponent> ();
		room = FindObjectOfType<RoomManager> ();
		if (room != null)
			print (room);
		socketurlbase = socket.url;

		DontDestroyOnLoad (socket.gameObject);

		socket.On("connect", connected);
		socket.On ("update", UpdateJSON);
		socket.On ("roomNotFound", roomNotFound);
		socket.On ("roomFound", roomFound);
		socket.On ("error", handleError);
		socket.On ("disconnect", handleDisconnect);
	}

	// Update is called once per frame
	void Update () {
		
	}

	public void connection(JSONObject js){
		roomCode = js;
		socket.Emit ("joinRoom", js);
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
		string models = e.data.ToString ();
		print (models);
		mapGameObject.setMap (models);
	}

	public void roomNotFound(SocketIOEvent e){
		Debug.Log ("Signal of 'Room Not Found' received."); 
		room.roomNotFound ();
	}

	public void roomFound (SocketIOEvent e){
		Debug.Log ("Connection received");
		string models = e.data.ToString ();
		print (models); 
		mapGameObject.setMap (models);
		if (!mainSceneLoaded) {
			
			SceneManager.sceneLoaded += OnSceneLoaded;
			SceneManager.LoadScene ("main", LoadSceneMode.Additive);
			mainSceneLoaded = true;
			Debug.Log ("Connection received");
			models = e.data.ToString ();
			print (models); 
			mapGameObject.setMap (models);

		}
	}

	public void handleError (SocketIOEvent e){
		Debug.LogError ("error event received from socket server" + e.data.ToString ());
		if (room != null) {
			print (room); 
			room.serverErrorReceived (e);
		}
	}

	public void handleDisconnect (SocketIOEvent e){
		Debug.Log ("Disconnected");
		if (mainSceneLoaded) {
			SceneManager.LoadScene ("Login", LoadSceneMode.Additive);
			LeaveRoomSession ();
			mainSceneLoaded = false;
			room.serverErrorReceived (e);
		}
	}

	public void OnSceneLoaded(Scene scene, LoadSceneMode mode){
		mapGameObject.findMapController ();
		if (scene.name == "main") {
			SceneManager.SetActiveScene (SceneManager.GetSceneByName ("main"));
			SceneManager.UnloadSceneAsync ("Login");
			VuforiaBehaviour.Instance.enabled = true;
		} else {
			VuforiaBehaviour.Instance.enabled = false;
			SceneManager.SetActiveScene (SceneManager.GetSceneByName ("Login"));
			SceneManager.UnloadSceneAsync ("main");
			//mainSceneLoaded = false;
			//Destroy (GameObject.FindObjectOfType<RoomManager> ());
			Destroy (this.gameObject);
		}

	}

	public void LeaveRoomSession(){
		if (roomCode["room"] != null) {
			socket.Emit ("leaveRoom", roomCode);
		}
	}
}
