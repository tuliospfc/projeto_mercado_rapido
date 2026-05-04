#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

# Resetar manualmente as tabelas
with connection.cursor() as cursor:
    # Verificar estrutura atual
    cursor.execute("PRAGMA table_info(compras_itemcompra)")
    columns = cursor.fetchall()
    print("Colunas atuais da tabela compras_itemcompra:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    # Remover tabela Categoria se existir
    try:
        cursor.execute("DROP TABLE compras_categoria")
        print("Tabela compras_categoria removida")
    except:
        print("Tabela compras_categoria não existe")
    
    # Verificar se existe coluna categoria
    has_categoria = any(col[1] == 'categoria' for col in columns)
    if has_categoria:
        # SQLite não suporta DROP COLUMN diretamente, precisamos recriar a tabela
        cursor.execute("CREATE TABLE compras_itemcompra_temp AS SELECT id, lista_id, nome, quantidade, comprado, observacao, criado_em FROM compras_itemcompra")
        cursor.execute("DROP TABLE compras_itemcompra")
        cursor.execute("ALTER TABLE compras_itemcompra_temp RENAME TO compras_itemcompra")
        print("Coluna categoria removida da tabela compras_itemcompra")
    else:
        print("Coluna categoria não encontrada na tabela compras_itemcompra")

print("Reset concluído!")
