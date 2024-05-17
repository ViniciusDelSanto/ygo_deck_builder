from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Deck, Card
from .forms import DeckForm
import requests



def card_list(request):
    url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
    response = requests.get(url)
    cards = response.json()['data'] 
    context = {'cards': cards}
    return render(request, 'card_list.html', context)


def card_info(request):
    card_name = request.GET.get('card_name')
    if card_name:
        try:
            # Busca a carta no banco de dados
            card = Card.objects.get(name=card_name)
            return render(request, 'card_info.html', {'cards_data': [card]})
        except Card.DoesNotExist:
            # Se a carta não existir no banco de dados, busca na API
            url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
            params = {'name': card_name}
            response = requests.get(url, params=params)
            data = response.json()
            if 'data' in data:
                return render(request, 'card_info.html', {'cards_data': data['data'], 'searched_card': card_name})
    return render(request, 'card_search.html')

def card_search(request):
    return render(request, 'card_search.html')

def sync_cards(request):
    url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
    response = requests.get(url)
    data = response.json()
    cards_data = data['data']

    for card_data in cards_data:
        card, created = Card.objects.get_or_create(
            name=card_data['name'],
            defaults={
                'type': card_data['type'],
                'atk': card_data.get('atk'),
                'defense': card_data.get('def'),
                'level': card_data.get('level'),
                'race': card_data['race'],
                'attribute': card_data['attribute'],
                'desc': card_data['desc'],
                'image_url': card_data['card_images'][0]['image_url'],  # Salva a URL da imagem
            }
        )
    messages.success(request, 'Cartas sincronizadas com sucesso!')
    return redirect('list_decks')

def list_decks(request):
    decks = Deck.objects.all()
    return render(request, 'list_decks.html', {'decks': decks})

def create_or_edit_deck(request, deck_id=None):
    deck = None
    if deck_id:
        deck = get_object_or_404(Deck, id=deck_id)
    if request.method == 'POST':
        form = DeckForm(request.POST, instance=deck)
        if form.is_valid():
            deck = form.save()
            messages.success(request, 'Deck salvo com sucesso!')
            return redirect('list_decks')
    else:
        form = DeckForm(instance=deck)
    cards = Card.objects.all()
    return render(request, 'create_edit_deck.html', {'deck': deck, 'form': form, 'cards': cards})

def delete_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    if request.method == 'POST':
        deck.delete()
        return redirect('list_decks')
    return render(request, 'delete_deck.html', {'deck': deck})

def view_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    return render(request, 'view_deck.html', {'deck': deck})