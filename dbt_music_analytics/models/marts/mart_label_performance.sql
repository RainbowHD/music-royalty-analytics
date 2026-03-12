{{ config(materialized='table') }}

SELECT
    label_name,
    COUNT(DISTINCT isrc)        AS catalog_size,
    COUNT(DISTINCT store_name)  AS stores_present,
    SUM(qty)                    AS total_streams,
    ROUND(SUM(value), 2)        AS total_revenue,
    ROUND(SUM(royalty), 2)      AS total_royalties,
    ROUND(SUM(royalty) / NULLIF(SUM(value), 0) * 100, 2) AS royalty_rate_pct,
    COUNT(*)                    AS transaction_count
FROM {{ ref('stg_royalty_transactions') }}
GROUP BY 1
ORDER BY total_royalties DESC