SELECT
  store_name,
  COUNT(*) AS invoice_count,
  SUM(total_amount) AS total_revenue,
  ROUND(AVG(total_amount), 2) AS avg_invoice_amount
FROM {{ ref('stg_invoices') }}
GROUP BY store_name
