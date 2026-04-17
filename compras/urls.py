from django.urls import path
from . import views

app_name = 'compras'

urlpatterns = [
    path('', views.lista_list, name='lista_list'),
    path('nova/', views.lista_create, name='lista_create'),
    path('<int:lista_id>/', views.lista_detail, name='lista_detail'),
    path('<int:lista_id>/delete/', views.lista_delete, name='lista_delete'),
    path('<int:lista_id>/limpar-comprados/', views.limpar_comprados, name='limpar_comprados'),
    path('<int:lista_id>/desmarcar-todos/', views.desmarcar_todos, name='desmarcar_todos'),
    path('item/<int:item_id>/toggle/', views.item_toggle_comprado, name='item_toggle'),
    path('item/<int:item_id>/delete/', views.item_delete, name='item_delete'),
]
