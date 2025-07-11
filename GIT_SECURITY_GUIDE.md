# 🔐 Git Security Guide

## ⚠️ IMPORTANT: Password Protection

This project uses dynamic configurations to protect passwords and sensitive credentials. **NEVER** commit files with real passwords!

## 📁 SAFE Files for Git

### ✅ Files that can be committed:
- `config.env.example` - Configuration template (no real passwords)
- `generate_sql.py` - Dynamic generation script
- `clean_generated_files.py` - Cleanup script
- `README.md` - Documentation
- `*.sql` - Fixed SQL files (no credentials)

### ❌ Files that should NOT be committed:
- `config.env` - **CONTAINS REAL PASSWORDS**
- `credential/*.json` - **CONTAINS CREDENTIALS**
- `linkedService/*.json` - **CONTAINS SENSITIVE CONFIGURATIONS**
- Dynamically generated SQL files

## 🛡️ Implemented Protections

### 1. .gitignore
The `.gitignore` file automatically protects:
```gitignore
# Password configuration files
config.env
*.env
.env

# Credential files
credential/*.json
linkedService/*.json

# Dynamically generated SQL files
snowpipe/*/01_create_stage.sql
snowpipe/*/02_create_tables.sql
snowpipe/*/03_create_snowpipe.sql
snowpipe/*/05_create_task.sql
snowpipe/*/deploy_snowpipe.sql
```

### 2. Dynamic Configuration
- Passwords stay only in `config.env` (not committed)
- SQL scripts are generated dynamically
- Templates use placeholders like `${SNOWFLAKE_USER}`

## 🚀 Secure Workflow

### For Developers

1. **Clone the repository**:
   ```bash
   git clone <repo>
   cd snowpipe/station_information
   ```

2. **Configure your credentials**:
   ```bash
   cp config.env.example config.env
   # Edit config.env with your real passwords
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

6. **Commit only safe files**:
   ```bash
   git add config.env.example generate_sql.py README.md
   git commit -m "Add secure dynamic configuration"
   ```

### For Production Deployment

1. **Configure environment variables** on the server
2. **Execute the generation script**
3. **Execute the deploy in Snowflake**
4. **Never commit config.env**

## 🔍 Security Checks

### Before Committing

```bash
# Check if there are no passwords in code
grep -r "Juniorcamisa1007" . --exclude-dir=.git
grep -r "sp=racwdlme" . --exclude-dir=.git

# Check if config.env is not being committed
git status | grep config.env
```

### Check Sensitive Files

```bash
# List files that might contain passwords
find . -name "*.env" -o -name "*.json" | grep -v node_modules
```

## 🚨 Risk Scenarios

### ❌ NEVER DO:
- Commit `config.env` with real passwords
- Commit `credential/*.json` files
- Commit `linkedService/*.json` files
- Commit dynamically generated SQL files
- Put passwords in code comments

### ✅ ALWAYS DO:
- Use `config.env.example` as template
- Generate SQL files dynamically
- Clean generated files before commit
- Use environment variables in production
- Rotate passwords regularly

## 🔧 CI/CD Configuration

### GitHub Actions
```yaml
- name: Generate SQL
  env:
    SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
    AZURE_SAS_TOKEN: ${{ secrets.AZURE_SAS_TOKEN }}
  run: python3 generate_sql.py
```

### Azure DevOps
```yaml
- task: PythonScript@0
  inputs:
    scriptSource: 'filePath'
    scriptPath: 'generate_sql.py'
  env:
    SNOWFLAKE_PASSWORD: $(SNOWFLAKE_PASSWORD)
```

## 📋 Security Checklist

- [ ] `config.env` is in `.gitignore`
- [ ] `credential/*.json` is in `.gitignore`
- [ ] `linkedService/*.json` is in `.gitignore`
- [ ] Generated SQL files are in `.gitignore`
- [ ] `config.env.example` contains no real passwords
- [ ] Scripts use dynamic placeholders
- [ ] Passwords are not hardcoded in code
- [ ] Environment variables configured in production

## 🆘 In Case of Leak

1. **Immediately**:
   - Rotate all passwords
   - Revoke SAS tokens
   - Change Snowflake credentials

2. **Investigate**:
   - Check Git logs
   - Identify where leak occurred
   - Fix configuration

3. **Prevention**:
   - Review `.gitignore`
   - Implement Git hooks
   - Configure security alerts

## 📞 Support

If you encounter security issues:
1. Review this guide
2. Check `.gitignore` configuration
3. Use provided cleanup scripts
4. Consult project documentation

**Remember: Security first! 🔒** 