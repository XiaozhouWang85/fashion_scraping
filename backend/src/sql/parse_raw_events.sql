WITH raw_events AS (

    SELECT
    insertion_timestamp,
    website,
    JSON_EXTRACT_SCALAR(payload,"$.brand") AS brand,
    JSON_EXTRACT_SCALAR(payload,"$.img_src") AS img_src,
    JSON_EXTRACT_SCALAR(payload,"$.url") AS url,
    JSON_EXTRACT_SCALAR(payload,"$.title") AS title,
    JSON_EXTRACT_SCALAR(payload,"$.curr") AS curr,
    JSON_EXTRACT_SCALAR(payload,"$.cost") AS cost,
    JSON_EXTRACT_SCALAR(payload,"$.price") AS price,
    JSON_EXTRACT_SCALAR(payload,"$.orig_price") AS orig_price,
    JSON_EXTRACT_SCALAR(payload,"$.err") AS err,

    FROM `{project}`.`{dataset}`.`{table}`
  
),

parsed_data AS (

    SELECT 
    insertion_timestamp,
    website,
    brand,
    img_src,
    url,
    title,
    err,
    CASE 
        WHEN curr="USD" THEN "USD"
        WHEN curr="£" THEN "GBP"
        WHEN curr="€" THEN "EUR"
        WHEN curr="$" THEN "USD"
    END AS curr,
    CASE 
        WHEN curr="USD" THEN "$"
        WHEN curr="£" THEN "£"
        WHEN curr="€" THEN "€"
        WHEN curr="$" THEN "$"
    END AS curr_symbol,
    SAFE_CAST(REGEXP_REPLACE(cost,r"[\$\,]*","") AS FLOAT64) AS cost,
    SAFE_CAST(REGEXP_REPLACE(price,r"[\$\,]*","") AS FLOAT64) AS price,
    orig_price,
    CASE
        WHEN website = "yoogiscloset" 
          THEN CONCAT(
            "yoogiscloset-",
            REGEXP_EXTRACT(img_src,r"\/([0-9]*)_[0-9]")
          )
        WHEN website = "fashionphile" THEN CONCAT(
            "fashionphile-", 
            REGEXP_EXTRACT(url,r"-([0-9]*)$")
        )
        WHEN website = "hardlyeverwornit" THEN CONCAT(
            "hardlyeverwornit-", 
            REGEXP_EXTRACT(url,r"item\/([0-9]*)\/")  
        )
    END AS item_ID,
    REGEXP_CONTAINS(
    err,
    r"Sold") AS sold_status
    FROM raw_events
  
)

SELECT 
*
FROM parsed_data
