#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from compras.models import Categoria

# Categorias padrão
categorias_padrao = [
    {'nome': 'Alimentos', 'cor': '#28a745'},
    {'nome': 'Higiene Pessoal', 'cor': '#17a2b8'},
    {'nome': 'Limpeza', 'cor': '#6f42c1'},
    {'nome': 'Bebidas', 'cor': '#fd7e14'},
    {'nome': 'Padaria', 'cor': '#ffc107'},
    {'nome': 'Frutas e Verduras', 'cor': '#20c997'},
    {'nome': 'Carnes', 'cor': '#dc3545'},
    {'nome': 'Laticínios', 'cor': '#6c757d'},
    {'nome': 'Mercearia', 'cor': '#343a40'},
    {'nome': 'Congelados', 'cor': '#007bff'},
    {'nome': 'Outros', 'cor': '#e83e8c'},
]

print("Criando categorias padrão...")
for cat_data in categorias_padrao:
    categoria, created = Categoria.objects.get_or_create(
        nome=cat_data['nome'],
        defaults={'cor': cat_data['cor']}
    )
    if created:
        print(f"Categoria '{categoria.nome}' criada com sucesso!")
    else:
        print(f"Categoria '{categoria.nome}' já existe.")

print("\nCategorias criadas com sucesso!")
