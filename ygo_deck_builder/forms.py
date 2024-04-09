from django import forms
from .models import Deck
from collections import Counter

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name', 'main_deck', 'extra_deck', 'side_deck']

def clean(self):
    cleaned_data = super().clean()
    main_deck = cleaned_data.get('main_deck')
    extra_deck = cleaned_data.get('extra_deck')
    side_deck = cleaned_data.get('side_deck')

    # Verificar se o Main Deck não está vazio
    if not main_deck:
        raise forms.ValidationError('O Main Deck não pode estar vazio.')

    # Validar se o Main Deck contém entre 40 e 60 cartas
    if len(main_deck) < 40 or len(main_deck) > 60:
        raise forms.ValidationError('O Main Deck deve conter entre 40 e 60 cartas.')

    # Verificar se o Extra Deck não está vazio
    if not extra_deck:
        raise forms.ValidationError('O Extra Deck não pode estar vazio.')

    # Validar se o Extra Deck contém no máximo 15 cartas
    if len(extra_deck) > 15:
        raise forms.ValidationError('O Extra Deck deve conter no máximo 15 cartas.')

    # Verificar se o Side Deck não está vazio
    if not side_deck:
        raise forms.ValidationError('O Side Deck não pode estar vazio.')

    # Validar se o Side Deck contém no máximo 15 cartas
    if len(side_deck) > 15:
        raise forms.ValidationError('O Side Deck deve conter no máximo 15 cartas.')

    # Verificar se há mais de 3 cartas com o mesmo nome no Main Deck
    main_deck_counts = Counter(main_deck)
    for card_name, count in main_deck_counts.items():
        if count > 3:
            raise forms.ValidationError(f'Só é permitido até 3 cartas com o mesmo nome no Main Deck: {card_name}.')

    # Verificar se há monstros proibidos nos decks
    forbidden_monsters = ['Fusion', 'Xyz', 'Synchro', 'Link']
    for monster_type in forbidden_monsters:
        if any(monster_type in card for card in main_deck):
            raise forms.ValidationError(f'Não são permitidos monstros do tipo {monster_type} no Main Deck.')

        if any(monster_type in card for card in extra_deck):
            raise forms.ValidationError(f'Somente monstros do tipo {monster_type} são permitidos no Extra Deck.')

        if any(monster_type in card for card in side_deck):
            raise forms.ValidationError(f'Não são permitidos monstros do tipo {monster_type} no Side Deck.')

    return cleaned_data