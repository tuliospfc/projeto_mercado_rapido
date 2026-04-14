from django import forms
from .models import ItemCompra, ListaCompraMensal


class ListaCompraMensalForm(forms.ModelForm):
    class Meta:
        model = ListaCompraMensal
        fields = ['mes', 'ano']
        widgets = {
            'mes': forms.Select(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: 2026'}),
        }


class ItemCompraForm(forms.ModelForm):
    class Meta:
        model = ItemCompra
        fields = ['nome', 'quantidade', 'observacao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Arroz'}),
            'quantidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: 2 pacotes'}),
            'observacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: marca preferida'}),
        }

    def __init__(self, *args, **kwargs):
        self.lista = kwargs.pop('lista', None)
        super().__init__(*args, **kwargs)

    def clean_nome(self):
        nome = self.cleaned_data['nome']
        if self.lista and ItemCompra.objects.filter(lista=self.lista, nome__iexact=nome.strip()).exists():
            raise forms.ValidationError('Já existe um item com este nome nesta lista.')
        return nome.strip()
