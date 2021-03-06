﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RaycastText : MonoBehaviour {

	[SerializeField] private string raycastInfoText = "";

	public void appendRaycastInfoText(string text){
		raycastInfoText += text;
	}

	public string getRaycastInfoText(){
		return raycastInfoText;
	}

	public void clearRaycastInfoText(){
		raycastInfoText = "";
	}
}
