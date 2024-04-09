from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from collections import Counter
from .models import Deck
from .forms import DeckForm
import requests

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
    card_name = None

    if deck_id:
        deck = get_object_or_404(Deck, id=deck_id)

    if request.method == 'POST':
        form = DeckForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            main_deck = form.cleaned_data['main_deck']
            extra_deck = form.cleaned_data['extra_deck']
            side_deck = form.cleaned_data['side_deck']

            # Validação do Main Deck
            if main_deck and (len(main_deck) < 40 or len(main_deck) > 60):
                messages.error(request, 'O Main Deck deve conter entre 40 e 60 cartas.')
                return redirect('create_or_edit_deck')

            # Verifica se há mais de 3 cartas com o mesmo nome no Main Deck
            if main_deck:
                main_deck_counts = Counter(main_deck)
                for card_name, count in main_deck_counts.items():
                    if count > 3:
                        messages.error(request, f'Só é permitido até 3 cartas com o mesmo nome no Main Deck: {card_name}.')
                        return redirect('create_or_edit_deck')

            # Validação do Extra Deck
            if extra_deck and len(extra_deck) > 15:
                messages.error(request, 'O Extra Deck deve conter no máximo 15 cartas.')
                return redirect('create_or_edit_deck')

            # Validação do Side Deck
            if side_deck and len(side_deck) > 15:
                messages.error(request, 'O Side Deck deve conter no máximo 15 cartas.')
                return redirect('create_or_edit_deck')

            # Verifica se há monstros proibidos nos decks
            forbidden_monsters = ['Fusion', 'Xyz', 'Synchro', 'Link']
            for monster_type in forbidden_monsters:
                if main_deck and any(monster_type in card for card in main_deck):
                    messages.error(request, f'Não são permitidos monstros do tipo {monster_type} no Main Deck.')
                    return redirect('create_or_edit_deck')

                if extra_deck and any(monster_type in card for card in extra_deck):
                    messages.error(request, f'Somente monstros do tipo {monster_type} são permitidos no Extra Deck.')
                    return redirect('create_or_edit_deck')

                if side_deck and any(monster_type in card for card in side_deck):
                    messages.error(request, f'Não são permitidos monstros do tipo {monster_type} no Side Deck.')
                    return redirect('create_or_edit_deck')

            if deck:
                deck.name = name
                deck.save()
            else:
                Deck.objects.create(name=name)
            return redirect('list_decks')
        else:
            print("Formulário inválido:", form.errors)
            messages.error(request, "Erro no formulário. Por favor, verifique os dados inseridos.")
    else:
        form = DeckForm()

    if 'card_name' in request.GET:
        card_name = request.GET.get('card_name')
        url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
        params = {'name': card_name}
        response = requests.get(url, params=params)
        data = response.json()
        if 'data' in data:
            return render(request, 'card_info.html', {'cards_data': data['data'], 'searched_card': card_name})

    url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
    response = requests.get(url)
    cards_data = response.json()['data']
    card_names = [card['name'] for card in cards_data]

    return render(request, 'create_edit_deck.html', {'deck': deck, 'form': form, 'card_names': card_names, 'searched_card': card_name})

def delete_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    if request.method == 'POST':
        deck.delete()
        return redirect('list_decks')
    return render(request, 'delete_deck.html', {'deck': deck})