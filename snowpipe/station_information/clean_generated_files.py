#!/usr/bin/env python3
"""
Script para limpar arquivos SQL gerados dinamicamente
Mantém apenas os templates e arquivos de configuração
"""

import os
import glob

def clean_generated_files():
    """Remove arquivos SQL gerados dinamicamente"""
    
    # Arquivos que devem ser removidos (gerados dinamicamente)
    files_to_remove = [
        '01_create_stage.sql',
        '02_create_tables.sql', 
        '03_create_snowpipe.sql',
        '05_create_task.sql',
        'deploy_snowpipe.sql'
    ]
    
    print("🧹 Limpando arquivos gerados dinamicamente...")
    
    removed_count = 0
    for filename in files_to_remove:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"🗑️ Removido: {filename}")
            removed_count += 1
        else:
            print(f"ℹ️ Não encontrado: {filename}")
    
    print(f"\n✅ Limpeza concluída! {removed_count} arquivos removidos.")
    print("\n📁 Arquivos mantidos:")
    print("   - config.env.example (template de configuração)")
    print("   - config.env (configuração real - NÃO COMMITAR)")
    print("   - generate_sql.py (script de geração)")
    print("   - 04_create_stream.sql (fixo)")
    print("   - 06_monitoring_queries.sql (fixo)")
    print("   - 07_setup_azure_event_grid.sql (fixo)")
    print("   - README.md (documentação)")
    print("   - clean_generated_files.py (este script)")
    
    print("\n🔐 Lembre-se:")
    print("   - config.env NÃO deve ser commitado no Git")
    print("   - Use generate_sql.py para gerar os arquivos SQL")
    print("   - Use clean_generated_files.py para limpar após uso")

if __name__ == "__main__":
    clean_generated_files() 