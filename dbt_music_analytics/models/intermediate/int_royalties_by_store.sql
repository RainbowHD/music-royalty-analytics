{{ config(materialized='view') }}

SELECT
    store_name,
    format,
    sale_type,
    deal,
    COUNT(*)                                        AS transaction_count,
    SUM(qty)                                        AS total_qty,
    ROUND(SUM(value), 2)                            AS total_value,
    ROUND(SUM(royalty), 2)                          AS total_royalty,
    ROUND(AVG(royalty_rate_pct), 4)                 AS avg_royalty_rate_pct,
    COUNT(DISTINCT isrc)                            AS unique_tracks,
    COUNT(DISTINCT label_name)                      AS unique_labels
FROM {{ ref('stg_royalty_transactions') }}
GROUP BY 1, 2, 3, 4