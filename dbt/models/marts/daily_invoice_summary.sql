SELECT
  invoice_date,
  COUNT(*) AS invoice_count,
  SUM(total_amount) AS total_revenue,
  COUNTIF(payment_status = 'Pending') AS pending_invoice_count,
  SUM(IF(payment_status = 'Pending', total_amount, 0)) AS pending_amount
FROM {{ ref('stg_invoices') }}
GROUP BY invoice_date
