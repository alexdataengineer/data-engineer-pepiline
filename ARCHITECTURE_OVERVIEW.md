# 🏗️ Complete Data Engineering Architecture

## 📊 System Overview

This data engineering pipeline extracts Citi Bike data from APIs, processes it through multiple layers, and delivers analytics-ready data for business intelligence.

**Developer**: Alexsander - Data Engineer

## 🔄 Complete Data Flow

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

## 🛠️ Technology Stack

### Data Sources
- **Citi Bike API**: `https://gbfs.citibikenyc.com`
- **Data Format**: JSON (station_information.json)

### Cloud Platform
- **Azure**: Data Factory, Blob Storage, Event Grid
- **Snowflake**: Data Warehouse, Snowpipe, Tasks

### Data Processing
- **dbt**: Data transformation and modeling
- **Python**: Scripts and automation
- **SQL**: Data queries and transformations

### Infrastructure
- **Git**: Version control and collaboration
- **CI/CD**: Automated deployments

## 📁 Project Structure

```
data-engineer-pipeline/
├── README.md                     # Main project documentation
├── SNOWFLAKE_SETUP.md           # Snowflake configuration guide
├── GIT_SECURITY_GUIDE.md        # Security best practices
├── SOLUTION_SUMMARY.md           # Solution documentation
├── DBT_README.md                # dbt transformation guide
├── ARCHITECTURE_OVERVIEW.md     # This file
├── .gitignore                   # Git ignore rules
├── dbt_project.yml              # dbt project configuration
├── profiles.yml                 # dbt profiles configuration
├── snowpipe/                    # Snowpipe configurations
│   └── station_information/     # Station data pipeline
├── models/                      # dbt models
│   ├── bronze/                  # Raw data layer
│   ├── silver/                  # Cleaned data layer
│   ├── gold/                    # Analytics layer
│   └── sources.yml              # Source definitions
├── dataset/                     # Azure Synapse datasets
├── pipeline/                    # Azure Data Factory pipelines
├── linkedService/               # Azure Synapse linked services
├── credential/                  # Secure credential storage
├── trigger/                     # Pipeline triggers
├── integrationRuntime/          # Integration runtime configs
└── notebook/                    # Jupyter notebooks
```

## 🔄 Data Pipeline Stages

### 1. Data Extraction (Azure Data Factory)
- **Source**: Citi Bike API (`https://gbfs.citibikenyc.com`)
- **Tool**: Azure Data Factory Copy Data Activity
- **Format**: JSON responses
- **Frequency**: Scheduled extraction
- **Output**: Azure Blob Storage

### 2. Data Storage (Azure Blob Storage)
- **Container**: `raw`
- **File Format**: JSON
- **Structure**: `gbfs/en/station_information.json`
- **Purpose**: Raw data landing zone
- **Retention**: Configurable retention policies

### 3. Data Ingestion (Snowflake Snowpipe)
- **Tool**: Snowpipe with Auto-Ingest
- **Trigger**: Azure Event Grid notifications
- **Target**: Raw JSON tables
- **Processing**: Real-time ingestion
- **Tables**: `_STATION_RAW_JSON`, `STATION_INFORMATION`

### 4. Data Transformation (dbt)
- **Tool**: dbt Core
- **Architecture**: Bronze → Silver → Gold layers
- **Transformations**: Data cleaning, business logic, aggregations
- **Output**: Analytics-ready datasets

### 5. Data Analytics (Snowflake)
- **Gold Layer**: Final analytics tables
- **Use Cases**: Business intelligence, reporting, dashboards
- **Schemas**: `BRONZE`, `SILVER`, `GOLD`

## 📊 Data Models

### Bronze Layer (Raw)
- **Purpose**: Raw data with minimal transformations
- **Tables**: `stations_bronze`
- **Features**: Basic data quality checks, source validation

### Silver Layer (Cleaned)
- **Purpose**: Cleaned and enriched data
- **Tables**: `stations_silver`
- **Features**: 
  - Geographic categorization
  - Station size classification
  - Data quality scoring
  - Business logic applied

### Gold Layer (Analytics)
- **Purpose**: Business analytics and KPIs
- **Tables**: `station_analytics`
- **Features**:
  - Station metrics by region
  - Geographic summaries
  - Station type analysis
  - Overall system metrics

## 🔧 Configuration Management

### Environment Variables
```bash
# Snowflake Configuration
SNOWFLAKE_USER=ALEXBETIM2025
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=FYRESSZ-ME75053
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=STANGING
SNOWFLAKE_SCHEMA=AZURE_SYNAPSE

# Azure Configuration
AZURE_STORAGE_ACCOUNT=lakeiqbetim
AZURE_CONTAINER=raw
AZURE_SAS_TOKEN=your_sas_token
```

### Security Features
- **Dynamic Configuration**: Passwords not in code
- **Git Protection**: `.gitignore` protects sensitive files
- **Environment Variables**: Secure credential management
- **Role-Based Access**: Snowflake security controls

## 📈 Monitoring & Observability

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

### Data Quality
- Completeness checks
- Validity tests
- Consistency monitoring
- Freshness tracking

## 🔄 Automation & Scheduling

### Azure Data Factory
- **Frequency**: Scheduled extraction
- **Triggers**: Time-based or event-based
- **Monitoring**: Built-in monitoring and alerting

### Snowflake Snowpipe
- **Auto-Ingest**: Enabled
- **Event-Driven**: Azure Event Grid notifications
- **Real-Time**: Immediate processing

### dbt Transformations
- **Scheduling**: Configurable via dbt Cloud or Airflow
- **Dependencies**: Automatic dependency management
- **Testing**: Automated data quality tests

## 🚀 Deployment Strategy

### Development Environment
- Local development with dbt
- Test data and configurations
- Development Snowflake environment

### Staging Environment
- Integration testing
- Performance validation
- Data quality verification

### Production Environment
- Live data processing
- High availability
- Monitoring and alerting

## 📚 Documentation

### Technical Documentation
- [Main README](README.md): Project overview and setup
- [Snowflake Setup](SNOWFLAKE_SETUP.md): Snowflake configuration
- [Security Guide](GIT_SECURITY_GUIDE.md): Security best practices
- [dbt Guide](DBT_README.md): Transformation layer documentation

### Architecture Documentation
- [Solution Summary](SOLUTION_SUMMARY.md): Technical solution details
- [Architecture Overview](ARCHITECTURE_OVERVIEW.md): This document

## 🔍 Troubleshooting

### Common Issues
1. **API Connection**: Check Citi Bike API availability
2. **Azure Storage**: Verify SAS token permissions
3. **Snowflake**: Confirm warehouse and role access
4. **dbt**: Validate environment variables and connections

### Debug Commands
```bash
# Test Azure Data Factory connection
az datafactory pipeline list --factory-name your-factory

# Test Snowflake connection
dbt debug

# Check Snowpipe status
SELECT SYSTEM$PIPE_STATUS('station_information_pipe');
```

## 📊 Analytics Examples

### Station Distribution
```sql
SELECT 
    geographic_area,
    COUNT(*) as station_count,
    AVG(capacity) as avg_capacity
FROM GOLD.station_analytics
GROUP BY geographic_area
ORDER BY station_count DESC;
```

### Data Quality Overview
```sql
SELECT 
    data_layer,
    COUNT(*) as record_count,
    AVG(data_quality_score) as avg_quality
FROM GOLD.station_analytics
GROUP BY data_layer;
```

## 🎯 Success Metrics

### Technical Metrics
- **Data Freshness**: < 5 minutes from API to analytics
- **Data Quality**: > 95% completeness score
- **System Uptime**: > 99.9% availability
- **Processing Time**: < 2 minutes end-to-end

### Business Metrics
- **Station Coverage**: Complete NYC station data
- **Geographic Distribution**: All boroughs covered
- **Data Accuracy**: Valid coordinates and capacities
- **Analytics Readiness**: Clean, structured data

## 🚀 Future Enhancements

### Planned Features
1. **Real-time Analytics**: Stream processing capabilities
2. **Advanced ML**: Predictive analytics for station usage
3. **Multi-source Integration**: Additional bike share systems
4. **Advanced Monitoring**: Custom dashboards and alerts

### Scalability Considerations
- **Data Volume**: Handle increased API data
- **Processing Power**: Optimize warehouse usage
- **Storage**: Implement data lifecycle management
- **Performance**: Query optimization and caching

---

Alexsander - Data Engineer**

*This architecture provides a complete, scalable, and secure data engineering solution for Citi Bike analytics.* 