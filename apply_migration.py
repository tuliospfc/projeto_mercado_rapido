#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

# Aplicar a migração manualmente
with connection.cursor() as cursor:
    # Criar tabela Categoria
    cursor.execute("""
        CREATE TABLE "compras_categoria" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
            "nome" varchar(50) NOT NULL UNIQUE, 
            "cor" varchar(7) NOT NULL, 
            "criado_em" datetime NOT NULL
        )
    """)
    print("Tabela compras_categoria criada")
    
    # Criar nova tabela ItemCompra com categoria_id
    cursor.execute("""
        CREATE TABLE "new__compras_itemcompra" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
            "nome" varchar(100) NOT NULL, 
            "quantidade" varchar(50) NOT NULL, 
            "comprado" bool NOT NULL, 
            "observacao" varchar(150) NOT NULL, 
            "criado_em" datetime NOT NULL, 
            "lista_id" bigint NOT NULL REFERENCES "compras_listacompramensal" ("id") DEFERRABLE INITIALLY DEFERRED, 
            "categoria_id" bigint NULL REFERENCES "compras_categoria" ("id") DEFERRABLE INITIALLY DEFERRED
        )
    """)
    print("Nova tabela compras_itemcompra criada")
    
    # Migrar dados (categoria_id será NULL pois não há correspondência)
    cursor.execute("""
        INSERT INTO "new__compras_itemcompra" 
        ("id", "nome", "quantidade", "comprado", "observacao", "criado_em", "lista_id", "categoria_id") 
        SELECT "id", "nome", "quantidade", "comprado", "observacao", "criado_em", "lista_id", NULL 
        FROM "compras_itemcompra"
    """)
    print("Dados migrados")
    
    # Substituir tabela antiga
    cursor.execute('DROP TABLE "compras_itemcompra"')
    cursor.execute('ALTER TABLE "new__compras_itemcompra" RENAME TO "compras_itemcompra"')
    print("Tabela substituída")
    
    # Criar índices
    cursor.execute('CREATE INDEX "compras_itemcompra_lista_id_3d7e12ef" ON "compras_itemcompra" ("lista_id")')
    cursor.execute('CREATE INDEX "compras_itemcompra_categoria_id_79ab172a" ON "compras_itemcompra" ("categoria_id")')
    print("Índices criados")

print("Migração aplicada com sucesso!")
