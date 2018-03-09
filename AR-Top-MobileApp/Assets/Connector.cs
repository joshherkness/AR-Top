﻿using System.Collections;
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

	// Use this for initialization
	void Start () {
		DontDestroyOnLoad (this.gameObject);
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

	}

	// Update is called once per frame
	void Update () {
		
	}

	public void connection(JSONObject js){
		//socket.url = socketurlbase;
		//socket.url += "&room=" + js ["roomNumber"];
		//print (socket.url); 
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
		Debug.LogError ("error event received from socket server" + e.data.ToString ());
		if (room != null) {
			print (room); 
			room.serverErrorReceived (e);
		}
	}

	public void OnSceneLoaded(Scene scene, LoadSceneMode mode){
		MapController jsonReader = FindObjectOfType<MapController> ();
		print (jsonReader);
		if (scene.name == "main") {
			VuforiaBehaviour.Instance.enabled = true;
			SceneManager.SetActiveScene (SceneManager.GetSceneByName ("main"));
			SceneManager.UnloadSceneAsync ("Login");
		} else {
			VuforiaBehaviour.Instance.enabled = false;
			SceneManager.SetActiveScene (SceneManager.GetSceneByName ("Login"));
			SceneManager.UnloadSceneAsync ("main");
			mainSceneLoaded = false;
			Destroy (this);
		}

	}
}
