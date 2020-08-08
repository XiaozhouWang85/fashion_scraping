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
first_seen_ts,
latest_seen_ts,
TIMESTAMP_DIFF(latest_seen_ts,first_seen_ts,MINUTE) / (60 *24) AS days
FROM `{project}`.`{dataset}`.`{table}`
WHERE rank_rev=1