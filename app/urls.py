from django.urls import path
from ygo_deck_builder import views

urlpatterns = [
    path('', views.list_decks, name='list_decks'),
    path('create/', views.create_or_edit_deck, name='create_or_edit_deck'),
    path('edit/<int:deck_id>/', views.create_or_edit_deck, name='create_or_edit_deck'),
    path('delete/<int:deck_id>/', views.delete_deck, name='delete_deck'),
    path('view/<int:deck_id>/', views.view_deck, name='view_deck'),
    path('card_info/', views.card_info, name='card_info'),
    path('card_search/', views.card_search, name='card_search'),
    path('sync_cards/', views.sync_cards, name='sync_cards'),
]