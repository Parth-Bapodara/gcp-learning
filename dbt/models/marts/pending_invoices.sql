SELECT
  invoice_id,
  customer_name,
  store_name,
  invoice_date,
  item_name,
  total_amount,
  payment_method,
  city
FROM {{ ref('stg_invoices') }}
WHERE payment_status = 'Pending'
