using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using Vuforia;

public class JSONReader : MonoBehaviour {

	//Simple prefabs that can be altered later.
	[SerializeField] GameObject charPrefab;
	[SerializeField] GameObject tilePrefab;
	[SerializeField] GameObject gridPrefab;
	[SerializeField] GameObject npcPrefab;

	//GameObjects that will be used to organize the hierarchy and scale the layout.
	private GameObject mapScaler;
	private GameObject gridLayout;
	private GameObject playerLayout;
	private GameObject tileLayout;
	private GameObject npcLayout;

	private int gridHeightGap = 2; //The height gap for y coordinate grid spaces. Every increment represents 5 gamefoot.

	//A test JSON string to use until we pull directly from the server.
	private string JSONSTRING = @"
	{
	""width"": 16,
	""height"": 2,
	""depth"": 16,
	""base_color"": 
	{
		""r"": 0.69,
		""g"": 0.69,
		""b"": 0.69,
		""a"": 1.0
	},
	""models"": 
	[
		{
		""type"": ""voxel"",
		""position"": 
			{
				""x"": 1,
				""y"": 1,
				""z"": 1
			},
			""color"": 
			{
				""r"": 0.25,
				""g"": 0.25,
				""b"": 1,
				""a"": 1.0
			}
		},
		{
		""type"":""voxel"",
		""position"":
			{
				""x"": 3,
				""y"": 1,
				""z"": 10
			},
			""color"":
			{
				""r"": 0.25,
				""g"": 0.25,
				""b"": 1,
				""a"": 1.0
			}
		},
		{
		""type"":""voxel"",
		""position"":
			{
				""x"": 5,
				""y"": 1,
				""z"": 4
			},
			""color"":
			{
				""r"": 0.25,
				""g"": 0.25,
				""b"": 1,
				""a"": 1.0
			}
		},
		{
		""type"":""voxel"",
		""position"":
			{
				""x"": 15,
				""y"": 1,
				""z"": 5
			},
			""color"":
			{
				""r"": 0.25,
				""g"": 0.25,
				""b"": 1,
				""a"": 1.0
			}
		},
		{
		""type"":""voxel"",
		""position"":
			{
				""x"": 11,
				""y"": 1,
				""z"": 15
			},
			""color"":
			{
				""r"": 0.25,
				""g"": 0.25,
				""b"": 1,
				""a"": 1.0
			}
		},
		{
		""type"":""voxel"",
		""position"":
			{
				""x"": 8,
				""y"": 1,
				""z"": 10
			},
			""color"":
			{
				""r"": 0.25,
				""g"": 0.25,
				""b"": 1,
				""a"": 1.0
			}
		}
	]}";

	//GridItem is serializable to make it JSON friendly.
	//GridItems represent individual pieces to place on the board.
	[Serializable]
	public class GridItem
	{
		//All values for this class are default values.
		public string type = null; //The type of the piece. Could be "character", "tile", or "npc".

		//Vector3 position coordinates, and Vector4 color values.
		public Vector3 position = new Vector3 (0f, 0f, 0f);
		public Color color = new Color (1f, 1f, 1f, 1f);
	}

	//MapItem is serializable to make it JSON friendly.
	//MapItem contains information about the map and an array of GridItems.
	[Serializable]
	public class MapItem
	{
		public int width = 1;
		public int height = 1;
		public int depth = 1;

		public Color base_color = new Color(1f, 1f, 1f, 1f);

		public GridItem[] models = null;
	}



	// Use this for initialization
	void Start () {

		//Create an empty parent GameObject to control the scale of the entire layout.
		mapScaler = GameObject.Find ("MapScaler");
		if (mapScaler == null) {
			mapScaler = new GameObject ("MapScaler");
		}

		//Create an empty parent for the grid.
		gridLayout = GameObject.Find ("GridLayout");
		if (gridLayout == null){
			gridLayout = new GameObject("GridLayout");
			gridLayout.transform.SetParent (mapScaler.transform);
		}

		//Create an empty parent for the Player Character pieces.
		playerLayout = GameObject.Find ("PlayerLayout");
		if (playerLayout == null) {
			playerLayout = new GameObject ("PlayerLayout");
			playerLayout.transform.SetParent (mapScaler.transform);
		}

		//Create an empty parent for the NPC pieces.
		npcLayout = GameObject.Find ("NPCLayout");
		if (npcLayout == null) {
			npcLayout = new GameObject ("NPCLayout");
			npcLayout.transform.SetParent (mapScaler.transform);
		}

		//Create an empty parent for the Tile pieces.
		tileLayout = GameObject.Find ("TileLayout");
		if (tileLayout == null) {
			tileLayout = new GameObject ("TileLayout");
			tileLayout.transform.SetParent (mapScaler.transform);
		}

		MapItem grid = JsonUtility.FromJson<MapItem> (JSONSTRING);
		Vector3 gridVector = new Vector3 (-0.5f, 0, -0.5f);
		GridMesh gridMaker = Instantiate (gridPrefab, gridVector, Quaternion.identity).GetComponent <GridMesh>();
		gridMaker.transform.SetParent (gridLayout.transform);
		gridMaker.setSize (grid.width);
		buildMap (grid);

	}
	
	// Update is called once per frame
	void Update () {
		
	}

	void buildMap (MapItem obj){
		int row = (int) obj.width;
		int col = (int) obj.depth;
		int height = (int) obj.height;

		for (int i = 0; i < row; i++) {
			for (int j = 0; j < col; j++) {
				//Create a grid.
				/*Vector3 gridVector = new Vector3 (i, .52f, j);
				GameObject gridspace = Instantiate (gridPrefab, gridVector, Quaternion.identity);
				gridspace.transform.SetParent (gridLayout.transform);
				SpriteRenderer sprite = gridspace.GetComponentInChildren <SpriteRenderer> ();
				sprite.color = new Color (0f, 0f, 0f, 1f);*/
				//Create the plane.
				Vector3 tilesVector = new Vector3 (i, 0f, j);
				GameObject tile = Instantiate (tilePrefab, tilesVector, Quaternion.identity);
				tile.transform.SetParent (tileLayout.transform);
				fillColor (obj, tile);
			}
		}
		/*for (int k = 0; k <= height; k++) {
			if (k % gridHeightGap == 0) {
				Vector3 gridVector = new Vector3 (getGridSize (row) - 1, k + .52f, getGridSize (col) - 1);
				GameObject gridOutline = Instantiate (gridPrefab, gridVector, Quaternion.identity);
				gridOutline.transform.SetParent (gridLayout.transform);
				gridOutline.transform.localScale = new Vector3 (row, 1, col);
				SpriteRenderer sprite = gridOutline.GetComponentInChildren <SpriteRenderer> ();
				sprite.color = new Color (0f, 0f, 0f, 1f);
			}
		}*/

		foreach (GridItem model in obj.models) {
			buildPiece (model);
		}
	}

	//Builds a piece based on its type. Places the piece and gives it its color.
	void buildPiece (GridItem obj)
	{
		
		GridItem piece = JsonUtility.FromJson<GridItem> (JsonUtility.ToJson (obj)); //Makes the object a JSON serialized object.

		//Checks the type of the piece. Will be converted to a switch statement to check for all types.
		switch (piece.type) {

		case "voxel": 
			Vector3 tileVector = piece.position; //Tile's position.
			GameObject tilePiece = Instantiate (tilePrefab, tileVector, Quaternion.identity); //Creates a tile prefab.
			tilePiece.transform.SetParent (tileLayout.transform); //Sets parent to TileLayout GameObject.
			fillColor (piece, tilePiece); 
			break;

		case "character":
			Vector3 charVector = piece.position; //Character's position.
			GameObject character = Instantiate (charPrefab, charVector, Quaternion.identity); //Creates a character prefab.
			character.transform.SetParent (playerLayout.transform); //Sets parent to PlayerLayout GameObject.
			fillColor (piece, character);
			break;
		

		case "npc": 
			Vector3 npcVector = piece.position; //Character's position.
			GameObject npc = Instantiate (npcPrefab, npcVector, Quaternion.identity); //Creates a character prefab.
			npc.transform.SetParent (npcLayout.transform); //Sets parent to PlayerLayout GameObject.
			fillColor (piece, npc);
			break;
		}
	}

	static void fillColor (GridItem piece, GameObject obj)
	{
		MeshRenderer[] meshes = obj.GetComponentsInChildren<MeshRenderer> ();
		//Gets the child objects of the prefab by finding their MeshRenderer.
		//Foreach loop colors the tiles with the appropriate color.
		foreach (MeshRenderer mesh in meshes) {
			Renderer rend = mesh.GetComponent<Renderer> ();
			Color color = piece.color;
			rend.material.color = color;
		}
	}

	static void fillColor (MapItem piece, GameObject obj)
	{
		MeshRenderer[] meshes = obj.GetComponentsInChildren<MeshRenderer> ();
		//Gets the child objects of the prefab by finding their MeshRenderer.
		//Foreach loop colors the tiles with the appropriate color.
		foreach (MeshRenderer mesh in meshes) {
			Renderer rend = mesh.GetComponent<Renderer> ();
			Color color = piece.base_color;
			rend.material.color = color;
		}
	}

	float getGridSize (int n){
		return (n + 1) / 2f;
	}
}
