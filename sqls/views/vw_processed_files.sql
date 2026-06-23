CREATE VIEW IF NOT EXISTS `gcp-invoice-pipeline-499805.invoice_analytics.vw_processed_files` AS
SELECT
  bucket_name,
  file_name,
  processed_at,
  row_count,
  status,
  error_message
FROM `gcp-invoice-pipeline-499805.invoice_analytics.processed_files`
ORDER BY processed_at DESC;
