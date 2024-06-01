from django.core.management.base import BaseCommand
import requests
from decks.models import Carta

class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
        response = requests.get(url)
        data = response.json()

        for card_data in data['data']:
            carta, created = Carta.objects.get_or_create(
                api_id=card_data['id'],
                defaults={
                    'nome': card_data['name'],
                    'tipo': card_data['type'],
                    'ataque': card_data.get('atk', None),
                    'defesa': card_data.get('def', None),
                    'desc': card_data.get('desc', None),
                    'imagem_url': card_data['card_images'][0]['image_url']
                }
            )
            if created:
                print(f'Carta "{carta.nome}" criada.')