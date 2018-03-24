using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ObjectPoolerScript : MonoBehaviour {

	public static ObjectPoolerScript current;
	[SerializeField] GameObject pooledObject;
	[SerializeField] int pooledAmount = 1600;
	[SerializeField] int maxAmount = 1600;

	[SerializeField] List<GameObject> pooledObjects;

	void Awake(){
		current = this;
	}

	// Use this for initialization
	void Start () {
		pooledObjects = new List<GameObject> ();
		for (int i = 0; i < pooledAmount; i++) {
			GameObject obj = (GameObject)Instantiate (pooledObject);
			obj.SetActive (false);
			pooledObjects.Add (obj);
		}
	}

	public GameObject getPooledObject (){
		for (int i = 0; i < pooledAmount; i++) {
			if (pooledObjects [i].transform.parent == null) {
				return pooledObjects [i];
			}
		}

		if (pooledObjects.Count < maxAmount) {
			GameObject obj = (GameObject)Instantiate (pooledObject);
			pooledObjects.Add (obj);
			pooledAmount = pooledObjects.Count;
			return obj;
		}

		return null;
	}

	public int getMaxAmount(){
		return maxAmount;
	}
}
