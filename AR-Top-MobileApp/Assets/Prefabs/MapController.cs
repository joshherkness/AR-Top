using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using System;
using Vuforia;

public class MapController : MonoBehaviour
{

	[SerializeField] GameObject tilePrefab;
	[SerializeField] GameObject gridPrefab;
	[SerializeField] GameObject playerPrefab;

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
		string filePath = Path.Combine(Application.streamingAssetsPath, "TestData/voxel_shell_x8.json");
		if (File.Exists (filePath)) {
			dataAsJson = File.ReadAllText (filePath); 
		} else {
			dataAsJson = "{\n  \"width\": 4,\n  \"height\": 48,\n  \"depth\": 4,\n  \"color\": \"#FFFFFF\",\n  \"id\": \"5a8a417e2a74a062699e6075\",\n  \"name\": \"Tiny Shell\",\n  \"models\": [\n    {\n      \"position\": {\n        \"x\": 0,\n        \"y\": 0,\n        \"z\": 0\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#fe78cc\"\n    },\n    {\n      \"position\": {\n        \"x\": 0,\n        \"y\": 1,\n        \"z\": 0\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#0600b8\"\n    },\n    {\n      \"position\": {\n        \"x\": 0,\n        \"y\": 2,\n        \"z\": 0\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#ad7f3e\"\n    },\n    {\n      \"position\": {\n        \"x\": 0,\n        \"y\": 3,\n        \"z\": 0\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#fc8e04\"\n    },\n    {\n      \"position\": {\n        \"x\": 0,\n        \"y\": 0,\n        \"z\": 1\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#1ba754\"\n    },\n    {\n      \"position\": {\n        \"x\": 0,\n        \"y\": 1,\n        \"z\": 1\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#831575\"\n    },\n    {\n      \"position\": {\n        \"x\": 0,\n        \"y\": 2,\n        \"z\": 1\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#833088\"\n    },\n    {\n      \"position\": {\n        \"x\": 0,\n        \"y\": 3,\n        \"z\": 1\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#ca3b2a\"\n    },\n    {\n      \"position\": {\n        \"x\": 0,\n        \"y\": 0,\n        \"z\": 2\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#843bef\"\n    },\n    {\n      \"position\": {\n        \"x\": 0,\n        \"y\": 1,\n        \"z\": 2\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#5b925c\"\n    },\n    {\n      \"position\": {\n        \"x\": 0,\n        \"y\": 2,\n        \"z\": 2\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#4beaf9\"\n    },\n    {\n      \"position\": {\n        \"x\": 0,\n        \"y\": 3,\n        \"z\": 2\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#1b2d66\"\n    },\n    {\n      \"position\": {\n        \"x\": 0,\n        \"y\": 0,\n        \"z\": 3\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#8545a6\"\n    },\n    {\n      \"position\": {\n        \"x\": 0,\n        \"y\": 1,\n        \"z\": 3\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#eb8538\"\n    },\n    {\n      \"position\": {\n        \"x\": 0,\n        \"y\": 2,\n        \"z\": 3\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#e55982\"\n    },\n    {\n      \"position\": {\n        \"x\": 0,\n        \"y\": 3,\n        \"z\": 3\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#ae67e3\"\n    },\n    {\n      \"position\": {\n        \"x\": 1,\n        \"y\": 0,\n        \"z\": 0\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#f1a95c\"\n    },\n    {\n      \"position\": {\n        \"x\": 1,\n        \"y\": 1,\n        \"z\": 0\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#2d488b\"\n    },\n    {\n      \"position\": {\n        \"x\": 1,\n        \"y\": 2,\n        \"z\": 0\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#adc187\"\n    },\n    {\n      \"position\": {\n        \"x\": 1,\n        \"y\": 3,\n        \"z\": 0\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#f59760\"\n    },\n    {\n      \"position\": {\n        \"x\": 1,\n        \"y\": 0,\n        \"z\": 1\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#f37f61\"\n    },\n    {\n      \"position\": {\n        \"x\": 1,\n        \"y\": 3,\n        \"z\": 1\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#4b5478\"\n    },\n    {\n      \"position\": {\n        \"x\": 1,\n        \"y\": 0,\n        \"z\": 2\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#2aeadf\"\n    },\n    {\n      \"position\": {\n        \"x\": 1,\n        \"y\": 3,\n        \"z\": 2\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#919626\"\n    },\n    {\n      \"position\": {\n        \"x\": 1,\n        \"y\": 0,\n        \"z\": 3\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#91b487\"\n    },\n    {\n      \"position\": {\n        \"x\": 1,\n        \"y\": 1,\n        \"z\": 3\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#5a357a\"\n    },\n    {\n      \"position\": {\n        \"x\": 1,\n        \"y\": 2,\n        \"z\": 3\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#ac83f0\"\n    },\n    {\n      \"position\": {\n        \"x\": 1,\n        \"y\": 3,\n        \"z\": 3\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#aa4158\"\n    },\n    {\n      \"position\": {\n        \"x\": 2,\n        \"y\": 0,\n        \"z\": 0\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#0c60c9\"\n    },\n    {\n      \"position\": {\n        \"x\": 2,\n        \"y\": 1,\n        \"z\": 0\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#838c61\"\n    },\n    {\n      \"position\": {\n        \"x\": 2,\n        \"y\": 2,\n        \"z\": 0\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#483b1b\"\n    },\n    {\n      \"position\": {\n        \"x\": 2,\n        \"y\": 3,\n        \"z\": 0\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#1b16b3\"\n    },\n    {\n      \"position\": {\n        \"x\": 2,\n        \"y\": 0,\n        \"z\": 1\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#947685\"\n    },\n    {\n      \"position\": {\n        \"x\": 2,\n        \"y\": 3,\n        \"z\": 1\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#83da28\"\n    },\n    {\n      \"position\": {\n        \"x\": 2,\n        \"y\": 0,\n        \"z\": 2\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#0fd922\"\n    },\n    {\n      \"position\": {\n        \"x\": 2,\n        \"y\": 3,\n        \"z\": 2\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#a615d3\"\n    },\n    {\n      \"position\": {\n        \"x\": 2,\n        \"y\": 0,\n        \"z\": 3\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#bf0cdf\"\n    },\n    {\n      \"position\": {\n        \"x\": 2,\n        \"y\": 1,\n        \"z\": 3\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#495b90\"\n    },\n    {\n      \"position\": {\n        \"x\": 2,\n        \"y\": 2,\n        \"z\": 3\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#f28975\"\n    },\n    {\n      \"position\": {\n        \"x\": 2,\n        \"y\": 3,\n        \"z\": 3\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#e820ab\"\n    },\n    {\n      \"position\": {\n        \"x\": 3,\n        \"y\": 0,\n        \"z\": 0\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#fcb82e\"\n    },\n    {\n      \"position\": {\n        \"x\": 3,\n        \"y\": 1,\n        \"z\": 0\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#9d33a6\"\n    },\n    {\n      \"position\": {\n        \"x\": 3,\n        \"y\": 2,\n        \"z\": 0\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#1d91f4\"\n    },\n    {\n      \"position\": {\n        \"x\": 3,\n        \"y\": 3,\n        \"z\": 0\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#93949e\"\n    },\n    {\n      \"position\": {\n        \"x\": 3,\n        \"y\": 0,\n        \"z\": 1\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#64de74\"\n    },\n    {\n      \"position\": {\n        \"x\": 3,\n        \"y\": 1,\n        \"z\": 1\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#f72433\"\n    },\n    {\n      \"position\": {\n        \"x\": 3,\n        \"y\": 2,\n        \"z\": 1\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#2e8176\"\n    },\n    {\n      \"position\": {\n        \"x\": 3,\n        \"y\": 3,\n        \"z\": 1\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#9eba4c\"\n    },\n    {\n      \"position\": {\n        \"x\": 3,\n        \"y\": 0,\n        \"z\": 2\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#887441\"\n    },\n    {\n      \"position\": {\n        \"x\": 3,\n        \"y\": 1,\n        \"z\": 2\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#b3bd90\"\n    },\n    {\n      \"position\": {\n        \"x\": 3,\n        \"y\": 2,\n        \"z\": 2\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#9ca6f1\"\n    },\n    {\n      \"position\": {\n        \"x\": 3,\n        \"y\": 3,\n        \"z\": 2\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#129246\"\n    },\n    {\n      \"position\": {\n        \"x\": 3,\n        \"y\": 0,\n        \"z\": 3\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#90ab01\"\n    },\n    {\n      \"position\": {\n        \"x\": 3,\n        \"y\": 1,\n        \"z\": 3\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#c72993\"\n    },\n    {\n      \"position\": {\n        \"x\": 3,\n        \"y\": 2,\n        \"z\": 3\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#386140\"\n    },\n    {\n      \"position\": {\n        \"x\": 3,\n        \"y\": 3,\n        \"z\": 3\n      },\n      \"type\": \"voxel\",\n      \"color\": \"#6e6f65\"\n    }\n  ]\n}\n";
			dataAsJson = dataAsJson.Replace ("\n", "");
		}

		Grid grid = JsonUtility.FromJson<Grid> (dataAsJson);
		buildMap (grid);

	}

	public void setMapJSON (string JSONstring)
	{
		Destroy (baseLayer);
		Destroy (modelLayer);
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
		Vector3 tileVector = obj.position;
		GameObject tilePiece;
		//Checks the type of the piece. Will be converted to a switch statement to check for all types.
		switch (obj.type) 
		{
		case "voxel": 
			tilePiece = Instantiate (tilePrefab, tileVector, Quaternion.identity);
			tilePiece.transform.SetParent (modelLayer.transform);
			colorize (tilePiece, obj.color);
			break;
		case "player": 
			tilePiece = Instantiate (playerPrefab, tileVector, Quaternion.identity);
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