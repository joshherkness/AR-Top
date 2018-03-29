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

	/**
	 * Sets the dropdown index value
	 * by taking the Anti-Aliasing stored in PlayerPrefs
	 * and shifting the bit 1 place to the right.
	 */
	void setDropdownValue (){
		int index = 2;
		if (PlayerPrefs.HasKey ("UserAA")) {
			index = PlayerPrefs.GetInt ("UserAA");
		}
		TMP_Dropdown dropdown = dropdowns [0];
		dropdown.value = index >> 1;
	}

	void Update(){
		if (Input.GetKeyDown (KeyCode.Escape)){
			closeSettingsPanel ();
		}
	}

	/**
	 * Sets Unity's Anti-Aliasing Setting
	 * The index of the dropdown is used to power 2
	 * e.g. User selects 4. Dropdown index is 2. 2^2=4
	 *		Anti-Aliasing is set to 4x
	 *
	 * Powering was chosen over bitshifting because
	 * 3 << 1 = 6, which does not reach 8x Anti-Aliasing
	 * but 2^0 = 1, which will reach 0 Anti-Aliasing
	 * Since Anti-Aliasing defaults to the first setting
	 * equal to or lower than the given index.
	 */
	public void setAntiAliasing (){
		int index = 2;
		TMP_Dropdown dropdown = dropdowns [0];

		index = (int) Math.Pow(2.0, (double)dropdown.value);

		QualitySettings.antiAliasing = index;
		PlayerPrefs.SetInt ("UserAA", index);
		print (index);
	}

	/**
	 * Sets the settings panel to active or inactive
	 * Also sets appropriate buttons on or off
	 * and changes the "Gear" icon to an "X" icon
	 */
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

	/**
	 * Toggles the Coordinate Display text on and off
	 */
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
