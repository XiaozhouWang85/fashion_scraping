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
latest_seen_ts
FROM `{project}`.`{dataset}`.`{table}`
WHERE rank_rev=1 AND NOT(sold_status)