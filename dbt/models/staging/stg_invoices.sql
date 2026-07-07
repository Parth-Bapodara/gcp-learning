SELECT
  TRIM(invoice_id) AS invoice_id,
  TRIM(customer_id) AS customer_id,
  TRIM(customer_name) AS customer_name,
  TRIM(store_name) AS store_name,
  SAFE_CAST(invoice_date AS DATE) AS invoice_date,
  TRIM(item_name) AS item_name,
  TRIM(category) AS category,
  SAFE_CAST(quantity AS INT64) AS quantity,
  SAFE_CAST(unit_price AS FLOAT64) AS unit_price,
  SAFE_CAST(total_amount AS FLOAT64) AS total_amount,
  TRIM(payment_method) AS payment_method,
  CASE
    WHEN LOWER(TRIM(payment_status)) = 'paid' THEN 'Paid'
    WHEN LOWER(TRIM(payment_status)) = 'pending' THEN 'Pending'
    ELSE 'Unknown'
  END AS payment_status,
  TRIM(city) AS city
FROM {{ source('invoice_analytics', 'raw_invoices') }}
WHERE TRIM(invoice_id) IS NOT NULL
  AND TRIM(invoice_id) != ''
