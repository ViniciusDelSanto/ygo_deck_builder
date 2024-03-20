import requests
from django.shortcuts import render


# Create your views here.


# urls.py




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

