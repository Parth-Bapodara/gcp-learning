SELECT
  video_id,
  title,
  COUNT(DISTINCT trending_date) AS trending_days
FROM `yt-analytics-123.yt_dataset.youtube_videos`
GROUP BY video_id, title
HAVING trending_days > 1
ORDER BY trending_days DESC;