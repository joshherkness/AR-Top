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

	// Use this for initialization
	void Start () {
		camera = GameObject.FindGameObjectWithTag("MainCamera");
		displayTextBox = GameObject.FindGameObjectWithTag("CoordinatesDisplay").GetComponent<TextMeshProUGUI>();
		gameObject.transform.SetParent(camera.transform);
		coordinatesText = "(0,0,0)\n(x,y,z)";
	}
	
	// Update is called once per frame
	void Update () {
		GameObject hitObject = findVoxel();
		if (hitObject != prevHitObject)
		{
			Vector3 hitObjectPos = hitObject.transform.position * 10;
			coordinatesText = "(" + Math.Round(hitObjectPos.x) + ',';
			coordinatesText += Math.Round(hitObjectPos.z) + ",";
			coordinatesText += Math.Round(hitObjectPos.y) + ")";
			displayTextBox.text = coordinatesText;
		}
		prevHitObject = hitObject;
	}

	public GameObject findVoxel()
	{
		//cast ray from camera in forward camera direction
		var finderRay = new Ray(camera.transform.position, camera.transform.forward);
		var resultHit = new RaycastHit();
		Physics.Raycast(finderRay, out resultHit);
		//whatever ray hits, get info
		return resultHit.collider.gameObject;
	}
}
