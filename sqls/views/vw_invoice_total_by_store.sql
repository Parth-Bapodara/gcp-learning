CREATE VIEW IF NOT EXISTS `gcp-invoice-pipeline-499805.invoice_analytics.vw_total_amount_by_store` AS
SELECT
  store_name,
  COUNT(*) AS invoice_count,
  SUM(total_amount) AS total_revenue,
  ROUND(AVG(total_amount), 2) AS avg_invoice_amount
FROM `gcp-invoice-pipeline-499805.invoice_analytics.raw_invoices`
GROUP BY store_name
ORDER BY total_revenue DESC;
