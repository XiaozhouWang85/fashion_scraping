WITH assign_key AS (

  SELECT
  *,
  CONCAT(
      COALESCE(CAST(website AS STRING),""),
      COALESCE(CAST(brand AS STRING),""),
      COALESCE(CAST(img_src AS STRING),""),
      COALESCE(CAST(url AS STRING),""),
      COALESCE(CAST(title AS STRING),""),
      COALESCE(CAST(err AS STRING),""),
      COALESCE(CAST(curr AS STRING),""),
      COALESCE(CAST(curr_symbol AS STRING),""),
      COALESCE(CAST(cost AS STRING),""),
      COALESCE(CAST(price AS STRING),""),
      COALESCE(CAST(orig_price AS STRING),""),
      COALESCE(CAST(item_ID AS STRING),""),
      COALESCE(CAST(sold_status AS STRING),"")
  ) AS key

  FROM `{project}`.`{dataset}`.`{table}`
  
),

change_identified AS (

  SELECT 
  *,
  IF(key<>LAG(key) OVER(PARTITION BY item_ID ORDER BY insertion_timestamp),1,0) as change
  FROM assign_key

),

episode_identified AS (

  SELECT 
  *,
  SUM(change) OVER(item_part) + 1 AS episode,
  COALESCE(LEAD(insertion_timestamp) OVER(item_part),insertion_timestamp) AS lead_timestamp
  FROM change_identified 
  WINDOW item_part AS (
    PARTITION BY item_ID ORDER BY insertion_timestamp
  )
),

episodes_tagged AS (

  SELECT 
  *,
  ROW_NUMBER() OVER(episode_part_rev) AS episode_rank_rev,
  ROW_NUMBER() OVER(item_part_rev) AS rank_rev,
  MIN(insertion_timestamp) OVER(episode_part) AS episode_start_ts,
  MAX(lead_timestamp) OVER(episode_part) AS episode_end_ts,
  MIN(insertion_timestamp) OVER(item_part) AS first_seen_ts,
  MAX(insertion_timestamp) OVER(item_part) AS latest_seen_ts
  FROM episode_identified
  WINDOW episode_part_rev AS (
    PARTITION BY item_ID, episode ORDER BY insertion_timestamp DESC
  ),
  episode_part AS (
    PARTITION BY item_ID, episode ORDER BY insertion_timestamp 
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ),
  item_part_rev AS (
      PARTITION BY item_ID ORDER BY insertion_timestamp DESC
  ),
  item_part AS (
    PARTITION BY item_ID ORDER BY insertion_timestamp 
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  )
  
)

SELECT
website,
brand,
img_src,
url,
title,
err,
curr,
curr_symbol,
cost,
price,
orig_price,
item_ID,
sold_status,
episode,
episode_rank_rev,
rank_rev,
episode_start_ts,
episode_end_ts,
first_seen_ts,
latest_seen_ts
FROM episodes_tagged
WHERE episode_rank_rev=1