from django.urls import path
from ygo_deck_builder import views

urlpatterns = [
    path('', views.card_search, name='card_search'),
    path('card_info/', views.card_info, name='card_info'),
    path('all_cards/', views.all_cards, name='all_cards'),
    path('decks/', views.list_decks, name='list_decks'),
    path('decks/create/', views.create_or_edit_deck, name='create_deck'),  # URL para criar um novo deck
    path('decks/<int:deck_id>/edit/', views.create_or_edit_deck, name='edit_deck'),  # URL para editar um deck existente
    path('decks/<int:deck_id>/delete/', views.delete_deck, name='delete_deck'),  # URL para excluir um deck existente
]