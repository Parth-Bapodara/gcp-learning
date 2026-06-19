from google.cloud import bigquery

PROJECT_ID = "gcp-invoice-pipeline-499805"
DATASET_ID = "invoice_analytics"
TABLE_ID = "raw_invoices"


def load_csv_to_bigquery(bucket_name, file_name):
    """Load a CSV file from Cloud Storage into BigQuery."""
    client = bigquery.Client()

    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    uri = f"gs://{bucket_name}/{file_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    print(f"Loading {uri} into {table_ref}")

    load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)
    load_job.result()

    print(f"Loaded {load_job.output_rows} rows into {table_ref}")
    return load_job.output_rows
