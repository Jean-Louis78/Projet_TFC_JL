from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Custommer_User(AbstractUser):
    adresse = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='Clients_photos', blank=True)

    def __str__(self) -> str:
        return (f"{self.first_name} {self.last_name} {self.username}")
