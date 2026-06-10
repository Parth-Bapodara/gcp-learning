SELECT publish_country, COUNT(*) AS trending_videos
FROM `yt-analytics-123.yt_dataset.youtube_videos`
GROUP BY publish_country
ORDER BY trending_videos DESC;