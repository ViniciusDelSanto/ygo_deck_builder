from django.db import models

class Card(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=50)
    atk = models.IntegerField(null=True, blank=True)
    defense = models.IntegerField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    race = models.CharField(max_length=50)
    attribute = models.CharField(max_length=50)
    desc = models.TextField()
    image_url = models.URLField(max_length=200) 

    def __str__(self):
        return self.name

class Deck(models.Model):
    name = models.CharField(max_length=100)
    main_deck = models.ManyToManyField(Card, related_name='main_decks', blank=True)
    extra_deck = models.ManyToManyField(Card, related_name='extra_decks', blank=True)
    side_deck = models.ManyToManyField(Card, related_name='side_decks', blank=True)

    def __str__(self):
        return self.name