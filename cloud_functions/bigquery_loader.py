from datetime import datetime, timezone

from google.api_core.exceptions import NotFound
from google.cloud import bigquery

from cloud_functions.csv_validator import CSVValidationError, validate_invoice_csv

PROJECT_ID = "gcp-invoice-pipeline-499805"
DATASET_ID = "invoice_analytics"
TABLE_ID = "raw_invoices"
PROCESSED_FILES_TABLE = "processed_files"


def _get_table_ref(table_id):
    return f"{PROJECT_ID}.{DATASET_ID}.{table_id}"


def _ensure_processed_files_table(client):
    table_ref = _get_table_ref(PROCESSED_FILES_TABLE)
    try:
        client.get_table(table_ref)
    except NotFound:
        schema = [
            bigquery.SchemaField("bucket_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("file_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("processed_at", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("row_count", "INT64"),
            bigquery.SchemaField("status", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("error_message", "STRING"),
        ]
        client.create_table(bigquery.Table(table_ref, schema=schema))
        print(f"Created table {table_ref}")


def is_file_already_processed(client, bucket_name, file_name):
    _ensure_processed_files_table(client)

    query = f"""
        SELECT 1
        FROM `{_get_table_ref(PROCESSED_FILES_TABLE)}`
        WHERE bucket_name = @bucket_name
          AND file_name = @file_name
          AND status = 'success'
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("bucket_name", "STRING", bucket_name),
            bigquery.ScalarQueryParameter("file_name", "STRING", file_name),
        ]
    )
    return len(list(client.query(query, job_config=job_config).result())) > 0


def record_processed_file(client, bucket_name, file_name, status, row_count=None, error_message=None):
    _ensure_processed_files_table(client)

    rows = [{
        "bucket_name": bucket_name,
        "file_name": file_name,
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "row_count": row_count,
        "status": status,
        "error_message": error_message,
    }]
    errors = client.insert_rows_json(_get_table_ref(PROCESSED_FILES_TABLE), rows)
    if errors:
        print(f"Failed to record file metadata: {errors}")


def load_csv_to_bigquery(bucket_name, file_name):
    """Load a CSV file from Cloud Storage into BigQuery."""
    client = bigquery.Client()

    if is_file_already_processed(client, bucket_name, file_name):
        print(f"Skipping duplicate file: gs://{bucket_name}/{file_name}")
        return {"status": "duplicate", "rows_loaded": 0}

    try:
        validate_invoice_csv(bucket_name, file_name)
    except CSVValidationError as error:
        print(f"CSV validation failed: {error}")
        record_processed_file(
            client,
            bucket_name,
            file_name,
            status="failed",
            error_message=str(error),
        )
        return {"status": "invalid", "rows_loaded": 0, "error": str(error)}

    table_ref = _get_table_ref(TABLE_ID)
    uri = f"gs://{bucket_name}/{file_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    print(f"Loading {uri} into {table_ref}")

    try:
        load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)
        load_job.result()
        rows_loaded = load_job.output_rows

        record_processed_file(
            client,
            bucket_name,
            file_name,
            status="success",
            row_count=rows_loaded,
        )

        print(f"Loaded {rows_loaded} rows into {table_ref}")
        return {"status": "success", "rows_loaded": rows_loaded}

    except Exception as error:
        print(f"BigQuery load failed for {uri}: {error}")
        record_processed_file(
            client,
            bucket_name,
            file_name,
            status="failed",
            error_message=str(error),
        )
        raise
