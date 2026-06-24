import functions_framework

from cloud_functions.bucket_notifications import handle_bucket_notification
from cloud_functions.daily_summary import run_daily_summary


@functions_framework.http
def handle_event(request):
    request_json = request.get_json(silent=True)

    print("Cloud Run received request")

    if request_json and request_json.get("event_type") == "daily_summary":
        return run_daily_summary()

    print(f"Request JSON: {request_json}")

    if not request_json or "message" not in request_json:
        return "No Pub/Sub message found", 400

    return handle_bucket_notification(request_json["message"])
