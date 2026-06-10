CREATE VIEW IF NOT EXISTS `yt-analytics-123.yt_dataset.view_top_videos` AS
SELECT
  video_id,
  title,
  channel_title,
  views
FROM `yt-analytics-123.yt_dataset.youtube_videos`
ORDER BY views DESC;