from django.urls import path
from . import views

app_name = 'decks'

urlpatterns = [
    path('', views.index, name='index'),
    path('criar/', views.criar_deck, name='criar_deck'),
    path('<int:deck_id>/editar/', views.editar_deck, name='editar_deck'),
    path('<int:deck_id>/deletar/', views.deletar_deck, name='deletar_deck'),
]