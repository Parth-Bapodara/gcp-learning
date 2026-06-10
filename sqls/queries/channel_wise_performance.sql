SELECT
  channel_title,
  COUNT(*) as total_videos,
  SUM(views) as total_views,
  AVG(views) as avg_views
FROM `yt-analytics-123.yt_dataset.youtube_videos`
GROUP BY channel_title
ORDER BY total_views desc;