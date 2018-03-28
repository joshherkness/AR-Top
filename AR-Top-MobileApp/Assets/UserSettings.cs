using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using TMPro;

public class UserSettings : MonoBehaviour {

	public RectTransform settingsPanel;
	public Sprite settingsGear;
	public Sprite closeX;
	public Image settingsIcon;
	private TMP_Dropdown[] dropdowns;

	public Button[] buttons;

	public GameObject voxelFinder;
	public TextMeshProUGUI coordinatesDisplayText;
	public Button coordinateOnButton;
	public Button coordinateOffButton;

	// Use this for initialization
	void Start () {
		dropdowns = GetComponentsInChildren <TMP_Dropdown> ();
		settingsPanel.gameObject.SetActive (false);
		settingsIcon.sprite = settingsGear;

		if (PlayerPrefs.HasKey ("UserAA"))
			QualitySettings.antiAliasing = PlayerPrefs.GetInt ("UserAA");
		else {
			QualitySettings.antiAliasing = 2;
			PlayerPrefs.SetInt ("UserAA", 2);
		}

		setDropdownValue ();
	}

	void setDropdownValue (){
		int index = 2;
		if (PlayerPrefs.HasKey ("UserAA")) {
			index = PlayerPrefs.GetInt ("UserAA");
		}
		TMP_Dropdown dropdown = dropdowns [0];
		switch (index) {
		case 0:
			dropdown.value = 0;
			break;
		case 2:
			dropdown.value = 1;
			break;
		case 4:
			dropdown.value = 2;
			break;
		case 8:
			dropdown.value = 3;
			break;
		}

	}

	void Update(){
		if (Input.GetKeyDown (KeyCode.Escape)){
			closeSettingsPanel ();
		}
	}
	
	public void setAntiAliasing (){
		int index = 2;
		TMP_Dropdown dropdown = dropdowns [0];
		switch (dropdown.value) {
		case 0:
			index = 0;
			break;
		case 1:
			index = 2;
			break;
		case 2:
			index = 4;
			break;
		case 3:
			index = 8;
			break;
		}
		QualitySettings.antiAliasing = index;
		PlayerPrefs.SetInt ("UserAA", index);
		print (index); 
	}

	public void setSettingsPanel (){
		if (settingsPanel.gameObject.activeInHierarchy) {
			settingsPanel.gameObject.SetActive (false);
			settingsIcon.sprite = settingsGear;

			foreach (Button button in buttons) {
				button.gameObject.SetActive (true);
			}
		} else {
			settingsPanel.gameObject.SetActive (true);
			settingsIcon.sprite = closeX;

			foreach (Button button in buttons) {
				button.gameObject.SetActive (false);
			}
		}
	}

	public void closeSettingsPanel(){
		settingsPanel.gameObject.SetActive (false);
	}

	public void toggleCoordinates(){
		if (voxelFinder.activeInHierarchy) {
			voxelFinder.gameObject.SetActive (false);
			coordinatesDisplayText.enabled = false;
			coordinateOnButton.interactable = true;
			coordinateOffButton.interactable = false;
		} else {
			voxelFinder.gameObject.SetActive (true);
			coordinatesDisplayText.enabled = true;
			coordinateOnButton.interactable = false;
			coordinateOffButton.interactable = true;
		}
	}
}
