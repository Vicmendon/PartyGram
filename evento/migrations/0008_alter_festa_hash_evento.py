# Generated by Django 5.1.5 on 2025-01-28 16:36

import evento.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evento', '0007_festa_hash_evento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='festa',
            name='hash_evento',
            field=models.CharField(default=evento.models.gerar_hash_evento, max_length=20),
        ),
    ]
