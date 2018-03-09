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

	public delegate void OnOutlineChanged(string outline);
	public event OnOutlineChanged onOutlineChanged;

	// Use this for initialization
	void Start () {
		dropdowns = GetComponentsInChildren <TMP_Dropdown> ();
		settingsPanel.gameObject.SetActive (false);
		settingsIcon.sprite = settingsGear;
		onOutlineChanged += outlineChange;

		if (PlayerPrefs.HasKey ("UserAA"))
			QualitySettings.antiAliasing = PlayerPrefs.GetInt ("UserAA");
		else {
			QualitySettings.antiAliasing = 2;
			PlayerPrefs.SetInt ("UserAA", 2);
		}

		if (PlayerPrefs.HasKey ("UserGrid")) {
			onOutlineChanged(PlayerPrefs.GetString ("UserGrid"));
		} else {
			PlayerPrefs.SetString ("UserGrid", "Full");
			onOutlineChanged ("Full");
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

	public void setGridOutlineCounts (){
		TMP_Dropdown dropdown = dropdowns [1];
		switch (dropdown.value) {
		case 0:
			PlayerPrefs.SetString ("UserGrid", "None");
			break;
		case 1:
			PlayerPrefs.SetString ("UserGrid", "Top");
			break;
		case 2:
			PlayerPrefs.SetString ("UserGrid", "Full");
			break;
		}
		onOutlineChanged(PlayerPrefs.GetString ("UserGrid"));
	}

	public void setSettingsPanel (){
		if (settingsPanel.gameObject.activeInHierarchy) {
			settingsPanel.gameObject.SetActive (false);
			settingsIcon.sprite = settingsGear;
		} else {
			settingsPanel.gameObject.SetActive (true);
			settingsIcon.sprite = closeX;
		}
	}

	public void outlineChange (string str){
	
	}
}
