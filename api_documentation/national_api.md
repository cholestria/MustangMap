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
    **Content:** `{ Name : "Nationwide" }`

* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "User doesn't exist" }`

  OR

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "You are unauthorized to make this request." }`

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