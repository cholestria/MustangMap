**Show National Data**
----
  Returns json data about all states in BLM Mustang Program.

* **URL**

  /totaldata

* **Method:**

  `GET`

*  **URL Params**

   **None:**

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{
    "AdoptData": {
        "2014": [
            1789,
            346,
            1689,
            168
        ],
        "2015": [
            2331,
            300,
            3093,
            726
        ]
    },
    "Footnotes": {
        "2000": "no burro removal data was reported for this year",
        "2012": "no burro removal data was reported for this year",
        "2013": "no burro removal data was reported for this year",
        "2014": "no burro removal data was reported for this year",
        "2015": "no burro removal data was reported for this year"
    },
    "Name": "Nationwide",
    "PopData": {
        "2015": [
            47329,
            10821,
            42403054,
            53813117
        ],
        "2016": [
            54990,
            11716,
            42403054,
            53813117
        ]
    }
}`

* **Error Response:**


* **Sample Call:**

  ```javascript
    $.ajax({
      url: "/totaldata",
      dataType: "json",
      type : "GET",
      success : function(r) {
        console.log(r);
      }
    });
  ```