# Generated by Django 5.2 on 2025-04-28 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradex', '0002_tradxtar_wallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradxtar',
            name='Quantity',
            field=models.DecimalField(decimal_places=10, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='wallet',
            name='Quantity',
            field=models.DecimalField(decimal_places=10, default=0.0, max_digits=10),
        ),
    ]
