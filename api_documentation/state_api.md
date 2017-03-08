**Show State Data**
----
  Returns json data about a single state.

* **URL**

  /statedata/state_id

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `state_id=[string]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{
    "AdoptData": {
        "2014": [
            125,
            40,
            51,
            8
        ],
        "2015": [
            140,
            19,
            210,
            3
        ]
    },
    "Footnotes": {},
    "MapDict": {
        "latitude": 43.5,
        "longitude": -119.8,
        "map_names": [
            "/static/geodata/oregon_ha.geojson",
            "/static/geodata/oregon_hma.geojson"
        ],
        "name": "Oregon",
        "state_id": "OR",
        "zoom": 7
    },
    "Name": "Oregon",
    "PopData": {
        "2015": [
            4327,
            49,
            3608660,
            4312356
        ],
        "2016": [
            3785,
            56,
            3608660,
            4312356
        ]
    }
}`

* **Error Response:**


* **Sample Call:**

  ```javascript
    $.ajax({
      url: "/statedata/OR",
      dataType: "json",
      type : "GET",
      success : function(r) {
        console.log(r);
      }
    });
  ```