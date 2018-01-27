using System.Collections;
using System.Collections.Generic;
using UnityEngine;


[RequireComponent(typeof(MeshRenderer))]
[RequireComponent(typeof(MeshFilter))]
public class GridMesh : MonoBehaviour
{
	private int GridSize;
	//public int GridDepth;

	void DrawGrid ()
	{
		MeshFilter filter = gameObject.GetComponent<MeshFilter> ();
		var mesh = new Mesh ();
		var verticies = new List<Vector3> ();
		var indicies = new List<int> ();
		for (int i = 0; i <= GridSize; i++) {
			verticies.Add (new Vector3 (i, .52f, 0));
			verticies.Add (new Vector3 (i, .52f, GridSize));
			if (!indicies.Contains (4 * i + 0))
				indicies.Add (4 * i + 0);
			if (!indicies.Contains (4 * i + 1))
				indicies.Add (4 * i + 1);
			//if (!indicies.Contains (4 * i + 2))
			//indicies.Add (4 * i + 2);
			//if (!indicies.Contains (4 * i + 3))
			//indicies.Add (4 * i + 3);
			//}
			//for (int i = 0; i <= GridDepth; i++) {
			verticies.Add (new Vector3 (0, .52f, i));
			verticies.Add (new Vector3 (GridSize, .52f, i));
			//if (!indicies.Contains (4 * i + 0))
			//	indicies.Add (4 * i + 0);
			//if (!indicies.Contains (4 * i + 1))
			//	indicies.Add (4 * i + 1);
			if (!indicies.Contains (4 * i + 2))
				indicies.Add (4 * i + 2);
			if (!indicies.Contains (4 * i + 3))
				indicies.Add (4 * i + 3);
		}
		mesh.vertices = verticies.ToArray ();
		mesh.SetIndices (indicies.ToArray (), MeshTopology.Lines, 0);
		filter.mesh = mesh;
		MeshRenderer meshRenderer = gameObject.GetComponent<MeshRenderer> ();
		meshRenderer.material = new Material (Shader.Find ("Sprites/Default"));
		meshRenderer.material.color = Color.black;
	}

	public void setSize (int size){
		GridSize = size;
		DrawGrid ();
	}
}
