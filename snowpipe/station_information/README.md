# Snowpipe - Station Information (Dynamic Configuration)

This directory contains the complete Snowpipe configuration to load station information data from Azure Blob Storage to Snowflake with automatic processing using secure dynamic configurations.

## 🔐 Security

### Protected Files
- `config.env` - **DO NOT COMMIT** (contains real passwords)
- `credential/*.json` - **DO NOT COMMIT** (credentials)
- `linkedService/*.json` - **DO NOT COMMIT** (sensitive configurations)

### Safe Files for Git
- `config.env.example` - Configuration template (no real passwords)
- `generate_sql.py` - Dynamic generation script
- `clean_generated_files.py` - Cleanup script
- `README.md` - Documentation

## 📁 File Structure

```
snowpipe/station_information/
├── config.env.example          # Configuration template (safe for Git)
├── config.env                  # Real configuration (DO NOT COMMIT)
├── generate_sql.py             # Script to generate SQL dynamically
├── clean_generated_files.py    # Cleanup script
├── 04_create_stream.sql        # Stream (fixed)
├── 06_monitoring_queries.sql   # Monitoring queries (fixed)
├── 07_setup_azure_event_grid.sql # Azure Event Grid setup (fixed)
└── README.md                   # This file
```

## 🚀 Secure Configuration

### Step 1: Configure Environment Variables

1. **Copy the example file**:
   ```bash
   cp config.env.example config.env
   ```

2. **Edit the `config.env` file** with your real configurations:
   ```bash
   # Snowflake Credentials
   SNOWFLAKE_USER=ALEXBETIM2025
   SNOWFLAKE_PASSWORD=your_password_here
   SNOWFLAKE_ACCOUNT=FYRESSZ-ME75053
   
   # Azure Configurations
   AZURE_STORAGE_ACCOUNT=lakeiqbetim
   AZURE_SAS_TOKEN=your_token_here
   ```

### Step 2: Generate SQL Files Dynamically

Execute the Python script to generate SQL files with configurations:

```bash
python3 generate_sql.py
```

This command will:
- ✅ Load configurations from `config.env`
- ✅ Validate all required variables
- ✅ Generate SQL files with real values
- ✅ Create complete `deploy_snowpipe.sql`

### Step 3: Execute in Snowflake

Execute the generated file in Snowflake:

```sql
-- Execute in Snowflake
@deploy_snowpipe.sql
```

## ⚙️ Dynamic Configurations

### Available Variables

```bash
# Snowflake Credentials
SNOWFLAKE_USER=ALEXBETIM2025
SNOWFLAKE_PASSWORD=your_password_here
SNOWFLAKE_ACCOUNT=FYRESSZ-ME75053
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=STANGING
SNOWFLAKE_SCHEMA=AZURE_SYNAPSE

# Azure Blob Storage Configurations
AZURE_STORAGE_ACCOUNT=lakeiqbetim
AZURE_CONTAINER=raw
AZURE_SAS_TOKEN=your_token_here

# Snowpipe Configurations
SNOWPIPE_NAME=station_information_pipe
TASK_NAME=process_station_information_task
WAREHOUSE_TASK=COMPUTE_WH_TASK
SCHEDULE_INTERVAL=1 minute

# File Configurations
JSON_FILE_PATH=gbfs/en/station_information.json
```

### How It Works

1. **Templates**: SQL files use placeholders like `${SNOWFLAKE_USER}`
2. **Substitution**: Python script replaces placeholders with real values
3. **Generation**: Final SQL files are created with real values
4. **Security**: Passwords stay only in `config.env` (not committed)

## 🔄 Workflow

### For Developers

1. **Clone the repository**:
   ```bash
   git clone <repo>
   cd snowpipe/station_information
   ```

2. **Configure variables**:
   ```bash
   cp config.env.example config.env
   # Edit config.env with your credentials
   ```

3. **Generate SQL files**:
   ```bash
   python3 generate_sql.py
   ```

4. **Execute in Snowflake**:
   ```sql
   @deploy_snowpipe.sql
   ```

5. **Clean generated files**:
   ```bash
   python3 clean_generated_files.py
   ```

6. **Commit safe files**:
   ```bash
   git add config.env.example generate_sql.py README.md
   git commit -m "Secure dynamic configuration"
   ```

### For Production Deployment

1. **Configure environment variables** on the server
2. **Execute the generation script**
3. **Execute the deploy in Snowflake**
4. **Never commit config.env**

## 📊 Monitoring

### Monitoring Queries

Execute `06_monitoring_queries.sql` for:
- Snowpipe status
- Recent executions
- Task status
- Data counts
- Recent errors

### Automatic Checks

```sql
-- Snowpipe Status
SELECT PIPE_STATE FROM INFORMATION_SCHEMA.PIPES 
WHERE PIPE_NAME = '${SNOWPIPE_NAME}';

-- Task Status
SELECT TASK_STATE FROM INFORMATION_SCHEMA.TASKS 
WHERE TASK_NAME = '${TASK_NAME}';
```

## 🛠️ Troubleshooting

### Problem: config.env file not found
```bash
# Solution
cp config.env.example config.env
# Edit the file with your credentials
```

### Problem: Missing variables
```bash
# Check if all variables are in config.env
python3 generate_sql.py
```

### Problem: Connection error
```sql
-- Check credentials in Snowflake
SELECT CURRENT_USER(), CURRENT_ACCOUNT();
```

## 🔐 Advanced Security

### For Production Environments

1. **Use system environment variables**:
   ```bash
   export SNOWFLAKE_PASSWORD="secure_password"
   ```

2. **Use Azure Key Vault** to store secrets

3. **Use Azure Managed Identity** for authentication

4. **Rotate SAS tokens** regularly

### For CI/CD

1. **Configure secrets in pipeline**:
   ```yaml
   - name: Generate SQL
     env:
       SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
     run: python3 generate_sql.py
   ```

2. **Use Azure DevOps Variable Groups**

3. **Use GitHub Secrets**

## 📈 Benefits of Dynamic Configuration

- ✅ **Security**: Passwords not in code
- ✅ **Flexibility**: Easy configuration changes
- ✅ **Reusability**: Same code for different environments
- ✅ **Versioning**: Safe code for Git
- ✅ **Automation**: Easy CI/CD integration

## 🎯 Next Steps

1. **Configure `config.env`** with your credentials
2. **Execute `python3 generate_sql.py`**
3. **Execute the deploy in Snowflake**
4. **Configure Azure Event Grid**
5. **Monitor with provided queries**

The system is ready for secure production use! 🚀 