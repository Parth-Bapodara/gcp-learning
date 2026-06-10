CREATE VIEW IF NOT EXISTS `yt-analytics-123.yt_dataset.view_channel_performance` AS
SELECT
    channel_title,
    COUNT(*) AS total_videos,
    SUM(views) AS total_views,
    AVG(views) AS avg_views
FROM `yt-analytics-123.yt_dataset.youtube_videos`
GROUP BY channel_title;