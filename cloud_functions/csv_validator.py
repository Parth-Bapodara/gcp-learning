import csv
import io

from google.cloud import storage

REQUIRED_COLUMNS = [
    "invoice_id",
    "customer_id",
    "customer_name",
    "store_name",
    "invoice_date",
    "item_name",
    "category",
    "quantity",
    "unit_price",
    "total_amount",
    "payment_method",
    "payment_status",
    "city",
]


class CSVValidationError(Exception):
    """Raised when an invoice CSV fails ETL validation."""


def validate_invoice_csv(bucket_name, file_name):
    """Validate CSV structure before loading into BigQuery (ETL transform step)."""
    client = storage.Client()
    blob = client.bucket(bucket_name).blob(file_name)
    content = blob.download_as_text(encoding="utf-8")

    reader = csv.reader(io.StringIO(content))

    try:
        header = next(reader)
    except StopIteration as error:
        raise CSVValidationError("CSV file is empty") from error

    header = [column.strip() for column in header]
    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in header
    ]
    if missing_columns:
        raise CSVValidationError(
            f"Missing required columns: {', '.join(missing_columns)}"
        )

    row_count = sum(1 for _ in reader)
    if row_count == 0:
        raise CSVValidationError("CSV file has no data rows")

    print(f"CSV validation passed: {row_count} rows, columns OK")
    return row_count
