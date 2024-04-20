from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from .forms import RegisterForm
from django.contrib import messages
from .models import *

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.adresse = form.cleaned_data['adresse']
            user.photo = form.cleaned_data['photo']
            user.save()
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'USER/register2.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error={'error':"Identifiants Invalides"}
            return render(request, 'USER/login.html', error)
        
    return render(request, 'USER/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')

def all_users(request):
    utilisateurs = Custommer_User.objects.all()
    context = {
        'utilisateurs': utilisateurs
    }
    return render(request, 'USER/all-users.html', context)

def user_details(request, id):
    client = get_object_or_404(Custommer_User, id=id)
    context = {'client': client}
    return render(request, 'USER/user-details.html', context)

def user_profile(request, id):
    utilisateur = get_object_or_404(Custommer_User, id=id)
    context = {'utilisateur': utilisateur}
    return render(request, 'USER/profile.html', context)