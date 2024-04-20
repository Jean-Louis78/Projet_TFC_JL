# Generated by Django 4.2.3 on 2023-09-29 20:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Ecom', '0007_livreur_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Client'),
        ),
    ]
