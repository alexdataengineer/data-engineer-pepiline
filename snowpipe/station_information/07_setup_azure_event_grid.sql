-- =====================================================
-- Configuração do Azure Event Grid com Snowpipe
-- =====================================================

-- 1. Obter a URL de notificação do Snowpipe
-- Execute esta query para obter a URL que será usada no Azure Event Grid
SELECT 
    PIPE_NAME,
    PIPE_SCHEMA,
    NOTIFICATION_CHANNEL_NAME
FROM INFORMATION_SCHEMA.PIPES 
WHERE PIPE_SCHEMA = 'AZURE_SYNAPSE' 
AND PIPE_NAME = 'STATION_INFORMATION_PIPE';

-- 2. Verificar se o pipe está ativo
SELECT SYSTEM$PIPE_STATUS('STANGING.AZURE_SYNAPSE.station_information_pipe');

-- 3. Forçar resumo do pipe se necessário
SELECT SYSTEM$PIPE_FORCE_RESUME('STANGING.AZURE_SYNAPSE.station_information_pipe');

-- 4. Verificar configurações do stage
DESC STAGE stage_json_station_information;

-- 5. Testar acesso ao stage
LIST @stage_json_station_information/gbfs/en/; 