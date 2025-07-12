# Data Engineering Pipeline - Citi Bike Analytics

## 🚀 Project Overview

This data engineering project extracts, transforms, and loads Citi Bike data to provide analytics and insights. The pipeline follows a modern data architecture with Azure Data Factory, Snowflake, and dbt.

**Developer**: Alexsander - Data Engineer

## 📊 Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Citi Bike     │    │   Azure Data     │    │   Azure Blob    │    │   Snowflake     │
│     API         │───▶│     Factory      │───▶│     Storage     │───▶│   Data Lake     │
│                 │    │   (Copy Data)    │    │   (JSON Files)  │    │   (Raw Layer)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘    └─────────────────┘
                                                                              │
                                                                              ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   dbt Core      │◀───│   Snowflake      │    │   Snowflake     │    │   Analytics     │
│ (Transform)     │    │   (Bronze Layer) │    │   (Silver Layer)│    │   (Gold Layer)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔄 Data Pipeline Flow

### 1. **Data Extraction** (Azure Data Factory)
- **Source**: Citi Bike API (`https://gbfs.citibikenyc.com`)
- **Tool**: Azure Data Factory Copy Data Activity
- **Format**: JSON responses
- **Frequency**: Scheduled extraction

### 2. **Data Storage** (Azure Blob Storage)
- **Container**: `raw`
- **File Format**: JSON
- **Structure**: `gbfs/en/station_information.json`
- **Purpose**: Raw data landing zone

### 3. **Data Ingestion** (Snowflake Snowpipe)
- **Tool**: Snowpipe with Auto-Ingest
- **Trigger**: Azure Event Grid notifications
- **Target**: Raw JSON tables
- **Processing**: Real-time ingestion

### 4. **Data Transformation** (dbt)
- **Tool**: dbt Core
- **Models**: Bronze → Silver → Gold layers
- **Transformations**: Data cleaning, business logic, aggregations
- **Output**: Analytics-ready datasets

### 5. **Data Analytics** (Snowflake)
- **Gold Layer**: Final analytics tables
- **Use Cases**: Business intelligence, reporting, dashboards

## 🛠️ Technology Stack

### Cloud Platform
- **Azure**: Data Factory, Blob Storage, Event Grid
- **Snowflake**: Data Warehouse, Snowpipe, Tasks

### Data Tools
- **dbt**: Data transformation and modeling
- **Python**: Scripts and automation
- **SQL**: Data queries and transformations

### Infrastructure
- **Git**: Version control and collaboration
- **CI/CD**: Automated deployments

## 📁 Project Structure

```
data-engineer-pipeline/
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
├── SNOWFLAKE_SETUP.md           # Snowflake configuration guide
├── GIT_SECURITY_GUIDE.md        # Security best practices
├── SOLUTION_SUMMARY.md           # Solution documentation
├── snowpipe/                     # Snowpipe configurations
│   └── station_information/      # Station data pipeline
├── dataset/                      # Azure Synapse datasets
├── pipeline/                     # Azure Data Factory pipelines
├── linkedService/                # Azure Synapse linked services
├── credential/                   # Secure credential storage
├── trigger/                      # Pipeline triggers
├── integrationRuntime/           # Integration runtime configs
└── notebook/                     # Jupyter notebooks
```

## 🚀 Getting Started

### Prerequisites
- Azure subscription
- Snowflake account
- Python 3.8+
- dbt Core

### Quick Start
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd data-engineer-pipeline
   ```

2. **Configure Snowflake**
   ```bash
   cd snowpipe/station_information
   cp config.env.example config.env
   # Edit config.env with your credentials
   python3 generate_sql.py
   ```

3. **Deploy to Snowflake**
   ```sql
   -- Execute in Snowflake
   @deploy_snowpipe.sql
   ```

4. **Set up dbt**
   ```bash
   dbt init citi_bike_analytics
   dbt run
   ```

## 📊 Data Models

### Bronze Layer (Raw)
- `_station_raw_json`: Raw JSON data from API
- `station_information`: Parsed station data

### Silver Layer (Cleaned)
- `stations_cleaned`: Cleaned and validated station data
- `stations_enriched`: Enriched with additional metrics

### Gold Layer (Analytics)
- `station_analytics`: Business metrics and KPIs
- `station_trends`: Time-series analysis
- `station_performance`: Performance indicators

## 🔧 Configuration

### Environment Variables
```bash
# Snowflake Configuration
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema

# Azure Configuration
AZURE_STORAGE_ACCOUNT=your_storage_account
AZURE_CONTAINER=raw
AZURE_SAS_TOKEN=your_sas_token
```

### Security
- Credentials stored in environment variables
- SAS tokens with limited permissions
- Snowflake role-based access control
- Git security practices implemented

## 📈 Monitoring

### Pipeline Health
- Snowpipe execution status
- Task completion rates
- Data quality metrics
- Error tracking and alerting

### Performance Metrics
- Data processing times
- Storage utilization
- Query performance
- Cost optimization

## 🔄 CI/CD Pipeline

### Automated Deployment
1. **Code Changes**: Git push triggers pipeline
2. **Testing**: Automated tests for data quality
3. **Deployment**: Automated deployment to environments
4. **Monitoring**: Health checks and alerts

### Environment Management
- **Development**: Local testing and development
- **Staging**: Integration testing
- **Production**: Live data processing

 Alexsander - Data Engineer**
