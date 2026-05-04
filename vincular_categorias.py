#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from compras.models import ItemCompra, Categoria

# Mapeamento de palavras-chave para categorias
mapeamento_categorias = {
    'Alimentos': ['arroz', 'feijão', 'macarrão', 'açúcar', 'sal', 'óleo', 'farinha', 'pão', 'bolacha', 'biscoito', 'café', 'chá', 'milho', 'ervilha', 'grão', 'soja', 'trigo', 'aveia', 'corn flakes'],
    'Higiene Pessoal': ['sabonete', 'shampoo', 'condicionador', 'pasta de dente', 'escova de dente', 'desodorante', 'sabão em pó', 'sabão', 'papel higiênico', 'lenço umedecido', 'creme', 'loção', 'perfume', 'colon'],
    'Limpeza': ['detergente', 'limpador', 'multiuso', 'alvejante', 'desinfetante', 'lava-roupas', 'amaciante', 'saco de lixo', 'pano', 'esponja', 'palha de aço', 'cera', 'vinagre', 'bucha'],
    'Bebidas': ['água', 'refrigerante', 'suco', 'leite', 'cerveja', 'vinho', 'energético', ' isotônico'],
    'Padaria': ['pão', 'bolacha', 'biscoito', 'rosca', 'croissant', 'pão de queijo', 'torta', 'bolo', 'salgado'],
    'Frutas e Verduras': ['banana', 'maçã', 'laranja', 'limão', 'tomate', 'cebola', 'batata', 'cenoura', 'alface', 'couve', 'brócolis', 'morango', 'uva', 'melancia', 'abacaxi'],
    'Carnes': ['carne', 'frango', 'boi', 'porco', 'peixe', 'salsicha', 'linguiça', 'hambúrguer', 'bife', 'filé', 'contrafilé', 'picanha', 'costela'],
    'Laticínios': ['leite', 'queijo', 'manteiga', 'margarina', 'iogurte', 'requeijão', 'creme de leite', 'coalhada'],
    'Mercearia': ['feijão', 'arroz', 'macarrão', 'açúcar', 'sal', 'óleo', 'farinha', 'café', 'chá', 'tempero', 'molho', 'conserva'],
    'Congelados': ['pizza', 'sorvete', 'hambúrguer', 'nuggets', 'batata frita', 'lasanha', 'pastel', 'empada'],
}

print("Vinculando categorias aos itens existentes...")

# Obter todos os itens sem categoria
itens_sem_categoria = ItemCompra.objects.filter(categoria__isnull=True)
total_itens = itens_sem_categoria.count()
print(f"Encontrados {total_itens} itens sem categoria")

vinculados = 0

for item in itens_sem_categoria:
    nome_lower = item.nome.lower()
    categoria_encontrada = None
    
    # Procurar categoria correspondente
    for categoria_nome, palavras_chave in mapeamento_categorias.items():
        for palavra in palavras_chave:
            if palavra in nome_lower:
                categoria_encontrada = Categoria.objects.get(nome=categoria_nome)
                break
        if categoria_encontrada:
            break
    
    # Se não encontrar categoria específica, atribuir "Outros"
    if not categoria_encontrada:
        categoria_encontrada = Categoria.objects.get(nome="Outros")
    
    # Vincular categoria ao item
    item.categoria = categoria_encontrada
    item.save()
    vinculados += 1
    
    print(f"Item '{item.nome}' -> {categoria_encontrada.nome}")

print(f"\nProcesso concluído!")
print(f"Total de itens vinculados: {vinculados}/{total_itens}")

# Exibir estatísticas
print("\nEstatísticas por categoria:")
for categoria in Categoria.objects.all():
    count = ItemCompra.objects.filter(categoria=categoria).count()
    if count > 0:
        print(f"  {categoria.nome}: {count} itens")
