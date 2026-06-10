SELECT
  category_id,
  AVG(views) as avg_views
FROM `yt-analytics-123.yt_dataset.youtube_videos`
GROUP BY category_id
ORDER BY avg_views DESC;