from django.urls import path
from ygo_deck_builder import views

urlpatterns = [
    path('', views.card_search, name='card_search'),
    path('card_info/', views.card_info, name='card_info'),
    path('all_cards/', views.all_cards, name='all_cards'),
]