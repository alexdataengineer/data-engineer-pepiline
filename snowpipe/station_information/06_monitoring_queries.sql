-- =====================================================
-- Queries de Monitoramento do Snowpipe
-- =====================================================

-- 1. Verificar status do Snowpipe
SELECT 
    PIPE_NAME,
    PIPE_SCHEMA,
    PIPE_OWNER,
    PIPE_STATE,
    CREATED,
    LAST_ALTERED
FROM INFORMATION_SCHEMA.PIPES 
WHERE PIPE_SCHEMA = 'AZURE_SYNAPSE' 
AND PIPE_NAME = 'STATION_INFORMATION_PIPE';

-- 2. Verificar execuções recentes do Snowpipe
SELECT 
    PIPE_NAME,
    START_TIME,
    END_TIME,
    ROWS_INSERTED,
    ROWS_PARSED,
    ROWS_LOADED,
    BYTES_LOADED,
    STATUS
FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => '_STATION_RAW_JSON',
    START_TIME => DATEADD('hours', -24, CURRENT_TIMESTAMP())
))
WHERE PIPE_NAME = 'STATION_INFORMATION_PIPE'
ORDER BY START_TIME DESC;

-- 3. Verificar status das Tasks
SELECT 
    TASK_NAME,
    TASK_SCHEMA,
    TASK_STATE,
    SCHEDULE,
    WAREHOUSE_NAME,
    LAST_SCHEDULED_TIME,
    LAST_COMPLETED_TIME,
    NEXT_SCHEDULED_TIME
FROM INFORMATION_SCHEMA.TASKS 
WHERE TASK_SCHEMA = 'AZURE_SYNAPSE';

-- 4. Verificar dados na tabela raw
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT file_name) as total_files,
    MAX(load_timestamp) as last_load
FROM STANGING.AZURE_SYNAPSE._STATION_RAW_JSON;

-- 5. Verificar dados na tabela final
SELECT 
    COUNT(*) as total_stations,
    COUNT(DISTINCT station_id) as unique_stations,
    MAX(load_timestamp) as last_update
FROM STANGING.AZURE_SYNAPSE.STATION_INFORMATION;

-- 6. Verificar erros recentes
SELECT 
    PIPE_NAME,
    START_TIME,
    STATUS,
    ERROR_MESSAGE
FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => '_STATION_RAW_JSON',
    START_TIME => DATEADD('hours', -24, CURRENT_TIMESTAMP())
))
WHERE STATUS = 'FAILED'
ORDER BY START_TIME DESC; 