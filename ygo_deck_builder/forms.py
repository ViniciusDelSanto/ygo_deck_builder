from django import forms
from .models import Deck, Card
from collections import Counter

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name', 'main_deck', 'extra_deck', 'side_deck']
        widgets = {
            'main_deck': forms.CheckboxSelectMultiple,
            'extra_deck': forms.CheckboxSelectMultiple,
            'side_deck': forms.CheckboxSelectMultiple,
        }

    def clean(self):
        cleaned_data = super(DeckForm, self).clean()
        main_deck = cleaned_data.get('main_deck')
        extra_deck = cleaned_data.get('extra_deck')
        side_deck = cleaned_data.get('side_deck')

        # Validação das cartas
        self._validate_deck_size(main_deck, 40, 60, 'Main Deck')
        self._validate_deck_size(extra_deck, 0, 15, 'Extra Deck')
        self._validate_deck_size(side_deck, 0, 15, 'Side Deck')
        self._validate_card_limit(main_deck, 'Main Deck')
        self._validate_forbidden_monsters(main_deck, extra_deck, side_deck)

        return cleaned_data

    def _validate_deck_size(self, deck, min_size, max_size, deck_name):
        if deck and (len(deck) < min_size or len(deck) > max_size):
            raise forms.ValidationError(f'O {deck_name} deve conter entre {min_size} e {max_size} cartas.')

    def _validate_card_limit(self, deck, deck_name):
        if deck:
            card_counts = Counter(deck)
            for card_name, count in card_counts.items():
                if count > 3:
                    raise forms.ValidationError(f'Só é permitido até 3 cartas com o mesmo nome no {deck_name}: {card_name}.')

    def _validate_forbidden_monsters(self, main_deck, extra_deck, side_deck):
        forbidden_monsters = ['Fusion', 'Xyz', 'Synchro', 'Link']
        for monster_type in forbidden_monsters:
            if main_deck and any(monster_type in card.type for card in main_deck):
                raise forms.ValidationError(f'Não são permitidos monstros do tipo {monster_type} no Main Deck.')
            if extra_deck and any(monster_type not in card.type for card in extra_deck):
                raise forms.ValidationError(f'Somente monstros do tipo {monster_type} são permitidos no Extra Deck.')
            if side_deck and any(monster_type in card.type for card in side_deck):
                raise forms.ValidationError(f'Não são permitidos monstros do tipo {monster_type} no Side Deck.')