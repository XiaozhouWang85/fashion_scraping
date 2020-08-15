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
first_seen_ts,
episode_start_ts AS updated_ts,
sold_status OR days_since_seen>=1 AS sold_status
FROM `{project}`.`{dataset}`.`{table}`
WHERE rank_rev=1