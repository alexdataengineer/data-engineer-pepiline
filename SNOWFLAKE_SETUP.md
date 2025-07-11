# Configuração do Snowflake no Azure Synapse

## Informações da Conta Snowflake

- **Account Identifier**: FYRESSZ-ME75053
- **Data Sharing Account Identifier**: FYRESSZ.ME75053
- **Organization Name**: FYRESSZ
- **Account Name**: ME75053
- **Account/Server URL**: FYRESSZ-ME75053.snowflakecomputing.com
- **User Name**: ALEXBETIM2025
- **Role**: ACCOUNTADMIN
- **Account Locator**: WU43756
- **Cloud Platform**: AZURE
- **Edition**: Enterprise

## Arquivos Criados

### 1. Linked Service
- **Arquivo**: `linkedService/SnowflakeLinkedService.json`
- **Propósito**: Configuração da conexão com o Snowflake
- **Ação Necessária**: Substituir `YOUR_PASSWORD_HERE` pela senha real

### 2. Credentials
- **Arquivo**: `credential/SnowflakeCredential.json`
- **Propósito**: Armazenamento seguro das credenciais
- **Ação Necessária**: Substituir `YOUR_PASSWORD_HERE` pela senha real

### 3. Datasets
- **SnowflakeDataset.json**: Dataset para ler dados do Snowflake
- **SnowflakeOutputDataset.json**: Dataset para salvar dados extraídos

### 4. Pipeline
- **Arquivo**: `pipeline/snowflake_data_extraction.json`
- **Propósito**: Pipeline de exemplo para extrair dados do Snowflake

## Passos para Configuração

### 1. Configurar Credenciais
Edite o arquivo `credential/SnowflakeCredential.json` e substitua `YOUR_PASSWORD_HERE` pela sua senha real:

```json
{
    "type": "Basic",
    "typeProperties": {
        "userName": "ALEXBETIM2025",
        "password": {
            "type": "SecureString",
            "value": "SUA_SENHA_AQUI"
        }
    }
}
```

### 2. Publicar no Azure Synapse
Execute os seguintes comandos para publicar as configurações:

```bash
# Publicar linked service
az synapse linked-service create --workspace-name SEU_WORKSPACE --name SnowflakeLinkedService --file @linkedService/SnowflakeLinkedService.json

# Publicar credentials
az synapse credential create --workspace-name SEU_WORKSPACE --name SnowflakeCredential --file @credential/SnowflakeCredential.json

# Publicar datasets
az synapse dataset create --workspace-name SEU_WORKSPACE --name SnowflakeDataset --file @dataset/SnowflakeDataset.json
az synapse dataset create --workspace-name SEU_WORKSPACE --name SnowflakeOutputDataset --file @dataset/SnowflakeOutputDataset.json

# Publicar pipeline
az synapse pipeline create --workspace-name SEU_WORKSPACE --name snowflake_data_extraction --file @pipeline/snowflake_data_extraction.json
```

### 3. Testar Conexão
No Azure Synapse Studio:
1. Vá para "Manage" > "Linked Services"
2. Encontre "SnowflakeLinkedService"
3. Clique em "Test connection"

## Exemplo de Uso

O pipeline `snowflake_data_extraction` demonstra como:
- Conectar ao Snowflake
- Executar uma query SQL
- Extrair dados da tabela CUSTOMER
- Salvar os resultados em formato JSON no Azure Data Lake

## Queries Úteis

### Verificar Conexão
```sql
SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_ACCOUNT();
```

### Listar Databases
```sql
SHOW DATABASES;
```

### Listar Schemas
```sql
SHOW SCHEMAS IN DATABASE SNOWFLAKE_SAMPLE_DATA;
```

### Listar Tabelas
```sql
SHOW TABLES IN SCHEMA SNOWFLAKE_SAMPLE_DATA.TPCH_SF1;
```

## Troubleshooting

### Erro de Conexão
- Verifique se a senha está correta
- Confirme se o usuário tem as permissões necessárias
- Verifique se o firewall permite conexões

### Erro de Warehouse
- Certifique-se de que o warehouse `COMPUTE_WH` existe
- Verifique se o usuário tem acesso ao warehouse

### Erro de Database/Schema
- Confirme se o database `SNOWFLAKE_SAMPLE_DATA` existe
- Verifique se o schema `TPCH_SF1` existe
- Confirme se o usuário tem acesso aos objetos 