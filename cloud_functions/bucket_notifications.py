import base64
import json

from cloud_functions.bigquery_loader import load_csv_to_bigquery


def handle_bucket_notification(message):
    """Process a Pub/Sub push message coming from Cloud Storage bucket notifications."""
    attributes = message.get("attributes", {})
    event_type = attributes.get("eventType")

    encoded_data = message.get("data")
    if not encoded_data:
        return "No data in Pub/Sub message", 400

    try:
        decoded_data = base64.b64decode(encoded_data).decode("utf-8")
        event_data = json.loads(decoded_data)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"Failed to decode Pub/Sub message: {error}")
        return "Invalid Pub/Sub message", 400

    bucket_name = event_data.get("bucket")
    file_name = event_data.get("name")

    print(f"Bucket: {bucket_name}")
    print(f"File: {file_name}")
    print(f"Event type: {event_type}")

    if event_type != "OBJECT_FINALIZE":
        print(f"Skipping event type: {event_type}")
        return "Skipped non-upload event", 200

    if not file_name or not file_name.endswith(".csv"):
        print(f"Skipping non-CSV file: {file_name}")
        return "Skipped non-CSV file", 200

    print("CSV upload detected. Loading into BigQuery.")

    try:
        result = load_csv_to_bigquery(bucket_name, file_name)
    except Exception as error:
        print(f"Failed to process CSV upload: {error}")
        return f"Failed to load CSV into BigQuery: {error}", 500

    if result["status"] == "duplicate":
        return "File already processed", 200

    return f"Loaded {result['rows_loaded']} rows into BigQuery", 200
