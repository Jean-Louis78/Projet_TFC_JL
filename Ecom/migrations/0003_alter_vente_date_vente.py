# Generated by Django 4.2.3 on 2023-09-09 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom', '0002_alter_vente_date_vente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vente',
            name='date_vente',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]