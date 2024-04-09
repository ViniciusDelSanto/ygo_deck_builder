# Generated by Django 5.0.3 on 2024-04-09 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ygo_deck_builder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='extra_deck',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deck',
            name='main_deck',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deck',
            name='side_deck',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]