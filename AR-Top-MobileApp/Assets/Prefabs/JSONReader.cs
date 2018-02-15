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
	private ImageTargetBehaviour imageTarget;
	//private AnchorStageBehaviour anchorStage;

	private int gridHeightGap = 2; //The height gap for y coordinate grid spaces. Every increment represents 5 gamefoot.

	//A test JSON string to use until we pull directly from the server.
	private string JSONSTRING = @"
	{
  ""width"": 32,
  ""height"": 10,
  ""depth"": 32,
  ""color"": ""#417505"",
  ""models"": [
    {
      ""position"": {
        ""x"": 14,
        ""y"": 0,
        ""z"": 14
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 0,
        ""z"": 14
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 12,
        ""y"": 0,
        ""z"": 14
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 11,
        ""y"": 0,
        ""z"": 14
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 10,
        ""y"": 0,
        ""z"": 14
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 14,
        ""y"": 0,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 14,
        ""y"": 0,
        ""z"": 12
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 14,
        ""y"": 0,
        ""z"": 11
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 14,
        ""y"": 0,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 0,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 12,
        ""y"": 0,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 11,
        ""y"": 0,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 10,
        ""y"": 0,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 0,
        ""z"": 14
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 0,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 0,
        ""z"": 11
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 0,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 8,
        ""y"": 0,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 7,
        ""y"": 0,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 6,
        ""y"": 0,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 8,
        ""y"": 0,
        ""z"": 11
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 7,
        ""y"": 0,
        ""z"": 11
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 6,
        ""y"": 0,
        ""z"": 11
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 5,
        ""y"": 0,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 0,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 0,
        ""z"": 12
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 0,
        ""z"": 11
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 0,
        ""z"": 9
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 0,
        ""z"": 8
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 0,
        ""z"": 7
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 0,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 0,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 0,
        ""z"": 9
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 0,
        ""z"": 8
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 0,
        ""z"": 7
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 0,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 8,
        ""y"": 0,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 5,
        ""y"": 0,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 10,
        ""y"": 0,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 11,
        ""y"": 0,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 12,
        ""y"": 0,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 0,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 3,
        ""y"": 0,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 2,
        ""y"": 0,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 1,
        ""y"": 0,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 1,
        ""y"": 0,
        ""z"": 5
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 1,
        ""y"": 0,
        ""z"": 4
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 1,
        ""y"": 0,
        ""z"": 3
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 1,
        ""y"": 0,
        ""z"": 2
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 0,
        ""z"": 5
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 0,
        ""z"": 4
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 0,
        ""z"": 3
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 0,
        ""z"": 2
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 0,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 12,
        ""y"": 0,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 11,
        ""y"": 0,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 10,
        ""y"": 0,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 0,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 8,
        ""y"": 0,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 7,
        ""y"": 0,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 6,
        ""y"": 0,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 5,
        ""y"": 0,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 0,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 3,
        ""y"": 0,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 2,
        ""y"": 0,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 1,
        ""y"": 0,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 10,
        ""y"": 0,
        ""z"": 11
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 11,
        ""y"": 0,
        ""z"": 11
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 12,
        ""y"": 0,
        ""z"": 11
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 0,
        ""z"": 11
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 10,
        ""y"": 0,
        ""z"": 12
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 11,
        ""y"": 0,
        ""z"": 12
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 12,
        ""y"": 0,
        ""z"": 12
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 0,
        ""z"": 12
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 10,
        ""y"": 0,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 11,
        ""y"": 0,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 12,
        ""y"": 0,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 0,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 5,
        ""y"": 0,
        ""z"": 11
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 5,
        ""y"": 0,
        ""z"": 12
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 6,
        ""y"": 0,
        ""z"": 12
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 7,
        ""y"": 0,
        ""z"": 12
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 8,
        ""y"": 0,
        ""z"": 12
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 0,
        ""z"": 12
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 5,
        ""y"": 0,
        ""z"": 9
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 5,
        ""y"": 0,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 5,
        ""y"": 0,
        ""z"": 7
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 5,
        ""y"": 0,
        ""z"": 8
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 6,
        ""y"": 0,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 6,
        ""y"": 0,
        ""z"": 7
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 6,
        ""y"": 0,
        ""z"": 8
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 6,
        ""y"": 0,
        ""z"": 9
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 7,
        ""y"": 0,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 7,
        ""y"": 0,
        ""z"": 7
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 7,
        ""y"": 0,
        ""z"": 8
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 7,
        ""y"": 0,
        ""z"": 9
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 8,
        ""y"": 0,
        ""z"": 7
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 8,
        ""y"": 0,
        ""z"": 8
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 8,
        ""y"": 0,
        ""z"": 9
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 8,
        ""y"": 0,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 2,
        ""y"": 0,
        ""z"": 2
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 2,
        ""y"": 0,
        ""z"": 3
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 2,
        ""y"": 0,
        ""z"": 4
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 2,
        ""y"": 0,
        ""z"": 5
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 3,
        ""y"": 0,
        ""z"": 2
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 0,
        ""z"": 2
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 5,
        ""y"": 0,
        ""z"": 2
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 6,
        ""y"": 0,
        ""z"": 2
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 7,
        ""y"": 0,
        ""z"": 2
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 8,
        ""y"": 0,
        ""z"": 2
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 0,
        ""z"": 2
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 10,
        ""y"": 0,
        ""z"": 2
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 11,
        ""y"": 0,
        ""z"": 2
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 12,
        ""y"": 0,
        ""z"": 2
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 12,
        ""y"": 0,
        ""z"": 5
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 12,
        ""y"": 0,
        ""z"": 3
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 12,
        ""y"": 0,
        ""z"": 4
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 11,
        ""y"": 0,
        ""z"": 3
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 11,
        ""y"": 0,
        ""z"": 4
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 11,
        ""y"": 0,
        ""z"": 5
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 3,
        ""y"": 0,
        ""z"": 3
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 0,
        ""z"": 3
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 5,
        ""y"": 0,
        ""z"": 3
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 6,
        ""y"": 0,
        ""z"": 3
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 7,
        ""y"": 0,
        ""z"": 3
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 8,
        ""y"": 0,
        ""z"": 3
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 0,
        ""z"": 3
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 10,
        ""y"": 0,
        ""z"": 3
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 3,
        ""y"": 0,
        ""z"": 4
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 3,
        ""y"": 0,
        ""z"": 5
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 0,
        ""z"": 4
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 0,
        ""z"": 5
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 5,
        ""y"": 0,
        ""z"": 4
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 5,
        ""y"": 0,
        ""z"": 5
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 6,
        ""y"": 0,
        ""z"": 4
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 6,
        ""y"": 0,
        ""z"": 5
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 6,
        ""y"": 0,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 7,
        ""y"": 0,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 7,
        ""y"": 0,
        ""z"": 4
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 7,
        ""y"": 0,
        ""z"": 5
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 0,
        ""z"": 4
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 8,
        ""y"": 0,
        ""z"": 4
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 8,
        ""y"": 0,
        ""z"": 5
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 0,
        ""z"": 5
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 10,
        ""y"": 0,
        ""z"": 5
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 10,
        ""y"": 0,
        ""z"": 4
      },
      ""type"": ""voxel"",
      ""color"": ""#8B572A""
    },
    {
      ""position"": {
        ""x"": 14,
        ""y"": 1,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 14,
        ""y"": 1,
        ""z"": 11
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 14,
        ""y"": 1,
        ""z"": 12
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 14,
        ""y"": 1,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 14,
        ""y"": 1,
        ""z"": 14
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 1,
        ""z"": 14
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 10,
        ""y"": 1,
        ""z"": 14
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 11,
        ""y"": 1,
        ""z"": 14
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 12,
        ""y"": 1,
        ""z"": 14
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 1,
        ""z"": 14
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 1,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 7,
        ""y"": 1,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 8,
        ""y"": 1,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 1,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 5,
        ""y"": 1,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 6,
        ""y"": 1,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 1,
        ""y"": 1,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 1,
        ""y"": 1,
        ""z"": 2
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 1,
        ""y"": 1,
        ""z"": 3
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 1,
        ""y"": 1,
        ""z"": 4
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 1,
        ""y"": 1,
        ""z"": 5
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 1,
        ""y"": 1,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 2,
        ""y"": 1,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 3,
        ""y"": 1,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 1,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 5,
        ""y"": 1,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 1,
        ""z"": 7
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 1,
        ""z"": 8
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 1,
        ""z"": 9
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 1,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 1,
        ""z"": 11
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 1,
        ""z"": 12
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 6,
        ""y"": 1,
        ""z"": 11
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 7,
        ""y"": 1,
        ""z"": 11
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 8,
        ""y"": 1,
        ""z"": 11
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 1,
        ""z"": 11
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 1,
        ""z"": 7
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 1,
        ""z"": 8
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 1,
        ""z"": 9
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 1,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 10,
        ""y"": 1,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 11,
        ""y"": 1,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 12,
        ""y"": 1,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 1,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 8,
        ""y"": 1,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 1,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 10,
        ""y"": 1,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 11,
        ""y"": 1,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 12,
        ""y"": 1,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 1,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 1,
        ""z"": 5
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 1,
        ""z"": 4
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 1,
        ""z"": 3
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 1,
        ""z"": 2
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 1,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 2,
        ""y"": 1,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 3,
        ""y"": 1,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 1,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 5,
        ""y"": 1,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 6,
        ""y"": 1,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 7,
        ""y"": 1,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 8,
        ""y"": 1,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 1,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 10,
        ""y"": 1,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 11,
        ""y"": 1,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 12,
        ""y"": 1,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 14,
        ""y"": 2,
        ""z"": 14
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 14,
        ""y"": 2,
        ""z"": 12
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 14,
        ""y"": 2,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 6,
        ""y"": 2,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 2,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 2,
        ""z"": 11
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 2,
        ""z"": 9
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 4,
        ""y"": 2,
        ""z"": 7
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 3,
        ""y"": 2,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 1,
        ""y"": 2,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 1,
        ""y"": 2,
        ""z"": 3
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 1,
        ""y"": 2,
        ""z"": 4
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 1,
        ""y"": 2,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 2,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 11,
        ""y"": 2,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 2,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 3,
        ""y"": 2,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 5,
        ""y"": 2,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 7,
        ""y"": 2,
        ""z"": 1
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 2,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 2,
        ""z"": 4
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 13,
        ""y"": 2,
        ""z"": 3
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 11,
        ""y"": 2,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 2,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 5,
        ""y"": 2,
        ""z"": 6
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 2,
        ""z"": 8
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 2,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 12,
        ""y"": 2,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 11,
        ""y"": 2,
        ""z"": 10
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 11,
        ""y"": 2,
        ""z"": 14
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 12,
        ""y"": 2,
        ""z"": 14
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 9,
        ""y"": 2,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    },
    {
      ""position"": {
        ""x"": 7,
        ""y"": 2,
        ""z"": 13
      },
      ""type"": ""voxel"",
      ""color"": ""#B8B8B8""
    }
  ]
}";

	//GridItem is serializable to make it JSON friendly.
	//GridItems represent individual pieces to place on the board.
	[Serializable]
	public class GridItem
	{
		//All values for this class are default values.
		public string type = null; //The type of the piece. Could be "character", "tile", or "npc".

		//Vector3 position coordinates, and Vector4 color values.
		public Vector3 position = new Vector3 (0f, 0f, 0f);
		public string color = "FFFFFF";
	}

	//MapItem is serializable to make it JSON friendly.
	//MapItem contains information about the map and an array of GridItems.
	[Serializable]
	public class MapItem
	{
		public int width = 1;
		public int height = 1;
		public int depth = 1;

		public string color = "#FFFFFF";

		public GridItem[] models = null;
	}

	// Use this for initialization
	void Start () {

		//Set anti-aliasing to highest value
		QualitySettings.antiAliasing = 2;

		//Find the Image Target
		imageTarget = GameObject.Find ("ImageTarget").GetComponent <ImageTargetBehaviour>();
		//anchorStage = GameObject.Find ("Ground Plane Stage").GetComponent <AnchorStageBehaviour> (); 

		buildChildren ();





		MapItem grid = JsonUtility.FromJson<MapItem> (JSONSTRING);
		//Vector3 gridVector = new Vector3 (-0.5f, 0, -0.5f);
		//GridMesh gridMaker = Instantiate (gridPrefab, gridVector, Quaternion.identity).GetComponent <GridMesh>();
		//gridMaker.transform.SetParent (gridLayout.transform);
		//gridMaker.setSize (grid.width);
		buildMap (grid);

	}
	
	// Update is called once per frame
	void Update () {
		
	}

	public void UpdateJSON (string JSONstring){
		Destroy (mapScaler);
		buildChildren ();
		MapItem map = JsonUtility.FromJson<MapItem> (JSONstring);
		buildMap (map);
	}

	void buildChildren ()
	{
		//Create an empty parent GameObject to control the scale of the entire layout.
		mapScaler = GameObject.Find ("MapScaler");
		if (mapScaler == null) {
			mapScaler = new GameObject ("MapScaler");
		}
		//Create an empty parent for the grid.
		gridLayout = GameObject.Find ("GridLayout");
		if (gridLayout == null) {
			gridLayout = new GameObject ("GridLayout");
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
				Vector3 tilesVector = new Vector3 (i, -1f, j);
				GameObject tile = Instantiate (tilePrefab, tilesVector, Quaternion.identity);
				tile.transform.SetParent (tileLayout.transform);
				fillColor (obj, tile);
			}
		}
		/*for (int k = 0; k <= height; k++) {
			if (k % gridHeightGap == 0) {
				Vector3 gridVector = new Vector3 (getGridSize (row) - 1, k - .52f, getGridSize (col) - 1);
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

		Vector3 position = new Vector3 ((mapScaler.transform.position.x - (obj.width / 2))*.1f, mapScaler.transform.position.y*.1f, (mapScaler.transform.position.z - (obj.depth / 2))*.1f);
		mapScaler.transform.Translate (position);
		StartCoroutine (scaleMap ());
		mapScaler.transform.SetParent (imageTarget.transform);

	}

	IEnumerator scaleMap(){
		yield return new WaitForSeconds (0.1f);
		mapScaler.transform.localScale = new Vector3 (0.1f, 0.1f, 0.1f);
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
			Color color;
			if (ColorUtility.TryParseHtmlString (piece.color, out color)) {
				rend.material.color = color;
			}
		}
	}

	static void fillColor (MapItem piece, GameObject obj)
	{
		MeshRenderer[] meshes = obj.GetComponentsInChildren<MeshRenderer> ();
		//Gets the child objects of the prefab by finding their MeshRenderer.
		//Foreach loop colors the tiles with the appropriate color.
		foreach (MeshRenderer mesh in meshes) {
			Renderer rend = mesh.GetComponent<Renderer> ();
			Color color;
			if (ColorUtility.TryParseHtmlString (piece.color, out color)) {
				rend.material.color = color;
			}
		}
	}

	float getGridSize (int n){
		return (n + 1) / 2f;
	}
}