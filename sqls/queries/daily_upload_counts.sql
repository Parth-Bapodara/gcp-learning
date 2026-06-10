select
  publish_date as upload_date,
  count(*) as total_uploads
from `yt-analytics-123.yt_dataset.youtube_videos`
group by upload_date
order by total_uploads desc;