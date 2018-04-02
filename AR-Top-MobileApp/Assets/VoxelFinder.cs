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
				Vector3 hitObjectPos = hitObject.transform.position * 10;
				if (hitObject.GetComponentInParent <RaycastText> () != null) {
					RaycastText raycastText = hitObject.GetComponentInParent <RaycastText> ();
					coordinatesText = raycastText.getRaycastInfoText ();
					displayTextBox.text = coordinatesText;
				} 

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
