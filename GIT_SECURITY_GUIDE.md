# 🔐 Guia de Segurança para Git

## ⚠️ IMPORTANTE: Proteção de Senhas

Este projeto usa configurações dinâmicas para proteger senhas e credenciais sensíveis. **NUNCA** commite arquivos com senhas reais!

## 📁 Arquivos SEGUROS para Git

### ✅ Arquivos que podem ser commitados:
- `config.env.example` - Template de configuração (sem senhas reais)
- `generate_sql.py` - Script de geração dinâmica
- `clean_generated_files.py` - Script de limpeza
- `README.md` - Documentação
- `*.sql` - Arquivos SQL fixos (sem credenciais)

### ❌ Arquivos que NÃO devem ser commitados:
- `config.env` - **CONTÉM SENHAS REAIS**
- `credential/*.json` - **CONTÉM CREDENCIAIS**
- `linkedService/*.json` - **CONTÉM CONFIGURAÇÕES SENSÍVEIS**
- Arquivos SQL gerados dinamicamente

## 🛡️ Proteções Implementadas

### 1. .gitignore
O arquivo `.gitignore` protege automaticamente:
```gitignore
# Arquivos de configuração com senhas
config.env
*.env
.env

# Arquivos de credenciais
credential/*.json
linkedService/*.json

# Arquivos SQL gerados dinamicamente
snowpipe/*/01_create_stage.sql
snowpipe/*/02_create_tables.sql
snowpipe/*/03_create_snowpipe.sql
snowpipe/*/05_create_task.sql
snowpipe/*/deploy_snowpipe.sql
```

### 2. Configuração Dinâmica
- Senhas ficam apenas no `config.env` (não commitado)
- Scripts SQL são gerados dinamicamente
- Templates usam placeholders como `${SNOWFLAKE_USER}`

## 🚀 Fluxo de Trabalho Seguro

### Para Desenvolvedores

1. **Clone o repositório**:
   ```bash
   git clone <repo>
   cd snowpipe/station_information
   ```

2. **Configure suas credenciais**:
   ```bash
   cp config.env.example config.env
   # Edite config.env com suas senhas reais
   ```

3. **Gere os arquivos SQL**:
   ```bash
   python3 generate_sql.py
   ```

4. **Execute no Snowflake**:
   ```sql
   @deploy_snowpipe.sql
   ```

5. **Limpe os arquivos gerados**:
   ```bash
   python3 clean_generated_files.py
   ```

6. **Commit apenas arquivos seguros**:
   ```bash
   git add config.env.example generate_sql.py README.md
   git commit -m "Adiciona configuração dinâmica segura"
   ```

### Para Deploy em Produção

1. **Configure variáveis de ambiente** no servidor
2. **Execute o script de geração**
3. **Execute o deploy no Snowflake**
4. **Nunca commite o config.env**

## 🔍 Verificações de Segurança

### Antes de Fazer Commit

```bash
# Verifique se não há senhas no código
grep -r "Juniorcamisa1007" . --exclude-dir=.git
grep -r "sp=racwdlme" . --exclude-dir=.git

# Verifique se config.env não está sendo commitado
git status | grep config.env
```

### Verificar Arquivos Sensíveis

```bash
# Lista arquivos que podem conter senhas
find . -name "*.env" -o -name "*.json" | grep -v node_modules
```

## 🚨 Cenários de Risco

### ❌ NUNCA FAÇA:
- Commitar `config.env` com senhas reais
- Commitar arquivos `credential/*.json`
- Commitar arquivos `linkedService/*.json`
- Commitar arquivos SQL gerados dinamicamente
- Colocar senhas em comentários de código

### ✅ SEMPRE FAÇA:
- Use `config.env.example` como template
- Gere arquivos SQL dinamicamente
- Limpe arquivos gerados antes do commit
- Use variáveis de ambiente em produção
- Rotacione senhas regularmente

## 🔧 Configuração para CI/CD

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

## 📋 Checklist de Segurança

- [ ] `config.env` está no `.gitignore`
- [ ] `credential/*.json` está no `.gitignore`
- [ ] `linkedService/*.json` está no `.gitignore`
- [ ] Arquivos SQL gerados estão no `.gitignore`
- [ ] `config.env.example` não contém senhas reais
- [ ] Scripts usam placeholders dinâmicos
- [ ] Senhas não estão hardcoded no código
- [ ] Variáveis de ambiente configuradas em produção

## 🆘 Em Caso de Vazamento

1. **Imediatamente**:
   - Rotacione todas as senhas
   - Revogue tokens SAS
   - Altere credenciais do Snowflake

2. **Investigue**:
   - Verifique logs do Git
   - Identifique onde ocorreu o vazamento
   - Corrija a configuração

3. **Prevenção**:
   - Revise `.gitignore`
   - Implemente hooks do Git
   - Configure alertas de segurança

## 📞 Suporte

Se encontrar problemas de segurança:
1. Revise este guia
2. Verifique a configuração do `.gitignore`
3. Use os scripts de limpeza fornecidos
4. Consulte a documentação do projeto

**Lembre-se: Segurança em primeiro lugar! 🔒** 