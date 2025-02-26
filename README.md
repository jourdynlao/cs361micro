# Microservice A: Metadata Indexing Service

This microservice manages metadata records, allowing creation, updating, and querying of records stored in a JSON file (`metadata.json`). It is implemented using Flask and communicates via a RESTful API.

# Table of Contents
- [Running the Microservice](#running-the-microservice)
- [Requesting Data from the Microservice](#requesting-data-from-the-microservice)
  - [Create a Record (POST /indexRecord)](#create-a-record-post-indexrecord)
  - [Update a Record (PUT /indexRecord)](#update-a-record-put-indexrecord)
  - [Query Records (GET /query)](#query-records-get-query)
- [Receiving Data from the Microservice](#receiving-data-from-the-microservice)
- [UML Sequence Diagram](#uml-sequence-diagram)

---

# Running the Microservice
To run the microservice locally:

1.  Clone the repository: git clone https://github.com/jourdynlao/cs361micro.git

3.	Install dependencies: pip install flask

4.	Run the microservice: python3 app.py

The microservice will be available at http://127.0.0.1:5000.

# Requesting Data from the Microservice

You can interact with the microservice by sending HTTP requests to its endpoints. Below are the details for each endpoint, including how to structure your requests and example calls.

## Create a Record (POST /indexRecord)

Purpose: Create a new metadata record.

HTTP Method: POST

Endpoint: /indexRecord

Request Body: JSON object with the following fields:

	•	recordID (string): Unique identifier for the record.
	•	type (string): Type of the record (e.g., “GameObject”).
	•	attributes (object): Key-value pairs of attributes (e.g., {"attack": 80, "defense": 60}).
	•	owner (string): Owner of the record.
	•	timestamp (string, optional): ISO 8601 timestamp (e.g., “2025-02-10T12:34:56Z”). If not provided, the current time is used.

Example Call (using Python requests):
```python
import requests
data = {
    "recordID": "REC12345",
    "type": "GameObject",
    "attributes": {"attack": 80, "defense": 60, "speed": 70},
    "owner": "Entity123"
}
response = requests.post('http://127.0.0.1:5000/indexRecord', json=data)
print(response.json())
```

## Update a Record (PUT /indexRecord)

Purpose: Update an existing metadata record.

HTTP Method: PUT

Endpoint: /indexRecord

Request Body: JSON object with the following fields:

	•	recordID (string): Unique identifier of the record to update.
	•	type (string): Updated type of the record.
	•	attributes (object): Updated key-value pairs of attributes.
	•	owner (string): Updated owner of the record.
	•	timestamp (string, optional): Updated ISO 8601 timestamp. If not provided, the current time is used.

Example Call (using Python requests):
```python
  import requests

  data = {

    "recordID": "REC12345",
    "type": "GameObject",
    "attributes": {"attack": 85, "defense": 65, "speed": 75},
    "owner": "Entity123"
  }
  response = requests.put('http://127.0.0.1:5000/indexRecord', json=data)
  print(response.json())
```

## Query Records (GET /query)

Purpose: Retrieve records that match the provided filters.

HTTP Method: GET

Endpoint: /query

Query Parameters: Filters for type, owner, or any attribute (e.g., type=GameObject&attack=80).

Example Call (using Python requests):
```python
import requests
params = {'type': 'GameObject', 'attack': '80'}
response = requests.get('http://127.0.0.1:5000/query', params=params)
print(response.json())
```

# Receiving Data from the Microservice

The microservice responds to requests with JSON data. Below is the structure of the responses for each endpoint.


### POST /indexRecord (Create Record):
	•	Success: {"status": "success", "recordID": "<recordID>"}
	•	Error: {"status": "error", "message": "<error message>"}

**Example POST Responses:**
```json
  {
    "status": "success",
    "recordID": "REC12345"
  }

  {
    "status": "error",
    "message": "Record already exists"
  }
```


### PUT /indexRecord (Update Record):

	•	Success: {"status": "success", "recordID": "<recordID>"}
	•	Error: {"status": "error", "message": "<error message>"}

**Example PUT Responses:**
```json
  {
    "status": "success",
    "recordID": "REC12345"
  }

  {
    "status": "error",
    "message": "Record not found"
  }
```
### GET /query (Query Records):
```
{
  "status": "success",
  "results": [
    {
      "recordID": "<recordID>",
      "type": "<type>",
      "attributes": {"<key>": <value>, ...},
      "owner": "<owner>",
      "timestamp": "<timestamp>"
    },
    ...
  ]
}
```


**Example GET Response:**
```
{
  "status": "success",
  "results": [
    {
      "recordID": "REC12345",
      "type": "GameObject",
      "attributes": {"attack": 80, "defense": 60, "speed": 70},
      "owner": "Entity123",
      "timestamp": "2025-02-10T12:34:56Z"
    }
  ]
}
```

**To receive and handle the response in your code:**

	•	Use the response.json() method in Python’s requests library to parse the JSON response.
	•	Check the "status" field to determine if the request was successful.
	•	For GET requests, the matching records are in the "results" array.

# UML Sequence Diagram

The UML sequence diagram below illustrates the communication flow between the client (your program), the indexing microservice, and the data store (metadata.json).



