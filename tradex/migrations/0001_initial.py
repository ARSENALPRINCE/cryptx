# Generated by Django 5.2 on 2025-04-23 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('symbol', models.CharField(choices=[('BTC', 'Bitcoin'), ('ETH', 'Ethereum'), ('LTC', 'Litecoin'), ('DOGE', 'Dogecoin')], max_length=5, unique=True)),
                ('description', models.TextField(default='')),
                ('price', models.DecimalField(decimal_places=3, max_digits=9)),
            ],
        ),
    ]
