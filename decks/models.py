from django.db import models

class Carta(models.Model):
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    ataque = models.IntegerField(blank=True, null=True)  # Adicione ataque
    defesa = models.IntegerField(blank=True, null=True) # Adicione defesa
    desc = models.TextField(blank=True, null=True)
    api_id = models.IntegerField(unique=True)
    imagem_url = models.URLField(blank=True)

    def __str__(self):
        return self.nome

class Deck(models.Model):
    nome = models.CharField(max_length=255)
    main_deck = models.ManyToManyField(Carta, related_name='main_decks')
    extra_deck = models.ManyToManyField(Carta, related_name='extra_decks')
    side_deck = models.ManyToManyField(Carta, related_name='side_decks')

    def __str__(self):
        return self.nome