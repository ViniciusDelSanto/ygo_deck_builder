from django.shortcuts import render, redirect, get_object_or_404
from .models import Deck, Carta
import requests

def buscar_cartas(request):
    """Busca cartas da API do YGOProDeck."""
    url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
    response = requests.get(url)
    data = response.json()
    return data['data']

def index(request):
    """Exibe a lista de decks."""
    decks = Deck.objects.all()
    return render(request, 'decks/index.html', {'decks': decks})

def criar_deck(request):
    """Cria um novo deck."""
    if request.method == 'POST':
        nome = request.POST['nome']
        deck = Deck.objects.create(nome=nome)
        return redirect('decks:editar_deck', deck_id=deck.id)
    else:
        cartas = buscar_cartas(request)
        return render(request, 'decks/criar_deck.html', {'cartas': cartas})

def editar_deck(request, deck_id):
    """Edita um deck existente."""
    deck = get_object_or_404(Deck, pk=deck_id)
    cartas = buscar_cartas(request)
    errors = []

    if request.method == 'POST':
        main_deck_cartas = request.POST.getlist('main_deck_cartas[]')
        extra_deck_cartas = request.POST.getlist('extra_deck_cartas[]')
        side_deck_cartas = request.POST.getlist('side_deck_cartas[]')

        deck.main_deck.clear()
        deck.extra_deck.clear()
        deck.side_deck.clear()

        for carta_api_id in main_deck_cartas:
            carta = Carta.objects.get(api_id=carta_api_id)
            deck.main_deck.add(carta)

        for carta_api_id in extra_deck_cartas:
            carta = Carta.objects.get(api_id=carta_api_id)
            deck.extra_deck.add(carta)

        for carta_api_id in side_deck_cartas:
            carta = Carta.objects.get(api_id=carta_api_id)
            deck.side_deck.add(carta)

        if not validar_deck(deck):
            return redirect('decks:index')
            # return render(request, 'decks/editar_deck.html', {'deck': deck, 'cartas': cartas, 'errors': errors})

        deck.save()  # Salva as alterações no banco de dados
        return redirect('decks:index')

    return render(request, 'decks/editar_deck.html', {'deck': deck, 'cartas': cartas, 'errors': errors})

def deletar_deck(request, deck_id):
    """Deleta um deck."""
    deck = get_object_or_404(Deck, pk=deck_id)
    deck.delete()
    return redirect('decks:index')

def validar_deck(deck):
    """Valida as regras do deck."""
    errors = []
    main_count = deck.main_deck.count()
    extra_count = deck.extra_deck.count()
    side_count = deck.side_deck.count()

    if not 40 <= main_count <= 60:
        errors.append('O Main Deck deve ter entre 40 e 60 cartas.')

    for carta in deck.main_deck.all():
        if carta.tipo in ['Fusion Monster', 'XYZ Monster', 'Synchro Monster', 'Link Monster']:
            errors.append(f'Carta inválida no Main Deck: {carta.nome}')

    for carta in deck.extra_deck.all():
        if carta.tipo not in ['Fusion Monster', 'XYZ Monster', 'Synchro Monster', 'Link Monster']:
            errors.append(f'Carta inválida no Extra Deck: {carta.nome}')

    if not 0 <= extra_count <= 15:
        errors.append('O Extra Deck deve ter entre 0 e 15 cartas.')

    if not 0 <= side_count <= 15:
        errors.append('O Side Deck deve ter entre 0 e 15 cartas.')

    # Validação de cartas repetidas:
    for deck_type in ['main_deck', 'extra_deck', 'side_deck']:
        cartas_no_deck = getattr(deck, deck_type).all()
        contagem_cartas = {}
        for carta in cartas_no_deck:
            if carta.id in contagem_cartas:
                contagem_cartas[carta.id] += 1
            else:
                contagem_cartas[carta.id] = 1

        for carta_id, quantidade in contagem_cartas.items():
            if quantidade > 3:
                carta = Carta.objects.get(pk=carta_id)
                errors.append(f'A carta {carta.nome} aparece mais de 3 vezes no {deck_type.replace("_", " ").title()}.')

    return len(errors) == 0