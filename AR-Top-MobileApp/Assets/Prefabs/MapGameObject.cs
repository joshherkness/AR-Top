using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class MapGameObject : MonoBehaviour {
	static GameObject mapGameObject = null;
	private MapController mapController;


	string dataAsJson;

	// Use this for initialization
	void Awake () {
		
		if (mapGameObject != null) {
			Destroy (this.gameObject);
		} else {
			mapGameObject = this.gameObject;
			GameObject.DontDestroyOnLoad (gameObject);
		}
	}
	
	// Update is called once per frame
	void Update () {
		
	}

	public void setMap (string JSON){
		dataAsJson = JSON;

		if (mapController != null) {
			mapController.setMapJSON (dataAsJson);
		}
	}

	public string getMap (){
		return dataAsJson;
	}

	public void findMapController (){
		if (mapController == null) {
			mapController = FindObjectOfType<MapController> ();
		}
	}
}
