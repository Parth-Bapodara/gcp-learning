import functions_framework

from cloud_functions.bucket_notifications import handle_bucket_notification


@functions_framework.http
def handle_event(request):
    envelope = request.get_json(silent=True)

    print("Cloud Run received request")
    print(f"Request JSON: {envelope}")

    if not envelope or "message" not in envelope:
        return "No Pub/Sub message found", 400

    return handle_bucket_notification(envelope["message"])
