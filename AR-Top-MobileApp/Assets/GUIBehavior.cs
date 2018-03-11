using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/**
 * GUIBehavior is a script that will control the behavior of the GUI
 * icons on the bottom of the screen.
 * This includes Exit to Login
 * Toggle Pan - Pan the map with a single finger
 * Toggle Rotation - Rotate the map along Y axis with 2 fingers
 * Toggle Scale - Grow/Shrink mape with 2 finger pinch motion
 * Reset Map - Resets the map to starting Position, Scale, and Rotation.
 * Toggle icons will Enable/Disable feature.
 **/
public class GUIBehavior : MonoBehaviour {

	private Vector3 startingPosition;
	private Vector3 startingScale;
	private Vector3 startingRotation;
	private GameObject mapLayer;

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		
	}

	/**
	 * set Starting Position sets the starting values for the Position, Rotation, and Scale
	 **/
	public void setStartingPositions (Transform obj){
		print (obj.position); 
		startingPosition = obj.position;
		startingScale = obj.localScale;
		startingRotation = obj.localEulerAngles;
		mapLayer = obj.gameObject;
	}

	public void resetMapLayer (){
		mapLayer.transform.position = startingPosition;
		mapLayer.transform.localScale = startingScale;
		mapLayer.transform.localEulerAngles = startingRotation;
	}
}
