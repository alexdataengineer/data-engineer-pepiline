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
