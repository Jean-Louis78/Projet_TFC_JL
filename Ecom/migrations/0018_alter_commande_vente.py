# Generated by Django 4.2.3 on 2023-10-13 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom', '0017_alter_livraison_etat_livraison'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='vente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Ecom.vente', verbose_name='Vente'),
        ),
    ]
