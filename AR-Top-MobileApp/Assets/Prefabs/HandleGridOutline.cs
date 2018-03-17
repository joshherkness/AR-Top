using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HandleGridOutline : MonoBehaviour {
	private UserSettings userSettings;
	private SpriteRenderer sprite;
	// Use this for initialization
	void Start () {
		userSettings = FindObjectOfType<UserSettings> ();
		userSettings.onOutlineChanged += OnOutlineChanged;
		sprite = GetComponent <SpriteRenderer> ();
	}

	public void OnOutlineChanged (string outline){
		string name = this.transform.name;
		if (outline == "None")
			sprite.enabled = false;
		else if (outline == "Full")
			sprite.enabled = true;
		else {
			sprite.enabled = false;
			if (name == "GridFaceTop")
				sprite.enabled = true;
		}
	}

	void OnDestroy(){
		userSettings.onOutlineChanged -= OnOutlineChanged;
	}

	public void changeOutlines (){
		OnOutlineChanged (PlayerPrefs.GetString ("UserGrid"));
	}
}
