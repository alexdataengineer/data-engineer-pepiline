# Snowflake Configuration in Azure Synapse

## Snowflake Account Information

- **Account Identifier**: FYRESSZ######
- **Data Sharing Account Identifier**: FYRE#####
- **Organization Name**: FYRESSZ
- **Account Name**: ME75053
- **Account/Server URL**: FYRESSZ-ME75053.##############
- **User Name**: ###############
- **Role**: ACCOUNTADMIN
- **Account Locator**: WU43756
- **Cloud Platform**: AZURE
- **Edition**: Enterprise

## Created Files

### 1. Linked Service
- **File**: `linkedService/SnowflakeLinkedService.json`
- **Purpose**: Snowflake connection configuration
- **Required Action**: Replace `YOUR_PASSWORD_HERE` with real password

### 2. Credentials
- **File**: `credential/SnowflakeCredential.json`
- **Purpose**: Secure credential storage
- **Required Action**: Replace `YOUR_PASSWORD_HERE` with real password

### 3. Datasets
- **SnowflakeDataset.json**: Dataset to read data from Snowflake
- **SnowflakeOutputDataset.json**: Dataset to save extracted data

### 4. Pipeline
- **File**: `pipeline/snowflake_data_extraction.json`
- **Purpose**: Example pipeline to extract data from Snowflake

## Setup Steps

### 1. Configure Credentials
Edit the file `credential/SnowflakeCredential.json` and replace `YOUR_PASSWORD_HERE` with your real password:

```json
{
    "type": "Basic",
    "typeProperties": {
        "userName": "ALEXBETIM2025",
        "password": {
            "type": "SecureString",
            "value": "YOUR_REAL_PASSWORD_HERE"
        }
    }
}
```

### 2. Publish to Azure Synapse
Execute the following commands to publish configurations:

```bash
# Publish linked service
az synapse linked-service create --workspace-name YOUR_WORKSPACE --name SnowflakeLinkedService --file @linkedService/SnowflakeLinkedService.json

# Publish credentials
az synapse credential create --workspace-name YOUR_WORKSPACE --name SnowflakeCredential --file @credential/SnowflakeCredential.json

# Publish datasets
az synapse dataset create --workspace-name YOUR_WORKSPACE --name SnowflakeDataset --file @dataset/SnowflakeDataset.json
az synapse dataset create --workspace-name YOUR_WORKSPACE --name SnowflakeOutputDataset --file @dataset/SnowflakeOutputDataset.json

# Publish pipeline
az synapse pipeline create --workspace-name YOUR_WORKSPACE --name snowflake_data_extraction --file @pipeline/snowflake_data_extraction.json
```

### 3. Test Connection
In Azure Synapse Studio:
1. Go to "Manage" > "Linked Services"
2. Find "SnowflakeLinkedService"
3. Click "Test connection"

## Usage Example

The `snowflake_data_extraction` pipeline demonstrates how to:
- Connect to Snowflake
- Execute SQL query
- Extract data from CUSTOMER table
- Save results in JSON format to Azure Data Lake

## Useful Queries

### Test Connection
```sql
SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_ACCOUNT();
```

### List Databases
```sql
SHOW DATABASES;
```

### List Schemas
```sql
SHOW SCHEMAS IN DATABASE SNOWFLAKE_SAMPLE_DATA;
```

### List Tables
```sql
SHOW TABLES IN SCHEMA SNOWFLAKE_SAMPLE_DATA.TPCH_SF1;
```

## Troubleshooting

### Connection Error
- Verify password is correct
- Confirm user has necessary permissions
- Check if firewall allows connections

### Warehouse Error
- Ensure warehouse `COMPUTE_WH` exists
- Verify user has access to warehouse

### Database/Schema Error
- Confirm database `SNOWFLAKE_SAMPLE_DATA` exists
- Verify schema `TPCH_SF1` exists
- Confirm user has access to objects 
