{{
  config(
    materialized='table',
    schema='GOLD'
  )
}}

-- Gold layer: Business analytics and KPIs
-- This model provides aggregated metrics for business intelligence

WITH station_metrics AS (
    SELECT
        region_id,
        geographic_area,
        station_size_category,
        station_type,
        COUNT(*) as total_stations,
        AVG(capacity) as avg_capacity,
        SUM(capacity) as total_capacity,
        COUNT(CASE WHEN has_kiosk = TRUE THEN 1 END) as stations_with_kiosk,
        COUNT(CASE WHEN electric_bike_surcharge_waiver = TRUE THEN 1 END) as stations_with_electric_waiver,
        COUNT(CASE WHEN eightd_has_key_dispenser = TRUE THEN 1 END) as stations_with_key_dispenser,
        AVG(data_quality_score) as avg_data_quality,
        MIN(lat) as min_latitude,
        MAX(lat) as max_latitude,
        MIN(lon) as min_longitude,
        MAX(lon) as max_longitude,
        CURRENT_TIMESTAMP() as metrics_calculated_at
    FROM {{ ref('stations_silver') }}
    GROUP BY region_id, geographic_area, station_size_category, station_type
),

overall_metrics AS (
    SELECT
        'Overall' as metric_category,
        COUNT(*) as total_stations,
        AVG(capacity) as avg_capacity,
        SUM(capacity) as total_capacity,
        COUNT(CASE WHEN has_kiosk = TRUE THEN 1 END) as stations_with_kiosk,
        COUNT(CASE WHEN electric_bike_surcharge_waiver = TRUE THEN 1 END) as stations_with_electric_waiver,
        COUNT(CASE WHEN eightd_has_key_dispenser = TRUE THEN 1 END) as stations_with_key_dispenser,
        AVG(data_quality_score) as avg_data_quality,
        CURRENT_TIMESTAMP() as metrics_calculated_at
    FROM {{ ref('stations_silver') }}
),

geographic_summary AS (
    SELECT
        geographic_area,
        COUNT(*) as station_count,
        AVG(capacity) as avg_capacity,
        SUM(capacity) as total_capacity,
        ROUND(COUNT(CASE WHEN has_kiosk = TRUE THEN 1 END) * 100.0 / COUNT(*), 2) as kiosk_percentage,
        ROUND(COUNT(CASE WHEN electric_bike_surcharge_waiver = TRUE THEN 1 END) * 100.0 / COUNT(*), 2) as electric_waiver_percentage,
        AVG(data_quality_score) as avg_data_quality,
        CURRENT_TIMESTAMP() as metrics_calculated_at
    FROM {{ ref('stations_silver') }}
    GROUP BY geographic_area
),

station_type_summary AS (
    SELECT
        station_type,
        COUNT(*) as station_count,
        AVG(capacity) as avg_capacity,
        SUM(capacity) as total_capacity,
        ROUND(COUNT(CASE WHEN has_kiosk = TRUE THEN 1 END) * 100.0 / COUNT(*), 2) as kiosk_percentage,
        ROUND(COUNT(CASE WHEN electric_bike_surcharge_waiver = TRUE THEN 1 END) * 100.0 / COUNT(*), 2) as electric_waiver_percentage,
        AVG(data_quality_score) as avg_data_quality,
        CURRENT_TIMESTAMP() as metrics_calculated_at
    FROM {{ ref('stations_silver') }}
    GROUP BY station_type
)

-- Final analytics table
SELECT
    'station_analytics' as table_name,
    'gold' as data_layer,
    station_id,
    station_name,
    region_id,
    geographic_area,
    station_size_category,
    station_type,
    capacity,
    has_kiosk,
    electric_bike_surcharge_waiver,
    eightd_has_key_dispenser,
    data_quality_score,
    lat,
    lon,
    load_timestamp,
    CURRENT_TIMESTAMP() as analytics_generated_at
FROM {{ ref('stations_silver') }}

UNION ALL

-- Add summary metrics
SELECT
    'overall_metrics' as table_name,
    'gold' as data_layer,
    NULL as station_id,
    metric_category as station_name,
    NULL as region_id,
    NULL as geographic_area,
    NULL as station_size_category,
    NULL as station_type,
    total_capacity as capacity,
    NULL as has_kiosk,
    NULL as electric_bike_surcharge_waiver,
    NULL as eightd_has_key_dispenser,
    avg_data_quality as data_quality_score,
    NULL as lat,
    NULL as lon,
    metrics_calculated_at as load_timestamp,
    CURRENT_TIMESTAMP() as analytics_generated_at
FROM overall_metrics 