{{ config(materialized='table') }}

SELECT
    COUNT(*)                                        AS total_rows,
    COUNT(isrc)                                     AS isrc_present,
    COUNT(*) - COUNT(isrc)                          AS isrc_missing,
    ROUND(COUNT(isrc) / COUNT(*) * 100, 1)          AS isrc_coverage_pct,
    COUNT(ean)                                      AS ean_present,
    ROUND(COUNT(ean) / COUNT(*) * 100, 1)           AS ean_coverage_pct,
    COUNT(CASE WHEN value <= 0 THEN 1 END)          AS zero_value_rows,
    COUNT(CASE WHEN royalty < 0 THEN 1 END)         AS negative_royalty_rows,
    COUNT(DISTINCT isrc)                            AS unique_isrcs,
    COUNT(DISTINCT store_name)                      AS unique_stores,
    COUNT(DISTINCT label_name)                      AS unique_labels
FROM {{ ref('stg_royalty_transactions') }}