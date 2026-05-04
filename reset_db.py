#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

# Resetar a migração problemática
with connection.cursor() as cursor:
    # Remover a tabela Categoria se existir
    cursor.execute("DROP TABLE IF EXISTS compras_categoria")
    
    # Remover a coluna categoria da tabela ItemCompra se existir
    cursor.execute("ALTER TABLE compras_itemcompra DROP COLUMN IF EXISTS categoria")
    
    print("Tabelas resetadas com sucesso!")

print("Reset concluído!")
