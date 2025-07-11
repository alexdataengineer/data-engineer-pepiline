-- =====================================================
-- Criação do Stream para detectar mudanças
-- =====================================================

-- Criar stream na tabela raw para detectar novos dados
CREATE OR REPLACE STREAM STANGING.AZURE_SYNAPSE.station_raw_stream
ON TABLE STANGING.AZURE_SYNAPSE._STATION_RAW_JSON;

-- Verificar o stream criado
SHOW STREAMS IN SCHEMA STANGING.AZURE_SYNAPSE; 