CREATE VIEW IF NOT EXISTS `gcp-invoice-pipeline-499805.invoice_analytics.vw_pending_invoices` AS
SELECT
  invoice_id,
  customer_name,
  store_name,
  invoice_date,
  item_name,
  total_amount,
  payment_method,
  city
FROM `gcp-invoice-pipeline-499805.invoice_analytics.raw_invoices`
WHERE payment_status = 'Pending'
ORDER BY invoice_date DESC, total_amount DESC;
