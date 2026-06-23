CREATE VIEW IF NOT EXISTS `gcp-invoice-pipeline-499805.invoice_analytics.vw_daily_invoice_count_by_city` AS
SELECT
  invoice_date,
  city,
  COUNT(*) AS invoice_count,
  SUM(total_amount) AS daily_revenue
FROM `gcp-invoice-pipeline-499805.invoice_analytics.raw_invoices`
GROUP BY invoice_date, city
ORDER BY invoice_date DESC, invoice_count DESC;
