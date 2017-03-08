**Show State Data**
----
  Returns json data about a single herd area.

* **URL**

  /hachartdata/herd_id

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `herd_id=[string]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{
    "Footnotes": {},
    "Name": "Palomino Buttes",
    "Pictures": {
        "f967e5da-8319-463c-852d-3faf0994f0b8.jpg": {
            "credit": "Richelle Ruhlin Wilson",
            "horse": "Aspen",
            "user": "Olivia Knott"
        }
    },
    "PopData": {
        "2015": [
            78,
            0,
            86191,
            98810
        ],
        "2016": [
            131,
            0,
            86191,
            98810
        ]
    }
}`

* **Error Response:**


* **Sample Call:**

  ```javascript
    $.ajax({
      url: "/hachartdata/OR0006",
      dataType: "json",
      type : "GET",
      success : function(r) {
        console.log(r);
      }
    });
  ```