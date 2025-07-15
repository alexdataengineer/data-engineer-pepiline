# dbt - Citi Bike Analytics

This directory contains the dbt (data build tool) project for transforming Citi Bike data from raw to analytics-ready format.

## 🏗️ Data Architecture

```
Raw Data (Bronze) → Cleaned Data (Silver) → Analytics (Gold)
```

### Data Layers

1. **Bronze Layer** (`models/bronze/`)
   - Raw data with minimal transformations
   - Basic data quality checks
   - Source: Snowflake raw tables

2. **Silver Layer** (`models/silver/`)
   - Cleaned and enriched data
   - Business logic applied
   - Data quality rules implemented
   - Geographic categorization

3. **Gold Layer** (`models/gold/`)
   - Business analytics and KPIs
   - Aggregated metrics
   - Ready for BI tools and dashboards

## 🚀 Getting Started

### Prerequisites
- dbt Core installed
- Snowflake account configured
- Environment variables set

### Installation
```bash
# Install dbt
pip install dbt-snowflake

# Clone the repository
git clone <repository-url>
cd data-engineer-pipeline
```

### Configuration
1. **Set environment variables**:
   ```bash
   export SNOWFLAKE_ACCOUNT="FYRESSZ-ME75053"
   export SNOWFLAKE_USER="ALEXBETIM2025"
   export SNOWFLAKE_PASSWORD="your_password"
   export SNOWFLAKE_ROLE="ACCOUNTADMIN"
   export SNOWFLAKE_DATABASE="STANGING"
   export SNOWFLAKE_WAREHOUSE="COMPUTE_WH"
   export SNOWFLAKE_SCHEMA="AZURE_SYNAPSE"
   ```

2. **Test connection**:
   ```bash
   dbt debug
   ```

### Running dbt

#### Development
```bash
# Run all models
dbt run

# Run specific model
dbt run --select stations_bronze

# Run models with dependencies
dbt run --select +stations_silver
```

#### Testing
```bash
# Run all tests
dbt test

# Run specific tests
dbt test --select source:raw
```

#### Documentation
```bash
# Generate documentation
dbt docs generate

# Serve documentation
dbt docs serve
```

## 📊 Models Overview

### Bronze Models
- `stations_bronze`: Raw station data with basic cleaning

### Silver Models
- `stations_silver`: Cleaned and enriched station data
  - Geographic categorization
  - Station size classification
  - Data quality scoring
  - Business logic applied

### Gold Models
- `station_analytics`: Business analytics and KPIs
  - Station metrics by region
  - Geographic summaries
  - Station type analysis
  - Overall system metrics

## 🔧 Configuration

### Project Configuration (`dbt_project.yml`)
- Database: `STANGING`
- Schema: `AZURE_SYNAPSE`
- Target schemas: `BRONZE`, `SILVER`, `GOLD`

### Sources (`models/sources.yml`)
- Raw tables from Snowflake
- Data quality tests defined
- Column descriptions documented

### Profiles (`profiles.yml`)
- Development and production targets
- Environment variable configuration
- Snowflake connection settings

## 📈 Data Quality

### Tests Implemented
- **Not null tests**: Required fields
- **Unique tests**: Primary keys
- **Custom tests**: Business logic validation

### Data Quality Metrics
- Data completeness score
- Geographic coverage
- Station type distribution
- Capacity analysis

## 🔄 Workflow

### Daily Processing
1. **Data Ingestion**: Snowpipe loads raw data
2. **Bronze Processing**: Basic cleaning and validation
3. **Silver Processing**: Business logic and enrichment
4. **Gold Processing**: Analytics and KPIs
5. **Testing**: Data quality validation
6. **Documentation**: Updated model documentation

### Monitoring
```sql
-- Check model freshness
SELECT 
    table_name,
    last_altered,
    row_count
FROM information_schema.tables 
WHERE table_schema IN ('BRONZE', 'SILVER', 'GOLD')
ORDER BY last_altered DESC;
```

## 🛠️ Development

### Adding New Models
1. Create model file in appropriate layer
2. Add tests in `models/sources.yml`
3. Update documentation
4. Run tests and validate

### Best Practices
- Use incremental models for large datasets
- Implement data quality tests
- Document business logic
- Follow naming conventions
- Version control all changes

## 📚 Documentation

### Model Documentation
Each model includes:
- Description of purpose
- Business logic explanation
- Data quality rules
- Dependencies and lineage

### Generated Documentation
```bash
dbt docs generate
dbt docs serve
```

## 🔍 Troubleshooting

### Common Issues
1. **Connection errors**: Check environment variables
2. **Permission errors**: Verify Snowflake role permissions
3. **Model errors**: Check dependencies and syntax
4. **Test failures**: Review data quality issues

### Debug Commands
```bash
# Debug connection
dbt debug

# Show model dependencies
dbt ls --select +model_name

# Show compiled SQL
dbt compile --select model_name
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

## 🚀 Next Steps

1. **Set up scheduling**: Configure dbt Cloud or Airflow
2. **Add more models**: Expand analytics capabilities
3. **Implement alerts**: Set up data quality monitoring
4. **Create dashboards**: Connect to BI tools
5. **Optimize performance**: Tune warehouse and queries

---

** Alexsander - Data Engineer** 
