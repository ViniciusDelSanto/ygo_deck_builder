import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Deck

def card_info(request):
    card_name = request.GET.get('card_name')
    if card_name:
        url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
        params = {'name': card_name}
        response = requests.get(url, params=params)
        data = response.json()
        # Verifica se a chave 'data' existe nos dados da API
        if 'data' in data:
            # Retorna os dados corretos para o template
            return render(request, 'card_info.html', {'cards_data': data['data'], 'searched_card': card_name})
    # Se não houver dados ou se não for especificado um nome de carta, renderiza o template de busca
    return render(request, 'card_search.html')
    
def card_search(request):
    return render(request, 'card_search.html')

def all_cards(request):
    url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
    response = requests.get(url)
    data = response.json()
    card_names = [card['name'] for card in data['data']]
    return render(request, 'all_cards.html', {'card_names': card_names})

def list_decks(request):
    decks = Deck.objects.all() 
    return render(request, 'list_decks.html', {'decks': decks})

def create_or_edit_deck(request, deck_id=None):
    deck = None
    if deck_id:
        deck = get_object_or_404(Deck, id=deck_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if deck:
            deck.name = name
            deck.save()
        else:
            Deck.objects.create(name=name)
        return redirect('list_decks')
    
    # Obter todos os cards da API para exibir na div da direita
    url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
    response = requests.get(url)
    cards_data = response.json()['data']
    card_names = [card['name'] for card in cards_data]

    return render(request, 'create_edit_deck.html', {'deck': deck, 'card_names': card_names})


def delete_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    if request.method == 'POST':
        deck.delete()
        return redirect('list_decks')
    return render(request, 'delete_deck.html', {'deck': deck})