# Snowpipe - Station Information (Configuração Dinâmica)

Este diretório contém a configuração completa do Snowpipe para carregar dados de station information do Azure Blob Storage para o Snowflake com processamento automático, usando configurações dinâmicas seguras.

## 🔐 Segurança

### Arquivos Protegidos
- `config.env` - **NÃO COMMITAR** (contém senhas reais)
- `credential/*.json` - **NÃO COMMITAR** (credenciais)
- `linkedService/*.json` - **NÃO COMMITAR** (configurações sensíveis)

### Arquivos Seguros para Git
- `config.env.example` - Exemplo de configuração (sem senhas reais)
- `generate_sql.py` - Script para gerar SQL dinamicamente
- `README.md` - Documentação

## 📁 Estrutura dos Arquivos

```
snowpipe/station_information/
├── config.env.example          # Exemplo de configuração (seguro para Git)
├── config.env                  # Configuração real (NÃO COMMITAR)
├── generate_sql.py             # Script para gerar SQL dinamicamente
├── 04_create_stream.sql        # Stream (fixo)
├── 06_monitoring_queries.sql   # Queries de monitoramento (fixo)
├── 07_setup_azure_event_grid.sql # Configuração Azure Event Grid (fixo)
└── README.md                   # Este arquivo
```

## 🚀 Configuração Segura

### Passo 1: Configurar Variáveis de Ambiente

1. **Copie o arquivo de exemplo**:
   ```bash
   cp config.env.example config.env
   ```

### Passo 2: Gerar Arquivos SQL Dinamicamente

Execute o script Python para gerar os arquivos SQL com as configurações:

```bash
python3 generate_sql.py
```

Este comando irá:
- ✅ Carregar configurações do `config.env`
- ✅ Validar todas as variáveis necessárias
- ✅ Gerar arquivos SQL com valores reais
- ✅ Criar `deploy_snowpipe.sql` completo

### Passo 3: Executar no Snowflake

Execute o arquivo gerado no Snowflake:

```sql
-- Execute no Snowflake
@deploy_snowpipe.sql
```

/station_information.json
```

### Como Funciona

1. **Templates**: Os arquivos SQL usam placeholders como `${SNOWFLAKE_USER}`
2. **Substituição**: O script Python substitui os placeholders pelos valores reais
3. **Geração**: Arquivos SQL finais são criados com valores reais
4. **Segurança**: Senhas ficam apenas no `config.env` (não commitado)

## 🔄 Fluxo de Trabalho

### Para Desenvolvedores

1. **Clone o repositório**:
   ```bash
   git clone <repo>
   cd snowpipe/station_information
   ```

2. **Configure as variáveis**:
   ```bash
   cp config.env.example config.env
   # Edite config.env com suas credenciais
   ```

3. **Gere os arquivos SQL**:
   ```bash
   python3 generate_sql.py
   ```

4. **Execute no Snowflake**:
   ```sql
   @deploy_snowpipe.sql
   ```

### Para Deploy em Produção

1. **Configure variáveis de ambiente** no servidor
2. **Execute o script de geração**
3. **Execute o deploy no Snowflake**

## 📊 Monitoramento

### Queries de Monitoramento

Execute `06_monitoring_queries.sql` para:
- Status do Snowpipe
- Execuções recentes
- Status das Tasks
- Contagem de dados
- Erros recentes

### Verificações Automáticas

```sql
-- Status do Snowpipe
SELECT PIPE_STATE FROM INFORMATION_SCHEMA.PIPES 
WHERE PIPE_NAME = '${SNOWPIPE_NAME}';

-- Status da Task
SELECT TASK_STATE FROM INFORMATION_SCHEMA.TASKS 
WHERE TASK_NAME = '${TASK_NAME}';
```

## 🛠️ Troubleshooting

### Problema: Arquivo config.env não encontrado
```bash
# Solução
cp config.env.example config.env
# Edite o arquivo com suas credenciais
```

### Problema: Variáveis faltando
```bash
# Verifique se todas as variáveis estão no config.env
python3 generate_sql.py
```

### Problema: Erro de conexão
```sql
-- Verifique as credenciais no Snowflake
SELECT CURRENT_USER(), CURRENT_ACCOUNT();
```

## 🔐 Segurança Avançada

### Para Ambientes de Produção

1. **Use variáveis de ambiente do sistema**:
   ```bash
   export SNOWFLAKE_PASSWORD="senha_segura"
   ```

2. **Use Azure Key Vault** para armazenar secrets

3. **Use Azure Managed Identity** para autenticação

4. **Rotacione tokens SAS** regularmente

### Para CI/CD

1. **Configure secrets no pipeline**:
   ```yaml
   - name: Generate SQL
     env:
       SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
     run: python3 generate_sql.py
   ```

2. **Use Azure DevOps Variable Groups**

3. **Use GitHub Secrets**

## 📈 Vantagens da Configuração Dinâmica

- ✅ **Segurança**: Senhas não ficam no código
- ✅ **Flexibilidade**: Fácil mudança de configurações
- ✅ **Reutilização**: Mesmo código para diferentes ambientes
- ✅ **Versionamento**: Código seguro para Git
- ✅ **Automação**: Fácil integração com CI/CD

## 🎯 Próximos Passos

1. **Configure o `config.env`** com suas credenciais
2. **Execute `python3 generate_sql.py`**
3. **Execute o deploy no Snowflake**
4. **Configure o Azure Event Grid**
5. **Monitore com as queries fornecidas**

O sistema está pronto para uso seguro em produção! 🚀 
