#!/usr/bin/env python3
"""
Script para gerar arquivos SQL dinamicamente
usando configurações de variáveis de ambiente
"""

import os
import re
from pathlib import Path

def load_env_file(env_file):
    """Carrega variáveis de um arquivo .env"""
    config = {}
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    return config

def replace_variables(content, config):
    """Substitui variáveis no conteúdo usando as configurações"""
    for key, value in config.items():
        placeholder = f'${{{key}}}'
        content = content.replace(placeholder, value)
    return content

def generate_sql_files():
    """Gera todos os arquivos SQL dinamicamente"""
    
    # Carregar configurações
    config = load_env_file('config.env')
    if not config:
        print("❌ Arquivo config.env não encontrado!")
        print("📝 Copie config.env.example para config.env e configure as variáveis")
        return False
    
    # Verificar se todas as variáveis necessárias estão presentes
    required_vars = [
        'SNOWFLAKE_USER', 'SNOWFLAKE_PASSWORD', 'SNOWFLAKE_ACCOUNT',
        'AZURE_STORAGE_ACCOUNT', 'AZURE_CONTAINER', 'AZURE_SAS_TOKEN',
        'SNOWPIPE_NAME', 'TASK_NAME', 'WAREHOUSE_TASK', 'SCHEDULE_INTERVAL'
    ]
    
    missing_vars = [var for var in required_vars if var not in config]
    if missing_vars:
        print(f"❌ Variáveis faltando: {missing_vars}")
        return False
    
    print("✅ Configurações carregadas com sucesso!")
    
    # Templates dos arquivos SQL
    templates = {
        '01_create_stage.sql': '''-- =====================================================
-- Criação do Stage para Azure Blob Storage
-- =====================================================

-- Criar o stage para conectar com Azure Blob Storage
CREATE OR REPLACE STAGE stage_json_station_information
URL = 'azure://${AZURE_STORAGE_ACCOUNT}.blob.core.windows.net/${AZURE_CONTAINER}/'
CREDENTIALS = (
  AZURE_SAS_TOKEN = '${AZURE_SAS_TOKEN}'
)
FILE_FORMAT = (TYPE = JSON);

-- Verificar se o stage foi criado
SHOW STAGES LIKE 'stage_json_station_information';''',

        '02_create_tables.sql': '''-- =====================================================
-- Criação das Tabelas para Station Information
-- =====================================================

-- Criar schema se não existir
CREATE SCHEMA IF NOT EXISTS ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA};

-- Tabela para dados brutos JSON
CREATE OR REPLACE TABLE ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}._STATION_RAW_JSON (
    raw VARIANT,
    file_name STRING,
    file_row_number NUMBER,
    file_content_key STRING,
    file_last_modified TIMESTAMP_NTZ,
    load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Tabela final para dados processados
CREATE OR REPLACE TABLE ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.STATION_INFORMATION (
    station_id STRING,
    name STRING,
    region_id STRING,
    capacity NUMBER,
    lat FLOAT,
    lon FLOAT,
    short_name STRING,
    external_id STRING,
    station_type STRING,
    has_kiosk BOOLEAN,
    electric_bike_surcharge_waiver BOOLEAN,
    eightd_has_key_dispenser BOOLEAN,
    rental_methods VARIANT,
    rental_uris VARIANT,
    eightd_station_services VARIANT,
    load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Verificar tabelas criadas
SHOW TABLES IN SCHEMA ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA};''',

        '03_create_snowpipe.sql': '''-- =====================================================
-- Criação do Snowpipe com Agendamento
-- =====================================================

-- Criar o Snowpipe para carregar dados do Azure Blob Storage
CREATE OR REPLACE PIPE ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.${SNOWPIPE_NAME}
AUTO_INGEST = TRUE
AS
COPY INTO ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}._STATION_RAW_JSON
FROM @stage_json_station_information/${JSON_FILE_PATH}
FILE_FORMAT = (TYPE = JSON);

-- Verificar o Snowpipe criado
SHOW PIPES IN SCHEMA ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA};

-- Obter a URL de notificação do Snowpipe (para configurar no Azure Event Grid)
SELECT SYSTEM$PIPE_FORCE_RESUME('${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.${SNOWPIPE_NAME}');
SELECT SYSTEM$PIPE_STATUS('${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.${SNOWPIPE_NAME}');''',

        '05_create_task.sql': '''-- =====================================================
-- Criação da Task para Processamento Automático
-- =====================================================

-- Criar warehouse para a task se não existir
CREATE WAREHOUSE IF NOT EXISTS ${WAREHOUSE_TASK}
WAREHOUSE_SIZE = 'XSMALL'
AUTO_SUSPEND = 60
AUTO_RESUME = TRUE;

-- Criar task para processar dados automaticamente
CREATE OR REPLACE TASK ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.${TASK_NAME}
WAREHOUSE = ${WAREHOUSE_TASK}
SCHEDULE = '${SCHEDULE_INTERVAL}'
AS
INSERT INTO ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.STATION_INFORMATION
SELECT
    value:station_id::STRING,
    value:name::STRING,
    value:region_id::STRING,
    value:capacity::NUMBER,
    value:lat::FLOAT,
    value:lon::FLOAT,
    value:short_name::STRING,
    value:external_id::STRING,
    value:station_type::STRING,
    value:has_kiosk::BOOLEAN,
    value:electric_bike_surcharge_waiver::BOOLEAN,
    value:eightd_has_key_dispenser::BOOLEAN,
    value:rental_methods,
    value:rental_uris,
    value:eightd_station_services,
    CURRENT_TIMESTAMP() as load_timestamp
FROM ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}._STATION_RAW_JSON,
     LATERAL FLATTEN(input => raw:data.stations)
WHERE raw IS NOT NULL;

-- Habilitar a task
ALTER TASK ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.${TASK_NAME} RESUME;

-- Verificar tasks criadas
SHOW TASKS IN SCHEMA ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA};'''
    }
    
    # Gerar arquivos SQL
    for filename, template in templates.items():
        content = replace_variables(template, config)
        
        with open(filename, 'w') as f:
            f.write(content)
        
        print(f"✅ Gerado: {filename}")
    
    # Gerar arquivo de deploy completo
    deploy_template = '''-- =====================================================
-- Script de Deploy Completo do Snowpipe
-- Execute este script para configurar todo o Snowpipe
-- =====================================================

-- Configurar contexto
USE DATABASE ${SNOWFLAKE_DATABASE};
USE SCHEMA ${SNOWFLAKE_SCHEMA};

-- 1. Criar Stage
-- =====================================================
CREATE OR REPLACE STAGE stage_json_station_information
URL = 'azure://${AZURE_STORAGE_ACCOUNT}.blob.core.windows.net/${AZURE_CONTAINER}/'
CREDENTIALS = (
  AZURE_SAS_TOKEN = '${AZURE_SAS_TOKEN}'
)
FILE_FORMAT = (TYPE = JSON);

-- 2. Criar Tabelas
-- =====================================================
-- Tabela para dados brutos JSON
CREATE OR REPLACE TABLE ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}._STATION_RAW_JSON (
    raw VARIANT,
    file_name STRING,
    file_row_number NUMBER,
    file_content_key STRING,
    file_last_modified TIMESTAMP_NTZ,
    load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Tabela final para dados processados
CREATE OR REPLACE TABLE ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.STATION_INFORMATION (
    station_id STRING,
    name STRING,
    region_id STRING,
    capacity NUMBER,
    lat FLOAT,
    lon FLOAT,
    short_name STRING,
    external_id STRING,
    station_type STRING,
    has_kiosk BOOLEAN,
    electric_bike_surcharge_waiver BOOLEAN,
    eightd_has_key_dispenser BOOLEAN,
    rental_methods VARIANT,
    rental_uris VARIANT,
    eightd_station_services VARIANT,
    load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 3. Criar Snowpipe
-- =====================================================
CREATE OR REPLACE PIPE ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.${SNOWPIPE_NAME}
AUTO_INGEST = TRUE
AS
COPY INTO ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}._STATION_RAW_JSON
FROM @stage_json_station_information/${JSON_FILE_PATH}
FILE_FORMAT = (TYPE = JSON);

-- 4. Criar Stream
-- =====================================================
CREATE OR REPLACE STREAM ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.station_raw_stream
ON TABLE ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}._STATION_RAW_JSON;

-- 5. Criar Warehouse para Task
-- =====================================================
CREATE WAREHOUSE IF NOT EXISTS ${WAREHOUSE_TASK}
WAREHOUSE_SIZE = 'XSMALL'
AUTO_SUSPEND = 60
AUTO_RESUME = TRUE;

-- 6. Criar Task com Agendamento
-- =====================================================
CREATE OR REPLACE TASK ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.${TASK_NAME}
WAREHOUSE = ${WAREHOUSE_TASK}
SCHEDULE = '${SCHEDULE_INTERVAL}'
AS
INSERT INTO ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.STATION_INFORMATION
SELECT
    value:station_id::STRING,
    value:name::STRING,
    value:region_id::STRING,
    value:capacity::NUMBER,
    value:lat::FLOAT,
    value:lon::FLOAT,
    value:short_name::STRING,
    value:external_id::STRING,
    value:station_type::STRING,
    value:has_kiosk::BOOLEAN,
    value:electric_bike_surcharge_waiver::BOOLEAN,
    value:eightd_has_key_dispenser::BOOLEAN,
    value:rental_methods,
    value:rental_uris,
    value:eightd_station_services,
    CURRENT_TIMESTAMP() as load_timestamp
FROM ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}._STATION_RAW_JSON,
     LATERAL FLATTEN(input => raw:data.stations)
WHERE raw IS NOT NULL;

-- 7. Habilitar Task
-- =====================================================
ALTER TASK ${SNOWFLAKE_DATABASE}.${SNOWFLAKE_SCHEMA}.${TASK_NAME} RESUME;

-- 8. Verificar Configuração
-- =====================================================
SELECT 'Stage criado' as status, COUNT(*) as count FROM @stage_json_station_information/${JSON_FILE_PATH};

SELECT 'Tabelas criadas' as status, COUNT(*) as count 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = '${SNOWFLAKE_SCHEMA}' 
AND TABLE_NAME IN ('_STATION_RAW_JSON', 'STATION_INFORMATION');

SELECT 'Snowpipe criado' as status, PIPE_STATE 
FROM INFORMATION_SCHEMA.PIPES 
WHERE PIPE_NAME = '${SNOWPIPE_NAME}';

SELECT 'Task criada' as status, TASK_STATE 
FROM INFORMATION_SCHEMA.TASKS 
WHERE TASK_NAME = '${TASK_NAME}';

-- 9. Obter URL de Notificação para Azure Event Grid
-- =====================================================
SELECT 
    'URL para Azure Event Grid' as info,
    NOTIFICATION_CHANNEL_NAME as notification_url
FROM INFORMATION_SCHEMA.PIPES 
WHERE PIPE_NAME = '${SNOWPIPE_NAME}';

-- 10. Status Final
-- =====================================================
SELECT 'Deploy concluído com sucesso!' as status;'''
    
    deploy_content = replace_variables(deploy_template, config)
    with open('deploy_snowpipe.sql', 'w') as f:
        f.write(deploy_content)
    
    print("✅ Gerado: deploy_snowpipe.sql")
    print("\n🎉 Todos os arquivos SQL foram gerados dinamicamente!")
    return True

if __name__ == "__main__":
    print("🚀 Gerando arquivos SQL dinamicamente...")
    success = generate_sql_files()
    
    if success:
        print("\n📋 Próximos passos:")
        print("1. Execute: python3 generate_sql.py")
        print("2. Execute: deploy_snowpipe.sql no Snowflake")
        print("3. Configure o Azure Event Grid")
    else:
        print("\n❌ Erro na geração dos arquivos") 