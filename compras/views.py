from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ItemCompraForm, ListaCompraMensalForm
from .models import ItemCompra, ListaCompraMensal


@login_required
def lista_list(request):
    listas = ListaCompraMensal.objects.prefetch_related('itens').all()
    return render(request, 'compras/lista_list.html', {'listas': listas})


@login_required
def lista_create(request):
    if request.method == 'POST':
        form = ListaCompraMensalForm(request.POST)
        if form.is_valid():
            lista = form.save()
            messages.success(request, 'Lista mensal criada com sucesso.')
            return redirect('compras:lista_detail', lista_id=lista.id)
    else:
        form = ListaCompraMensalForm()

    return render(request, 'compras/lista_form.html', {'form': form})


@login_required
def lista_detail(request, lista_id):
    lista = get_object_or_404(ListaCompraMensal.objects.prefetch_related('itens'), id=lista_id)
    
    # Obter parâmetro de ordenação
    ordenacao = request.GET.get('ordenacao', 'padrao')
    
    # Ordenar itens conforme seleção
    if ordenacao == 'categoria':
        itens = lista.itens.all().order_by('categoria__nome', 'comprado', 'nome')
    elif ordenacao == 'nome':
        itens = lista.itens.all().order_by('nome', 'comprado')
    else:  # padrão
        itens = lista.itens.all()
    
    # Opções de ordenação
    opcoes_ordenacao = [
        ('padrao', 'Padrão (comprados primeiro)'),
        ('categoria', 'Por categoria'),
        ('nome', 'Por nome'),
    ]

    if request.method == 'POST':
        form = ItemCompraForm(request.POST, lista=lista)
        if form.is_valid():
            item = form.save(commit=False)
            item.lista = lista
            item.save()
            messages.success(request, 'Item adicionado com sucesso.')
            return redirect('compras:lista_detail', lista_id=lista.id)
    else:
        form = ItemCompraForm(lista=lista)

    return render(request, 'compras/lista_detalhe.html', {
        'lista': lista, 
        'form': form, 
        'itens': itens,
        'ordenacao': ordenacao,
        'opcoes_ordenacao': opcoes_ordenacao
    })


@login_required
def item_toggle_comprado(request, item_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    item = get_object_or_404(ItemCompra, id=item_id)
    item.comprado = not item.comprado
    item.save(update_fields=['comprado'])

    if item.comprado:
        messages.success(request, f'Item "{item.nome}" marcado como comprado.')
    else:
        messages.warning(request, f'Item "{item.nome}" foi marcado como pendente.')

    return redirect('compras:lista_detail', lista_id=item.lista.id)


@login_required
def limpar_comprados(request, lista_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    lista = get_object_or_404(ListaCompraMensal, id=lista_id)
    itens_comprados = lista.itens.filter(comprado=True)
    count = itens_comprados.count()
    itens_comprados.delete()
    messages.success(request, f'{count} item(ns) comprado(s) removido(s) com sucesso.')
    return redirect('compras:lista_detail', lista_id=lista_id)


@login_required
def desmarcar_todos(request, lista_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    lista = get_object_or_404(ListaCompraMensal, id=lista_id)
    itens_comprados = lista.itens.filter(comprado=True)
    count = itens_comprados.count()
    itens_comprados.update(comprado=False)
    messages.success(request, f'{count} item(ns) desmarcado(s) com sucesso.')
    return redirect('compras:lista_detail', lista_id=lista_id)


@login_required
def marcar_todos(request, lista_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    lista = get_object_or_404(ListaCompraMensal, id=lista_id)
    itens_pendentes = lista.itens.filter(comprado=False)
    count = itens_pendentes.count()
    itens_pendentes.update(comprado=True)
    messages.success(request, f'{count} item(ns) marcado(s) como comprado(s) com sucesso.')
    return redirect('compras:lista_detail', lista_id=lista_id)


@login_required
def item_delete(request, item_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    item = get_object_or_404(ItemCompra, id=item_id)
    lista_id = item.lista.id
    nome_item = item.nome
    item.delete()
    messages.success(request, f'Item "{nome_item}" removido com sucesso.')
    return redirect('compras:lista_detail', lista_id=lista_id)


@login_required
def lista_delete(request, lista_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    lista = get_object_or_404(ListaCompraMensal, id=lista_id)
    nome_lista = str(lista)
    lista.delete()
    messages.success(request, f'Lista "{nome_lista}" removida com sucesso.')
    return redirect('compras:lista_list')
