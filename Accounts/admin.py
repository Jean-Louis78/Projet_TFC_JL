from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Custommer_User)
class TabClient(admin.ModelAdmin):
    list_display=['last_name','first_name','username','email','adresse']
