# Generated by Django 4.2.3 on 2023-09-29 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom', '0006_delete_panier'),
    ]

    operations = [
        migrations.AddField(
            model_name='livreur',
            name='password',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
    ]
