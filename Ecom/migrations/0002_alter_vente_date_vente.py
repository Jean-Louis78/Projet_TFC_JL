# Generated by Django 4.2.3 on 2023-09-09 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vente',
            name='date_vente',
            field=models.DateTimeField(editable=False),
        ),
    ]
