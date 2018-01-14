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

	//GridItem is serializable to make it JSON friendly.
	[Serializable]
	public class GridItem
	{
		public string type = null; //The type of the piece. Could be "character", "tile", or "npc".

		//x, y, z coordinates, and RGBA color floats. For grid, x, y, z are number of tiles in each direction.
		public int x = 0;
		public int y = 0;
		public int z = 0;
		public float red = 1f;
		public float green = 1f;
		public float blue = 1f;
		public float alpha = 1f;
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

		//This creates a game object to play around with. Eventually this
		//will be replaced by retrieving the JSON object from the server.
		GridItem obj = new GridItem ();
		obj.type = "character";
		obj.x = 1;
		obj.y = 0;
		obj.z = 1;
		obj.red = 0.2f;
		obj.green = 1f;
		obj.blue = 0.2f;
		obj.alpha = 1f;

		GridItem grid = new GridItem ();
		grid.type = "grid";
		grid.x = 5;
		grid.y = 2;
		grid.z = 7;
		grid.red = 0.2f;
		grid.green = 0.2f;
		grid.blue = 0.2f;
		grid.alpha = 1f;

		GridItem tilepiece = new GridItem ();
		tilepiece.type = "tile";
		tilepiece.x = 3;
		tilepiece.y = 0;
		tilepiece.z = 3;
		tilepiece.red = 1f;
		tilepiece.green = 0f;
		tilepiece.blue = 0f;
		tilepiece.alpha = 1f;

		GridItem tilepiece1 = new GridItem ();
		tilepiece1.type = "tile";
		tilepiece1.x = 4;
		tilepiece1.y = 0;
		tilepiece1.z = 3;
		tilepiece1.red = 1f;
		tilepiece1.green = 0f;
		tilepiece1.blue = 0f;
		tilepiece1.alpha = 1f;

		GridItem tilepiece2 = new GridItem ();
		tilepiece2.type = "tile";
		tilepiece2.x = 3;
		tilepiece2.y = 0;
		tilepiece2.z = 4;
		tilepiece2.red = 1f;
		tilepiece2.green = 0f;
		tilepiece2.blue = 0f;
		tilepiece2.alpha = 1f;

		GridItem tilepiece3 = new GridItem ();
		tilepiece3.type = "tile";
		tilepiece3.x = 4;
		tilepiece3.y = 0;
		tilepiece3.z = 4;
		tilepiece3.red = 1f;
		tilepiece3.green = 0f;
		tilepiece3.blue = 0f;
		tilepiece3.alpha = 1f;

		GridItem enemy = new GridItem ();
		enemy.type = "npc";
		enemy.x = 4;
		enemy.y = 0;
		enemy.z = 3;
		enemy.red = 0f;
		enemy.green = 0f;
		enemy.blue = 0f;
		enemy.alpha = 1f;

		//builds the piece.
		buildPiece (obj);
		buildPiece (grid);
		buildPiece (tilepiece);
		buildPiece (tilepiece1);
		buildPiece (tilepiece2);
		buildPiece (tilepiece3);
		buildPiece (enemy);
	}
	
	// Update is called once per frame
	void Update () {
		
	}

	//Builds a piece based on its type. Places the piece and gives it its color.
	void buildPiece (GridItem obj)
	{
		
		GridItem piece = JsonUtility.FromJson<GridItem> (JsonUtility.ToJson (obj)); //Makes the object a JSON serialized object.

		//Checks the type of the piece. Will be converted to a switch statement to check for all types.
		switch (piece.type) {
		case "grid":
			int row = obj.x;
			int col = obj.z;
			int height = obj.y;

			for (int i = 1; i <= row; i++) {
				for (int j = 1; j <= col; j++) {
					//Create a grid.
					Vector3 gridVector = new Vector3 (i, .02f, j);
					GameObject gridspace = Instantiate (gridPrefab, gridVector, Quaternion.identity);
					gridspace.transform.SetParent (gridLayout.transform);
					//Create the plane.
					Vector3 tilesVector = new Vector3 (i, 0f, j);
					GameObject tile = Instantiate (tilePrefab, tilesVector, Quaternion.identity);
					tile.transform.SetParent (tileLayout.transform);
					fillColor (piece, tile);
				}
			}
			for (int k = 0; k <= height; k++) {
				if (k % gridHeightGap == 0) {
					Vector3 gridVector = new Vector3 (getGridSize (row), k, getGridSize (col));
					GameObject gridOutline = Instantiate (gridPrefab, gridVector, Quaternion.identity);
					gridOutline.transform.SetParent (gridLayout.transform);
					gridOutline.transform.localScale = new Vector3 (row, 1, col);
				}
			}
			break;	

		case "tile": 
			Vector3 tileVector = new Vector3 (piece.x, piece.y + .01f, piece.z); //Tile's position.
			GameObject tilePiece = Instantiate (tilePrefab, tileVector, Quaternion.identity); //Creates a tile prefab.
			tilePiece.transform.SetParent (tileLayout.transform); //Sets parent to TileLayout GameObject.
			fillColor (piece, tilePiece); 
			break;

		case "character":
			Vector3 charVector = new Vector3 (piece.x, piece.y, piece.z); //Character's position.
			GameObject character = Instantiate (charPrefab, charVector, Quaternion.identity); //Creates a character prefab.
			character.transform.SetParent (playerLayout.transform); //Sets parent to PlayerLayout GameObject.
			fillColor (piece, character);
			break;
		

		case "npc": 
			Vector3 npcVector = new Vector3 (piece.x, piece.y, piece.z); //Character's position.
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
			Color color = new Color (piece.red, piece.green, piece.blue, piece.alpha);
			rend.material.color = color;
		}
	}

	float getGridSize (int n){
		return (n + 1) / 2f;
	}
}
