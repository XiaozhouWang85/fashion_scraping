SELECT
website,
brand,
img_src,
url,
title,
curr,
curr_symbol,
COALESCE(cost,price) AS price,
item_ID,
days_since_update,
days_since_update <= 1 AS last_1_day,
days_since_update <= 3 AS last_3_days,
days_since_update <= 7 AS last_7_days,
True AS all_time,
first_seen_ts,
episode_start_ts AS updated_ts,
days_since_seen,
sold_status OR days_since_seen>=1 AS sold_status
FROM `{project}`.`{dataset}`.`{table}`
WHERE rank_rev=1 AND item_ID IS NOT NULL