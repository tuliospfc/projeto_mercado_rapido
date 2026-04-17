from django.core.validators import MinValueValidator
from django.db import models


class ListaCompraMensal(models.Model):
    MESES = [
        (1, 'Janeiro'),
        (2, 'Fevereiro'),
        (3, 'Março'),
        (4, 'Abril'),
        (5, 'Maio'),
        (6, 'Junho'),
        (7, 'Julho'),
        (8, 'Agosto'),
        (9, 'Setembro'),
        (10, 'Outubro'),
        (11, 'Novembro'),
        (12, 'Dezembro'),
    ]

    mes = models.PositiveSmallIntegerField(choices=MESES, verbose_name='Mês')
    ano = models.PositiveSmallIntegerField(validators=[MinValueValidator(2020)], verbose_name='Ano')
    nome_customizado = models.CharField(max_length=100, blank=True, verbose_name='Nome personalizado')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['mes', 'ano'], name='unique_mes_ano_lista_compra')
        ]
        ordering = ['-ano', '-mes']
        verbose_name = 'Lista de compra mensal'
        verbose_name_plural = 'Listas de compra mensais'

    def __str__(self):
        return self.nome_customizado if self.nome_customizado else f'{self.get_mes_display()}/{self.ano}'

    @property
    def total_itens(self):
        return self.itens.count()

    @property
    def total_comprados(self):
        return self.itens.filter(comprado=True).count()

    @property
    def total_pendentes(self):
        return self.itens.filter(comprado=False).count()


class ItemCompra(models.Model):
    lista = models.ForeignKey(ListaCompraMensal, on_delete=models.CASCADE, related_name='itens', verbose_name='Lista')
    nome = models.CharField(max_length=100, verbose_name='Nome do item')
    quantidade = models.CharField(max_length=50, blank=True, verbose_name='Quantidade')
    comprado = models.BooleanField(default=False, verbose_name='Comprado')
    observacao = models.CharField(max_length=150, blank=True, verbose_name='Observação')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        ordering = ['comprado', 'nome']
        verbose_name = 'Item de compra'
        verbose_name_plural = 'Itens de compra'

    def __str__(self):
        return self.nome
