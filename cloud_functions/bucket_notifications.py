import base64
import json
import functions_framework


@functions_framework.cloud_event
def handle_bucket_event(cloud_event):
    pubsub_message = cloud_event.data.get("message", {})

    encoded_data = pubsub_message.get("data")
    attributes = pubsub_message.get("attributes", {})

    print("Pub/Sub message received")
    print(f"Attributes: {attributes}")

    if encoded_data:
        decoded_data = base64.b64decode(encoded_data).decode("utf-8")
        print(f"Decoded message: {decoded_data}")

        try:
            event_data = json.loads(decoded_data)

            bucket_name = event_data.get("bucket")
            file_name = event_data.get("name")
            content_type = event_data.get("contentType")

            print(f"Bucket: {bucket_name}")
            print(f"File: {file_name}")
            print(f"Content type: {content_type}")

            if file_name and file_name.endswith(".csv"):
                print("CSV file uploaded. Later we can process this file into BigQuery.")
            else:
                print("Non-CSV file event received.")

        except json.JSONDecodeError:
            print("Message is not valid JSON.")
    else:
        print("No message data found.")