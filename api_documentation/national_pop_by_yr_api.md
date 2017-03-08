**Show National Population Data**
----
  Returns json data with population compared across BLM states per year.

* **URL**

  /popbyyear

* **Method:**

  `GET`

*  **URL Params**

  None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{
    "2015": {
        "AZ": {
            "burro": 4860,
            "horse": 303
        },
        "CA": {
            "burro": 2946,
            "horse": 4395
        },
        "CO": {
            "burro": 0,
            "horse": 1415
        },
        "ID": {
            "burro": 0,
            "horse": 633
        },
        "MT": {
            "burro": 0,
            "horse": 172
        },
        "NM": {
            "burro": 0,
            "horse": 175
        },
        "NV": {
            "burro": 2611,
            "horse": 27599
        },
        "OR": {
            "burro": 49,
            "horse": 4327
        },
        "UT": {
            "burro": 355,
            "horse": 4550
        },
        "WY": {
            "burro": 0,
            "horse": 3760
        }
    },
    "2016": {
        "AZ": {
            "burro": 5317,
            "horse": 318
        },
        "CA": {
            "burro": 3391,
            "horse": 4925
        },
        "CO": {
            "burro": 0,
            "horse": 1530
        },
        "ID": {
            "burro": 0,
            "horse": 468
        },
        "MT": {
            "burro": 0,
            "horse": 160
        },
        "NM": {
            "burro": 0,
            "horse": 171
        },
        "NV": {
            "burro": 2552,
            "horse": 31979
        },
        "OR": {
            "burro": 56,
            "horse": 3785
        },
        "UT": {
            "burro": 400,
            "horse": 5440
        },
        "WY": {
            "burro": 0,
            "horse": 6214
        }
    }
}`

* **Error Response:**



* **Sample Call:**

  ```javascript
    $.ajax({
      url: "/popbyyear",
      dataType: "json",
      type : "GET",
      success : function(r) {
        console.log(r);
      }
    });
  ```