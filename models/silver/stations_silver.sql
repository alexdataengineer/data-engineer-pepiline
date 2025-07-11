{{
  config(
    materialized='table',
    schema='SILVER'
  )
}}

-- Silver layer: Cleaned and enriched data
-- This model applies business logic and data quality rules

WITH cleaned_stations AS (
    SELECT
        station_id,
        TRIM(name) as station_name,
        UPPER(region_id) as region_id,
        COALESCE(capacity, 0) as capacity,
        lat,
        lon,
        TRIM(short_name) as short_name,
        external_id,
        UPPER(station_type) as station_type,
        COALESCE(has_kiosk, FALSE) as has_kiosk,
        COALESCE(electric_bike_surcharge_waiver, FALSE) as electric_bike_surcharge_waiver,
        COALESCE(eightd_has_key_dispenser, FALSE) as eightd_has_key_dispenser,
        rental_methods,
        rental_uris,
        eightd_station_services,
        load_timestamp,
        dbt_loaded_at,
        data_layer
    FROM {{ ref('stations_bronze') }}
    WHERE station_id IS NOT NULL
      AND station_name IS NOT NULL
      AND lat BETWEEN -90 AND 90  -- Valid latitude
      AND lon BETWEEN -180 AND 180  -- Valid longitude
      AND capacity >= 0  -- Valid capacity
),

enriched_stations AS (
    SELECT
        *,
        -- Add calculated fields
        CASE 
            WHEN capacity > 20 THEN 'Large'
            WHEN capacity > 10 THEN 'Medium'
            ELSE 'Small'
        END as station_size_category,
        
        CASE 
            WHEN has_kiosk = TRUE THEN 'Yes'
            ELSE 'No'
        END as kiosk_available,
        
        CASE 
            WHEN electric_bike_surcharge_waiver = TRUE THEN 'Yes'
            ELSE 'No'
        END as electric_bike_waiver,
        
        -- Geographic categorization
        CASE 
            WHEN lat > 40.7 THEN 'Upper Manhattan'
            WHEN lat > 40.6 THEN 'Mid Manhattan'
            WHEN lat > 40.5 THEN 'Lower Manhattan'
            ELSE 'Other'
        END as geographic_area,
        
        -- Data quality score
        CASE 
            WHEN station_name IS NOT NULL 
                 AND lat IS NOT NULL 
                 AND lon IS NOT NULL 
                 AND capacity IS NOT NULL THEN 100
            WHEN station_name IS NOT NULL 
                 AND lat IS NOT NULL 
                 AND lon IS NOT NULL THEN 75
            WHEN station_name IS NOT NULL 
                 AND (lat IS NOT NULL OR lon IS NOT NULL) THEN 50
            ELSE 25
        END as data_quality_score
        
    FROM cleaned_stations
)

SELECT 
    station_id,
    station_name,
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
    station_size_category,
    kiosk_available,
    electric_bike_waiver,
    geographic_area,
    data_quality_score,
    load_timestamp,
    dbt_loaded_at,
    'silver' as data_layer
FROM enriched_stations 