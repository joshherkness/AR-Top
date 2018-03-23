using System;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class VoxelFinder : MonoBehaviour
{
	private GameObject camera;
	private TextMeshProUGUI displayTextBox;
	private string coordinatesText;
	private GameObject prevHitObject;
	private MapController mapController;

	// Use this for initialization
	void Start () {
		camera = GameObject.FindGameObjectWithTag("MainCamera");
		displayTextBox = GameObject.FindGameObjectWithTag("CoordinatesDisplay").GetComponent<TextMeshProUGUI>();
		gameObject.transform.SetParent(camera.transform);
		coordinatesText = "";
		mapController = FindObjectOfType<MapController> ();
	}
	
	// Update is called once per frame
	void Update () {
		GameObject hitObject = findVoxel();
		if (hitObject != null) {
			if (hitObject != prevHitObject) {
				Vector3 offset = mapController.getOffset () * 10;
				print (offset); 
				Vector3 hitObjectPos = hitObject.transform.position * 10;
				coordinatesText = "(" + Math.Round (hitObjectPos.x - offset.x) + ',';
				coordinatesText += Math.Round (hitObjectPos.z - offset.z) + ",";
				coordinatesText += Math.Round (hitObjectPos.y + 1) + ")";
				displayTextBox.text = coordinatesText;
			}
			prevHitObject = hitObject;
		} else {
			displayTextBox.text = "";
		}

	}

	public GameObject findVoxel()
	{
		//cast ray from camera in forward camera direction
		var finderRay = new Ray(camera.transform.position, camera.transform.forward);
		var resultHit = new RaycastHit();
		if (Physics.Raycast (finderRay, out resultHit)) {
			//whatever ray hits, get info
			return resultHit.collider.gameObject;
		} else {
			return null;
		}
	}
}
