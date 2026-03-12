{{ config(materialized='table') }}

SELECT
    store_name,
    ROUND(SUM(value), 2)        AS total_value,
    ROUND(SUM(royalty), 2)      AS total_royalty,
    ROUND(SUM(royalty) / NULLIF(SUM(value), 0) * 100, 2) AS royalty_rate_pct,
    COUNT(DISTINCT isrc)        AS unique_tracks,
    COUNT(DISTINCT label_name)  AS unique_labels,
    SUM(qty)                    AS total_qty
FROM {{ ref('stg_royalty_transactions') }}
GROUP BY 1
ORDER BY total_value DESC