from google.cloud import bigquery

from cloud_functions.bigquery_loader import DATASET_ID, PROJECT_ID


def get_daily_summary():
    client = bigquery.Client()
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.raw_invoices"

    summary_query = f"""
        SELECT
          COUNT(*) AS total_invoices,
          COUNTIF(payment_status = 'Pending') AS pending_count,
          SUM(IF(payment_status = 'Pending', total_amount, 0)) AS pending_amount,
          SUM(total_amount) AS total_revenue
        FROM `{table_ref}`
    """
    summary_row = list(client.query(summary_query).result())[0]

    store_query = f"""
        SELECT
          store_name,
          SUM(total_amount) AS store_revenue
        FROM `{table_ref}`
        GROUP BY store_name
        ORDER BY store_revenue DESC
        LIMIT 5
    """
    store_rows = list(client.query(store_query).result())

    return {
        "total_invoices": summary_row.total_invoices,
        "pending_count": summary_row.pending_count,
        "pending_amount": summary_row.pending_amount,
        "total_revenue": summary_row.total_revenue,
        "top_stores": [
            {"store_name": row.store_name, "store_revenue": row.store_revenue}
            for row in store_rows
        ],
    }


def run_daily_summary():
    try:
        summary = get_daily_summary()

        print("Daily invoice summary started")
        print(f"Total invoices: {summary['total_invoices']}")
        print(f"Pending invoices: {summary['pending_count']}")
        print(f"Pending amount: {summary['pending_amount']}")
        print(f"Total revenue: {summary['total_revenue']}")

        for store in summary["top_stores"]:
            print(
                f"Store: {store['store_name']} | "
                f"Revenue: {store['store_revenue']}"
            )

        print("Daily invoice summary completed")
        return "Daily summary logged", 200

    except Exception as error:
        print(f"Daily summary failed: {error}")
        return f"Daily summary failed: {error}", 500
