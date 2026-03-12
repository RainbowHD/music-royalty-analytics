{{ config(materialized='view') }}

WITH source AS (
    SELECT * FROM {{ source('raw', 'royalty_transactions') }}
),

cleaned AS (
    SELECT
        UPPER(TRIM(ISRC))           AS isrc,
        TRIM(EAN)                   AS ean,
        TRIM(TRACK_REF)             AS track_ref,
        TRIM(LABEL_NAME)            AS label_name,
        TRIM(CATALOG)               AS catalog,
        TRIM(RELEASE_ARTIST)        AS release_artist,
        TRIM(RELEASE_NAME)          AS release_name,
        TRIM(TRACK_ARTIST)          AS track_artist,
        TRIM(TRACK_TITLE)           AS track_title,
        TRIM(MIX_NAME)              AS mix_name,
        TRIM(STORE_NAME)            AS store_name,
        TRIM(FORMAT)                AS format,
        TRIM(SALE_TYPE)             AS sale_type,
        TRIM(DEAL)                  AS deal,
        QTY::NUMBER                 AS qty,
        VALUE::FLOAT                AS value,
        ROYALTY::FLOAT              AS royalty,
        CASE
            WHEN VALUE > 0
            THEN ROUND(ROYALTY / VALUE * 100, 4)
            ELSE NULL
        END                         AS royalty_rate_pct,
        _LOADED_AT,
        _SOURCE_FILE
    FROM source
    WHERE VALUE IS NOT NULL
)

SELECT * FROM cleaned