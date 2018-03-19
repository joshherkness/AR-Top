using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VoxelFinder : MonoBehaviour
{
	private GameObject camera;

	// Use this for initialization
	void Start () {
		camera = GameObject.FindGameObjectWithTag("MainCamera");
		gameObject.transform.SetParent(camera.transform);
	}
	
	// Update is called once per frame
	void Update () {
		GameObject hitObject = findVoxel();
		Debug.Log(hitObject.transform.position.ToString());
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
