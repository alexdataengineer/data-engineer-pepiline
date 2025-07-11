{{
  config(
    materialized='table',
    schema='BRONZE'
  )
}}

-- Bronze layer: Raw data with minimal transformations
-- This model takes data from the raw Snowflake table and applies basic cleaning

SELECT
    station_id,
    name,
    region_id,
    capacity,
    lat,
    lon,
    short_name,
    external_id,
    station_type,
    has_kiosk,
    electric_bike_surcharge_waiver,
    eightd_has_key_dispenser,
    rental_methods,
    rental_uris,
    eightd_station_services,
    load_timestamp,
    -- Add metadata columns
    CURRENT_TIMESTAMP() as dbt_loaded_at,
    'bronze' as data_layer
FROM {{ source('raw', 'station_information') }}
WHERE station_id IS NOT NULL  -- Basic data quality check
  AND name IS NOT NULL
  AND lat IS NOT NULL
  AND lon IS NOT NULL 