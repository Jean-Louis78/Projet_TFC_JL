from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Custommer_User

class RegisterForm(UserCreationForm):
    adresse = forms.CharField(max_length=200, required=True)
    photo = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["last_name"].widget.attrs.update({
            'required':'',
            'name':'',
            'id':'',
            'type':'text',
            'class':'form-control',
            'placeholder':'Jean-Louis',
        })
        self.fields["first_name"].widget.attrs.update({
            'required':'',
            'name':'',
            'id':'',
            'type':'text',
            'class':'form-control',
            'placeholder':'Douglas',
        })
        self.fields["username"].widget.attrs.update({
            'required':'',
            'name':'',
            'id':'',
            'type':'text',
            'class':'form-control',
            'placeholder':'Antisystem',
        })
        self.fields["email"].widget.attrs.update({
            'required':'',
            'name':'',
            'id':'',
            'type':'text',
            'class':'form-control',
            'placeholder':'jeanlouisdouglas93@gmail.com',
        })
        self.fields["adresse"].widget.attrs.update({
            'required':'',
            'name':'',
            'id':'',
            'type':'text',
            'class':'form-control',
            'placeholder':'Goma, Com.Goma, Q.Kyeshero, Av.Mulu',
        })
        self.fields["password1"].widget.attrs.update({
            'required':'',
            'name':'',
            'id':'',
            'type':'text',
            'class':'form-control',
            'placeholder':'12345678',
        })
        self.fields["password2"].widget.attrs.update({
            'required':'',
            'name':'',
            'id':'',
            'type':'text',
            'class':'form-control',
            'placeholder':'12345678',
        })
        self.fields["photo"].widget.attrs.update({
            'required':'',
            'name':'',
            'id':'',
            'type':'text',
            'class':'form-control',
        })

    class Meta:
        model = Custommer_User
        fields = ('last_name','first_name','username','email','adresse','password1','password2','photo')

