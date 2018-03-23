using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class QuitApp : MonoBehaviour {

	public void Update(){
		if (Input.GetKeyDown (KeyCode.Escape)){
			QuitApplication ();
		}
	}

	public void QuitApplication(){
		if (SceneManager.GetActiveScene().name == "Login") {
			Application.Quit ();
		}
	}
}
