# Generated by Django 4.2.3 on 2023-10-15 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom', '0023_alter_commande_livreur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='stock_dispo',
            field=models.IntegerField(),
        ),
    ]
