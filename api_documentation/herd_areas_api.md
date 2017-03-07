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
    **Content:** `{ id : "OR0006", Name : "Palomino Buttes" }`

* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "User doesn't exist" }`

  OR

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "You are unauthorized to make this request." }`

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