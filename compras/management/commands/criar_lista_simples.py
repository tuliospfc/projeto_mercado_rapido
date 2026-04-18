from django.core.management.base import BaseCommand
from django.utils import timezone
from compras.models import ListaCompraMensal, ItemCompra


class Command(BaseCommand):
    help = 'Cria uma lista de compras simples apenas com nomes de itens básicos de casa'

    def handle(self, *args, **options):
        # Limpar dados existentes
        ItemCompra.objects.all().delete()
        ListaCompraMensal.objects.all().delete()
        self.stdout.write('Dados anteriores limpos!')
        
        # Obter mês e ano atual
        agora = timezone.now()
        mes_atual = agora.month
        ano_atual = agora.year
        
        # Criar nova lista
        lista = ListaCompraMensal.objects.create(
            mes=mes_atual,
            ano=ano_atual,
            nome_customizado=f'Compras {agora.strftime("%B/%Y")}'
        )
        self.stdout.write(f'Lista "{lista}" criada!')
        
        # Itens básicos de casa (apenas nome)
        itens_basicos = [
            # Alimentos básicos
            'Arroz', 'Feijão', 'Óleo', 'Açúcar', 'Sal', 'Café', 'Macarrão',
            'Farinha', 'Ovos', 'Pão', 'Manteiga', 'Leite', 'Tomate', 'Cebola',
            'Alho', 'Batata', 'Cenoura', 'Mandioca', 'Abóbora', 'Milho',
            
            # Carnes e frios
            'Carne bovina', 'Frango', 'Linguiça', 'Salsicha', 'Presunto',
            'Queijo', 'Mortadela', 'Salame', 'Bacon',
            
            # Bebidas
            'Refrigerante', 'Suco', 'Água', 'Cerveja', 'Vinho',
            
            # Frutas
            'Banana', 'Maçã', 'Laranja', 'Limão', 'Mamão', 'Uva', 'Morango',
            'Abacaxi', 'Melancia', 'Pera', 'Manga',
            
            # Legumes e verduras
            'Alface', 'Couve', 'Espinafre', 'Brócolis', 'Couve-flor',
            'Pimentão', 'Pepino', 'Berinjela', 'Abobrinha', 'Chuchu',
            
            # Limpeza
            'Detergente', 'Sabão em pó', 'Água sanitária', 'Desinfetante',
            'Limpador', 'Esponja', 'Saco de lixo', 'Papel toalha',
            'Vassoura', 'Rodo', 'Pá', 'Flanela', 'Panos de chão',
            
            # Higiene pessoal
            'Sabonete', 'Shampoo', 'Condicionador', 'Papel higiênico',
            'Creme dental', 'Escova dental', 'Desodorante', 'Absorvente',
            'Algodão', 'Álcool', 'Hastes flexíveis', 'Pente',
            
            # Cozinha
            'Fósforo', 'Isqueiro', 'Pilhas', 'Lâmpada', 'Filtro',
            'Guardanapo', 'Fósforo', 'Velas', 'Papel alumínio',
            'Filme plástico', 'Detergente lava-louças',
            
            # Crianças (se aplicável)
            'Fralda', 'Lenço umedecido', 'Shampoo infantil',
            'Sabonete infantil', 'Papel higiênico infantil',
            
            # Pet (se aplicável)
            'Ração', 'Areia', 'Petisco', 'Shampoo pet',
            
            # Outros
            'Pilhas AA', 'Pilhas AAA', 'Bateria', 'Extensão',
            'Fita adesiva', 'Tesoura', 'Caneta', 'Lápis',
        ]
        
        criados = 0
        for nome_item in itens_basicos:
            ItemCompra.objects.create(
                lista=lista,
                nome=nome_item,
                quantidade='',
                observacao='',
                comprado=False
            )
            criados += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n=== RESUMO ===\n'
                f'Lista: {lista}\n'
                f'Itens criados: {criados}\n'
                f'Total de itens: {lista.total_itens}\n'
                f'Itens pendentes: {lista.total_pendentes}'
            )
        )
        
        # Mostrar categorização
        self.stdout.write('\n=== ITENS POR CATEGORIA ===')
        alimentos = ['Arroz', 'Feijão', 'Óleo', 'Açúcar', 'Sal', 'Café', 'Macarrão', 'Farinha', 'Ovos', 'Pão', 'Manteiga', 'Leite', 'Tomate', 'Cebola', 'Alho', 'Batata', 'Cenoura', 'Mandioca', 'Abóbora', 'Milho']
        carnes = ['Carne bovina', 'Frango', 'Linguiça', 'Salsicha', 'Presunto', 'Queijo', 'Mortadela', 'Salame', 'Bacon']
        bebidas = ['Refrigerante', 'Suco', 'Água', 'Cerveja', 'Vinho']
        frutas = ['Banana', 'Maçã', 'Laranja', 'Limão', 'Mamão', 'Uva', 'Morango', 'Abacaxi', 'Melancia', 'Pera', 'Manga']
        legumes = ['Alface', 'Couve', 'Espinafre', 'Brócolis', 'Couve-flor', 'Pimentão', 'Pepino', 'Berinjela', 'Abobrinha', 'Chuchu']
        limpeza = ['Detergente', 'Sabão em pó', 'Água sanitária', 'Desinfetante', 'Limpador', 'Esponja', 'Saco de lixo', 'Papel toalha', 'Vassoura', 'Rodo', 'Pá', 'Flanela', 'Panos de chão']
        higiene = ['Sabonete', 'Shampoo', 'Condicionador', 'Papel higiênico', 'Creme dental', 'Escova dental', 'Desodorante', 'Absorvente', 'Algodão', 'Álcool', 'Hastes flexíveis', 'Pente']
        cozinha = ['Fósforo', 'Isqueiro', 'Pilhas', 'Lâmpada', 'Filtro', 'Guardanapo', 'Fósforo', 'Velas', 'Papel alumínio', 'Filme plástico', 'Detergente lava-louças']
        
        categorias = {
            'Alimentos básicos': alimentos,
            'Carnes e frios': carnes,
            'Bebidas': bebidas,
            'Frutas': frutas,
            'Legumes e verduras': legumes,
            'Limpeza': limpeza,
            'Higiene pessoal': higiene,
            'Cozinha e utilidades': cozinha
        }
        
        for categoria, itens in categorias.items():
            self.stdout.write(f'\n{categoria} ({len(itens)}):')
            for item in itens[:5]:  # Mostra apenas 5 itens por categoria
                self.stdout.write(f'  - {item}')
            if len(itens) > 5:
                self.stdout.write(f'  ... e mais {len(itens) - 5} itens')
