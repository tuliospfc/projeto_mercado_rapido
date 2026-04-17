from django.test import TestCase
from django.urls import reverse

from .models import ItemCompra, ListaCompraMensal


class ComprasTests(TestCase):
    def setUp(self):
        self.lista = ListaCompraMensal.objects.create(mes=4, ano=2026)
        self.item = ItemCompra.objects.create(lista=self.lista, nome='Arroz', quantidade='2 pacotes')
        self.item_comprado = ItemCompra.objects.create(lista=self.lista, nome='Feijão', quantidade='1 pacote', comprado=True)

    def test_criar_lista_mensal(self):
        response = self.client.post(
            reverse('compras:lista_create'),
            data={'mes': 5, 'ano': 2026}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ListaCompraMensal.objects.filter(mes=5, ano=2026).exists())

    def test_criar_item_na_lista(self):
        response = self.client.post(
            reverse('compras:lista_detail', kwargs={'lista_id': self.lista.id}),
            data={'nome': 'Macarrão', 'quantidade': '1 pacote', 'observacao': 'tipo 00'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ItemCompra.objects.filter(nome='Macarrão').exists())

    def test_evitar_item_duplicado(self):
        response = self.client.post(
            reverse('compras:lista_detail', kwargs={'lista_id': self.lista.id}),
            data={'nome': 'arroz', 'quantidade': '3 pacotes'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Já existe um item com este nome nesta lista.')
        self.assertEqual(ItemCompra.objects.filter(nome__iexact='arroz').count(), 1)

    def test_marcar_e_desmarcar_item(self):
        response = self.client.post(reverse('compras:item_toggle', kwargs={'item_id': self.item.id}))
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertTrue(self.item.comprado)

        response = self.client.post(reverse('compras:item_toggle', kwargs={'item_id': self.item.id}))
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertFalse(self.item.comprado)

    def test_excluir_item(self):
        response = self.client.post(reverse('compras:item_delete', kwargs={'item_id': self.item.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ItemCompra.objects.filter(id=self.item.id).exists())

    def test_limpar_itens_comprados(self):
        response = self.client.post(reverse('compras:limpar_comprados', kwargs={'lista_id': self.lista.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ItemCompra.objects.filter(lista=self.lista, comprado=True).exists())
        self.assertTrue(ItemCompra.objects.filter(lista=self.lista, comprado=False).exists())

    def test_propriedades_da_lista(self):
        self.assertEqual(self.lista.total_itens, 2)
        self.assertEqual(self.lista.total_comprados, 1)
        self.assertEqual(self.lista.total_pendentes, 1)

    def test_nome_personalizado_lista(self):
        self.lista.nome_customizado = 'lista generica'
        self.lista.save()
        self.assertEqual(str(self.lista), 'lista generica')

    def test_desmarcar_todos_itens(self):
        # Marcar alguns itens como comprados
        self.item.comprado = True
        self.item.save()
        self.item_comprado.comprado = True
        self.item_comprado.save()
        
        # Verificar que existem itens comprados
        self.assertEqual(self.lista.total_comprados, 2)
        
        # Desmarcar todos
        response = self.client.post(reverse('compras:desmarcar_todos', kwargs={'lista_id': self.lista.id}))
        self.assertEqual(response.status_code, 302)
        
        # Verificar que todos foram desmarcados
        self.lista.refresh_from_db()
        self.assertEqual(self.lista.total_comprados, 0)
        self.assertEqual(self.lista.total_pendentes, 2)

    def test_list_view(self):
        # Configurar nome personalizado para o teste
        self.lista.nome_customizado = 'lista generica'
        self.lista.save()
        
        response = self.client.get(reverse('compras:lista_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lista generica')
        self.assertContains(response, 'Total de itens: 2')
