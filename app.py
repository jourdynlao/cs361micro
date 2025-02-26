from flask import Flask, request, jsonify
import json
import os
from datetime import datetime, timezone

app = Flask(__name__)

DATA_FILE = 'metadata.json'

# ====================================================
# 1. Data Persistence with a JSON File
# ====================================================
# Check if the data store (metadata.json) exists.
# If it exists, load its contents into the metadata_records dictionary.
# Otherwise, initialize metadata_records as an empty dictionary.
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        metadata_records = json.load(f)
else:
    metadata_records = {}

# Helper function to save the current state of metadata_records to metadata.json.
def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(metadata_records, f)

# ====================================================
# 2. Creating a New Record (POST /indexRecord)
# ====================================================
# This endpoint accepts a POST request to create a new record.
# It validates the input, checks for duplicates, creates the record,
# saves it to the JSON file, and returns a success response.
@app.route('/indexRecord', methods=['POST'])
def index_record():
    data = request.get_json()
    # Validate that required fields are present in the JSON payload.
    if not data or 'recordID' not in data or 'type' not in data or 'attributes' not in data or 'owner' not in data:
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

    recordID = data['recordID']
    # Check for duplicate recordID.
    if recordID in metadata_records:
        return jsonify({'status': 'error', 'message': 'Record already exists'}), 409

    # Create a new record with provided data; generate a timestamp if not provided.
    record = {
        'type': data['type'],
        'attributes': data['attributes'],
        'owner': data['owner'],
        'timestamp': data.get('timestamp', datetime.now(timezone.utc).isoformat())
    }
    # Add the new record to the in-memory data store.
    metadata_records[recordID] = record
    # Persist the updated data store to metadata.json.
    save_data()
    return jsonify({'status': 'success', 'recordID': recordID}), 201

# ====================================================
# 3. Updating an Existing Record (PUT /indexRecord)
# ====================================================
# This endpoint accepts a PUT request to update an existing record.
# It verifies the record exists, validates input, updates the record,
# saves the changes, and returns a success response.
@app.route('/indexRecord', methods=['PUT'])
def update_record():
    data = request.get_json()
    # Check that a recordID is provided.
    if not data or 'recordID' not in data:
        return jsonify({'status': 'error', 'message': 'Missing recordID'}), 400

    recordID = data['recordID']
    # Ensure the record exists before updating.
    if recordID not in metadata_records:
        return jsonify({'status': 'error', 'message': 'Record not found'}), 404

    # Validate that all required fields for update are present.
    if 'type' not in data or 'attributes' not in data or 'owner' not in data:
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

    # Update the record with new data, including a new timestamp if not provided.
    record = {
        'type': data['type'],
        'attributes': data['attributes'],
        'owner': data['owner'],
        'timestamp': data.get('timestamp', datetime.now(timezone.utc).isoformat())
    }
    metadata_records[recordID] = record

    # Save the updated record to metadata.json.
    save_data()
    return jsonify({'status': 'success', 'recordID': recordID}), 200

# ====================================================
# 4. Querying Records (GET /query)
# ====================================================
# This endpoint handles GET requests to search for records based on query parameters.
# It extracts filters from the URL, iterates through metadata_records,
# and returns any records that match all provided filters.
@app.route('/query', methods=['GET'])
def query_records():
    filters = request.args.to_dict()  # Get query parameters as a dictionary.
    results = []
    # Loop through each record in metadata_records.
    for recordID, record in metadata_records.items():
        match = True
        # Check each filter against the record.
        for key, value in filters.items():
            if key == 'type':
                if record['type'] != value:
                    match = False
                    break
            elif key == 'owner':
                if record['owner'] != value:
                    match = False
                    break
            elif key in record['attributes']:
                if str(record['attributes'][key]) != value:
                    match = False
                    break
            else:
                match = False
                break
        # If the record matches all filters, include it in the results.
        if match:
            results.append({'recordID': recordID, **record})
    return jsonify({'status': 'success', 'results': results}), 200

# ====================================================
# 5. Starting the Flask Server
# ====================================================
# The application starts here when the script is executed directly.
# Flask runs in debug mode and listens for incoming HTTP requests on port 5000.
if __name__ == '__main__':
    app.run(debug=True)