SELECT title, ROUND((likes / views) * 100, 2) AS engagement_rate
FROM `yt-analytics-123.yt_dataset.youtube_videos`
WHERE views > 100000
ORDER BY engagement_rate DESC
LIMIT 20