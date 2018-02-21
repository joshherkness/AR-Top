using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using System;
using Vuforia;

public class JSONReader : MonoBehaviour
{

	[SerializeField] GameObject tilePrefab;
	[SerializeField] GameObject gridPrefab;

	private GameObject mapLayer;
	private GameObject baseLayer;
	private GameObject modelLayer;

	/**
	 * Structure used to represent a single model within the map.
	 */
	[Serializable]
	public struct GridModel
	{
		public string type;
		public Vector3 position;
		public string color;
	}
		
	/**
	 * Structure used to describe a map.
	 */
	[Serializable]
	public struct Grid
	{
		public int width;
		public int height;
		public int depth;

		public string color;

		public GridModel[] models;
	}

	void Start () 
	{

		// Set anti-aliasing
		// TODO: Move this setting outside this script.
		QualitySettings.antiAliasing = 2;

		buildLayers ();

		string dataAsJson = "";

		// Load example file
		string filePath = Path.Combine(Application.streamingAssetsPath,"TestData/voxel_cube_8x8.json");
		if (File.Exists (filePath)) {
			dataAsJson = File.ReadAllText(filePath); 
		}

		Grid grid = JsonUtility.FromJson<Grid> (dataAsJson);
		buildMap (grid);

	}

	public void UpdateJSON (string JSONstring)
	{
		Destroy (mapLayer);
		buildLayers ();
		Grid map = JsonUtility.FromJson<Grid> (JSONstring);
		buildMap (map);
	}

	void buildLayers ()
	{
		mapLayer = GameObject.Find ("MapLayer");
		if (mapLayer == null)
			mapLayer = new GameObject ("MapLayer");

		baseLayer = GameObject.Find ("GridLayer");
		if (baseLayer == null)
		{
			baseLayer = new GameObject ("GridLayer");
			baseLayer.transform.SetParent (mapLayer.transform);
		}

		modelLayer = GameObject.Find ("TileLayer");
		if (modelLayer == null)
		{
			modelLayer = new GameObject ("TileLayert");
			modelLayer.transform.SetParent (mapLayer.transform);
		}
	}

	void buildMap (Grid obj)
	{
		int row = (int) obj.width;
		int col = (int) obj.depth;

		for (int i = 0; i < row; i++)
		{
			for (int j = 0; j < col; j++)
			{
				// Create the grid base
				Vector3 tilesVector = new Vector3 (i, -1f, j);
				GameObject tile = Instantiate (tilePrefab, tilesVector, Quaternion.identity);
				tile.transform.SetParent (modelLayer.transform);
				colorize (tile, obj.color);
			}
		}

		foreach (GridModel model in obj.models)
			buildPiece (model);

		Vector3 position = new Vector3 ((mapLayer.transform.position.x - (obj.width / 2))*.1f, mapLayer.transform.position.y*.1f, (mapLayer.transform.position.z - (obj.depth / 2))*.1f);
		mapLayer.transform.Translate (position);
		mapLayer.transform.localScale = this.gameObject.transform.localScale;
		mapLayer.transform.SetParent (this.gameObject.transform);

	}

	//Builds a piece based on its type. Places the piece and gives it its color.
	void buildPiece (GridModel obj)
	{

		//Checks the type of the piece. Will be converted to a switch statement to check for all types.
		switch (obj.type) 
		{

		case "voxel": 
			Vector3 tileVector = obj.position;
			GameObject tilePiece = Instantiate (tilePrefab, tileVector, Quaternion.identity);
			tilePiece.transform.SetParent (modelLayer.transform);
			colorize (tilePiece, obj.color); 
			break;
		}
	}

	static void colorize (GameObject obj, String stringColor)
	{
		MeshRenderer[] meshes = obj.GetComponentsInChildren<MeshRenderer> ();

		foreach (MeshRenderer mesh in meshes)
		{
			Color color;
			if (ColorUtility.TryParseHtmlString (stringColor, out color)) 
			{
				Renderer renderer = mesh.GetComponent<Renderer> ();
				renderer.material.color = color;
			}
		}
	}
}