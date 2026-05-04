#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

# Corrigir dados inválidos na tabela antes da migração
with connection.cursor() as cursor:
    # Verificar se há valores inválidos no campo categoria_id
    cursor.execute("SELECT COUNT(*) FROM compras_itemcompra WHERE categoria_id NOT NULL AND NOT EXISTS (SELECT 1 FROM sqlite_master WHERE type='table' AND name='compras_categoria')")
    count = cursor.fetchone()[0]
    print(f"Encontrados {count} itens com categoria_id inválido")
    
    # Limpar valores inválidos
    cursor.execute("UPDATE compras_itemcompra SET categoria_id = NULL WHERE categoria_id NOT NULL AND NOT EXISTS (SELECT 1 FROM sqlite_master WHERE type='table' AND name='compras_categoria')")
    print("Valores inválidos limpos com sucesso!")

print("Fix de migração concluído!")
