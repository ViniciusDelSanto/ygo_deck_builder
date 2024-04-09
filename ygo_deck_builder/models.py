from django.db import models

class Deck(models.Model):
    name = models.CharField(max_length=100)
    main_deck = models.TextField()  # Campo para armazenar as cartas do Main Deck como texto JSON
    extra_deck = models.TextField()  # Campo para armazenar as cartas do Extra Deck como texto JSON
    side_deck = models.TextField()  # Campo para armazenar as cartas do Side Deck como texto JSON

    def __str__(self):
        return self.name